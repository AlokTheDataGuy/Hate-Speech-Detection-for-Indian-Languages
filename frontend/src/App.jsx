import React, { useState } from "react";
import axios from "axios";
import SocialMediaAnalyzer from "./components/SocialMediaAnalyzer";

function App() {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", { text });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative bg-cover bg-center bg-no-repeat"
      style={{ backgroundImage: 'url("/hate.jpg")' }}>
      <div className="absolute inset-0 bg-black bg-opacity-30 z-10"></div>
      
      <div className="relative z-20 my-16 max-w-3xl w-full p-6 rounded-lg shadow-lg">
        <SocialMediaAnalyzer />
      </div>
    </div>
  );
}

export default App;
