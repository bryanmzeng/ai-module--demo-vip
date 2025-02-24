import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expandedSections, setExpandedSections] = useState({});

  const analyzeText = async () => {
    if (!text) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5001/analyze', { text });
      setResults(response.data);
      setExpandedSections({});
    } catch (error) {
      console.error('Error analyzing text:', error);
    }
    setLoading(false);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
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

  const renderConfidenceBreakdown = () => {
    if (!results?.testing_metrics?.confidence_breakdown) return null;
    
    return Object.entries(results.testing_metrics.confidence_breakdown).map(([model, scores]) => (
      <div key={model} className="confidence-section">
        <h4 onClick={() => toggleSection(model)}>
          {model.charAt(0).toUpperCase() + model.slice(1)} Confidence Scores ▼
        </h4>
        {expandedSections[model] && (
          <div className="confidence-scores">
            {scores.map((score, index) => (
              <div key={index} className="score-item">
                <span>{score.label}:</span>
                <span>{(score.score * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        )}
      </div>
    ));
  };

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
            {/* Existing metrics */}
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

            {/* Testing Metrics */}
            <div className="testing-metrics">
              <h3>Model Diagnostics</h3>
              
              <div className="model-versions">
                <h4>Model Versions</h4>
                {results.testing_metrics.model_versions && Object.entries(results.testing_metrics.model_versions).map(([name, version]) => (
                  <div key={name} className="model-version">
                    <span className="model-name">{name}:</span>
                    <span className="model-version">{version}</span>
                  </div>
                ))}
              </div>

              <div className="inference-times">
                <h4>Processing Times (ms)</h4>
                {results.testing_metrics.inference_times && Object.entries(results.testing_metrics.inference_times).map(([model, time]) => (
                  <div key={model} className="time-item">
                    <span>{model}:</span>
                    <span>{(time * 1000).toFixed(1)}</span>
                  </div>
                ))}
              </div>

              <div className="text-statistics">
                <h4>Text Statistics</h4>
                <p>Characters: {results.testing_metrics.text_statistics.text_length}</p>
                <p>Words: {results.testing_metrics.text_statistics.word_count}</p>
                <p>Estimated Tokens: {results.testing_metrics.text_statistics.estimated_tokens}</p>
              </div>

              <div className="confidence-breakdown">
                <h4>Model Confidence Breakdown</h4>
                {renderConfidenceBreakdown()}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;