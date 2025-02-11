import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!text) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5001/analyze', { text });
      setResults(response.data);
    } catch (error) {
      console.error('Error analyzing text:', error);
    }
    setLoading(false);
  };

  const MetricBar = ({ label, value }) => (
    <div className="metric">
      <div className="metric-label">{label}</div>
      <div className="metric-bar-container">
        <div 
          className="metric-bar" 
          style={{ width: `${value * 100}%` }}
        >
          {Math.round(value * 100)}%
        </div>
      </div>
    </div>
  );

  return (
    <div className="App">
      <h1>AI Text Analysis</h1>
      
      <div className="input-section">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text..."
          rows="5"
        />
        <button onClick={analyzeText} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Text'}
        </button>
      </div>

      {results && (
        <div className="results-section">
          <h2>Analysis Results</h2>
          <div className="metrics-container">
            <MetricBar label="Social Awareness" value={results.social_awareness} />
            <MetricBar label="Communication Style" value={results.communication_style} />
            <MetricBar label="Confidence Score" value={results.confidence_score} />
            <MetricBar label="Positivity Ratio" value={results.positivity_ratio} />
            <MetricBar label="Toxicity Risk" value={results.toxicity_risk} />
            <MetricBar label="Emotional Intelligence" value={results.emotional_intelligence} />
            
            <div className="sentiment-result">
              <h3>Emotional Tone</h3>
              <p>Primary Emotion: {results.emotional_tone.primary_emotion}</p>
              <p>Emotion Confidence: {Math.round(results.emotional_tone.emotion_confidence * 100)}%</p>
              <p>Sentiment: {results.emotional_tone.sentiment}</p>
              <p>Sentiment Score: {Math.round(results.emotional_tone.sentiment_score * 100)}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;