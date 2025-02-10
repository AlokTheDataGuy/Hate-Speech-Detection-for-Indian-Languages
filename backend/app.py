import re
import requests
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from transformers import AutoProcessor, AutoModelForCTC
import torch
# import soundfile as sf  
from scipy.io.wavfile import write
import tempfile
import numpy as np
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)


# # Load the processor and model
# processor = AutoProcessor.from_pretrained("theainerd/Wav2Vec2-large-xlsr-hindi")
# model = AutoModelForCTC.from_pretrained("theainerd/Wav2Vec2-large-xlsr-hindi")

# Load the fine-tuned MuRIL model
model_path = "training/muril_hate_speech_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Import the hardcoded phrases from the external file
from hate_speech_data import HARD_CODED_HATE, HARD_CODED_NON_HATE

# Set up API key for YouTube
YOUTUBE_API_KEY = "AIzaSyBgsEzrFPrpTOBpsyx5LTeP-HzXg_KgLRk"

# Function to extract video ID from a full YouTube URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return url  # Return as-is if already a video ID

# Function to fetch comments from YouTube using the YouTube Data API
def fetch_comments_from_youtube(video_id):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'key': YOUTUBE_API_KEY,
        'videoId': video_id,
        'part': 'snippet',
        'maxResults': 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'items' in data:
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
    return comments

# Preprocess text data: Remove URLs, mentions, etc.
def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text

# Rule-based classification
def rule_based_classification(text):
    for phrase in HARD_CODED_HATE:
        if phrase in text.lower():
            return 1  # Hate
    for phrase in HARD_CODED_NON_HATE:
        if phrase in text.lower():
            return 0  # Non-hate
    return None  # Let the model decide if no match

def predict_hate_speech(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    inputs = {key: val.to(device) for key, val in inputs.items()}  # Move to GPU if available

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).cpu().numpy()
    return predictions


# Function to transcribe audio using Wav2Vec2
def transcribe_audio_wav2vec(audio_file):
    # Read the audio file
    audio_input, _ = sf.read(audio_file)
    
    # Process the audio input (convert it to the correct format for the model)
    inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt")
    
    # Make predictions (get logits)
    with torch.no_grad():
        logits = model(**inputs).logits

    # Get the predicted IDs (the text in terms of token IDs)
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the predicted IDs into text
    text = processor.decode(predicted_ids[0])
    return text


# Analyze hate speech and calculate percentage, including sample comments
def analyze_hate_speech(comments):
    processed_comments = [clean_text(comment) for comment in comments]
    predictions = []
    
    for comment in processed_comments:
        rule_based_result = rule_based_classification(comment)
        if rule_based_result is not None:
            predictions.append(rule_based_result)
        else:
            model_prediction = predict_hate_speech([comment])[0]
            predictions.append(model_prediction)

    hate_speech_count = predictions.count(1)
    hate_speech_percentage = (hate_speech_count / len(comments)) * 100 if comments else 0

    hate_samples = []
    non_hate_samples = []
    for comment, prediction in zip(comments, predictions):
        if prediction == 1 and len(hate_samples) < 5:
            hate_samples.append(comment)
        elif prediction == 0 and len(non_hate_samples) < 5:
            non_hate_samples.append(comment)

    return hate_speech_percentage, hate_samples, non_hate_samples

# Route to handle the request from the frontend
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    link = data.get('link')
    audio_file = request.files.get('audio')

    if link:
        if "youtube.com" in link or "youtu.be" in link:
            video_id = extract_video_id(link)
            comments = fetch_comments_from_youtube(video_id)
            if not comments:
                return jsonify({'error': 'No comments found for this video.'}), 404
            hate_speech_percentage, hate_samples, non_hate_samples = analyze_hate_speech(comments)
            return jsonify({
                'hateSpeechPercentage': hate_speech_percentage,
                'hateSpeechSamples': hate_samples,
                'nonHateSpeechSamples': non_hate_samples
            }), 200
        else:
            return jsonify({'error': 'Unsupported link. Currently only YouTube links are supported.'}), 400

    elif text:
        hate_speech_percentage, hate_samples, non_hate_samples = analyze_hate_speech([text])
        return jsonify({
            'hateSpeechPercentage': hate_speech_percentage,
            'hateSpeechSamples': hate_samples,
            'nonHateSpeechSamples': non_hate_samples
        }), 200

    elif audio_file:
        transcription = transcribe_audio_wav2vec(audio_file)
        hate_speech_percentage, hate_samples, non_hate_samples = analyze_hate_speech([transcription])
        return jsonify({
            'hateSpeechPercentage': hate_speech_percentage,
            'hateSpeechSamples': hate_samples,
            'nonHateSpeechSamples': non_hate_samples
        }), 200


    else:
        return jsonify({'error': 'Either text, a link, or audio is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
