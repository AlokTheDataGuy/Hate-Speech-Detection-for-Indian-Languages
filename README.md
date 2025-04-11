# Multilingual Hate Speech Detection

![Project Screenshot](/screenshot/screenshot.png)

## Overview
This project is a **Multilingual Hate Speech Detection System** that detects hate speech in **English, Hindi, Bengali and Marathi**. It supports **text input, and YouTube comment detection**. The system is built using a **fine-tuned MuRIL model**, a **Flask backend**, and a **React + Tailwind frontend**.

## Features
- **Multilingual Text Detection**: Supports multiple Indian languages.
- **Audio Hate Speech Detection**: Converts speech to text and detects hate speech.
- **YouTube Comment Analysis**: Extracts comments from YouTube videos and classifies them.
- **Real-Time Processing**: Provides instant results for user inputs.
- **Web-Based Interface**: User-friendly UI built with React and Tailwind CSS.

## Tech Stack
- **Frontend**: React, Tailwind CSS
- **Backend**: Flask, FastAPI
- **Model**: MuRIL (Fine-tuned for hate speech detection)
- **Database**: MongoDB / Firebase (optional for logging results)
- **APIs & Libraries**: YouTube API, Speech-to-Text (Google API, Whisper, or similar), Transformers, Torch, Scikit-learn

## Installation
### Prerequisites
- Python 3.9+
- Node.js 18+
- GPU with CUDA support (recommended for faster inference)

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/AlokTheDataGuy/multilingual-hate-speech.git
cd multilingual-hate-speech/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```

### Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start the frontend
npm start
```

## Usage
1. **Text Analysis**: Enter text and check if it contains hate speech.
2. **Audio Detection**: Upload an audio file or use live speech detection.
3. **YouTube Analysis**: Enter a video link to analyze its comments.
4. **Real-time Results**: Get an immediate classification output.

## Model Files
Since the model files and results folder have been removed due to their large size, you can download the pre-trained model from:
[MuRIL Fine-tuned Model on Hugging Face](https://huggingface.co/Hate-speech-CNERG/indic-abusive-allInOne-MuRIL/tree/main)

## Model Training & Fine-tuning
1. Prepare your dataset (`train_dataset.pt`, `val_dataset.pt`).
2. Run the training script:
   ```bash
   python train.py --epochs 3 --batch_size 16 --lr 5e-5
   ```
3. Save and deploy the trained model for inference.

## Future Enhancements
- **Live Audio Streaming Detection**
- **Improved YouTube API Integration**
- **Customizable Hate Speech Categories**

## Contributors
- **Alok Deep** ([@lazylad99](https://github.com/lazylad99))

## License
This project is licensed under the MIT License.

