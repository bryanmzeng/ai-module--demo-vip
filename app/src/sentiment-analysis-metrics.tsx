import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AccuracyDashboard = () => {
  const [selectedMetric, setSelectedMetric] = useState('all');

  // Sample data from our analysis
  const testResults = [
    {
      id: 1,
      text: "Hello, my name is Bob, and I'm a passionate AI researcher...",
      primary_emotion: { expected: "joy", actual: "joy", match: true },
      sentiment: { expected: "POSITIVE", actual: "POSITIVE", match: true },
      formality: { expected: 0.75, actual: 0.72, difference: 0.03 },
      toxicity: { expected: 0.05, actual: 0.03, difference: 0.02 },
      empathy: { expected: 0.8, actual: 0.76, difference: 0.04 }
    },
    {
      id: 2,
      text: "Hey... I guess I should introduce myself. I'm Joe...",
      primary_emotion: { expected: "sadness", actual: "sadness", match: true },
      sentiment: { expected: "NEGATIVE", actual: "NEGATIVE", match: true },
      formality: { expected: 0.3, actual: 0.35, difference: 0.05 },
      toxicity: { expected: 0.1, actual: 0.12, difference: 0.02 },
      empathy: { expected: 0.4, actual: 0.45, difference: 0.05 }
    },
    {
      id: 3,
      text: "I'm absolutely furious with the customer service I received!...",
      primary_emotion: { expected: "anger", actual: "anger", match: true },
      sentiment: { expected: "NEGATIVE", actual: "NEGATIVE", match: true },
      formality: { expected: 0.4, actual: 0.42, difference: 0.02 },
      toxicity: { expected: 0.4, actual: 0.48, difference: 0.08 },
      empathy: { expected: 0.2, actual: 0.23, difference: 0.03 }
    },
    {
      id: 4,
      text: "I'm delighted to share that our team has successfully completed...",
      primary_emotion: { expected: "joy", actual: "joy", match: true },
      sentiment: { expected: "POSITIVE", actual: "POSITIVE", match: true },
      formality: { expected: 0.8, actual: 0.78, difference: 0.02 },
      toxicity: { expected: 0.05, actual: 0.04, difference: 0.01 },
      empathy: { expected: 0.7, actual: 0.72, difference: 0.02 }
    },
    {
      id: 5,
      text: "The technical specifications for this system are as follows...",
      primary_emotion: { expected: "neutral", actual: "neutral", match: true },
      sentiment: { expected: "NEUTRAL", actual: "NEUTRAL", match: true },
      formality: { expected: 0.9, actual: 0.91, difference: 0.01 },
      toxicity: { expected: 0.05, actual: 0.02, difference: 0.03 },
      empathy: { expected: 0.3, actual: 0.28, difference: 0.02 }
    },
    {
      id: 6,
      text: "I feel so lost and overwhelmed. Everything seems to be falling apart...",
      primary_emotion: { expected: "sadness", actual: "sadness", match: true },
      sentiment: { expected: "NEGATIVE", actual: "NEGATIVE", match: true },
      formality: { expected: 0.4, actual: 0.48, difference: 0.08 },
      toxicity: { expected: 0.1, actual: 0.09, difference: 0.01 },
      empathy: { expected: 0.6, actual: 0.64, difference: 0.04 }
    },
    {
      id: 7,
      text: "Thank you so much for your thoughtful feedback on my presentation...",
      primary_emotion: { expected: "joy", actual: "joy", match: true },
      sentiment: { expected: "POSITIVE", actual: "POSITIVE", match: true },
      formality: { expected: 0.7, actual: 0.74, difference: 0.04 },
      toxicity: { expected: 0.05, actual: 0.02, difference: 0.03 },
      empathy: { expected: 0.8, actual: 0.85, difference: 0.05 }
    },
    {
      id: 8,
      text: "This product is absolutely terrible! I wasted my money...",
      primary_emotion: { expected: "anger", actual: "anger", match: true },
      sentiment: { expected: "NEGATIVE", actual: "NEGATIVE", match: true },
      formality: { expected: 0.3, actual: 0.31, difference: 0.01 },
      toxicity: { expected: 0.6, actual: 0.65, difference: 0.05 },
      empathy: { expected: 0.2, actual: 0.18, difference: 0.02 }
    },
    {
      id: 9,
      text: "I'm writing to formally request a two-week leave of absence...",
      primary_emotion: { expected: "neutral", actual: "neutral", match: true },
      sentiment: { expected: "NEUTRAL", actual: "NEUTRAL", match: true },
      formality: { expected: 0.9, actual: 0.89, difference: 0.01 },
      toxicity: { expected: 0.05, actual: 0.03, difference: 0.02 },
      empathy: { expected: 0.5, actual: 0.47, difference: 0.03 }
    },
    {
      id: 10,
      text: "I'm so excited about our upcoming vacation! We've been planning...",
      primary_emotion: { expected: "joy", actual: "joy", match: true },
      sentiment: { expected: "POSITIVE", actual: "POSITIVE", match: true },
      formality: { expected: 0.5, actual: 0.56, difference: 0.06 },
      toxicity: { expected: 0.05, actual: 0.02, difference: 0.03 },
      empathy: { expected: 0.7, actual: 0.73, difference: 0.03 }
    }
  ];

  // Calculate overall accuracy metrics
  const totalSamples = testResults.length;
  const emotionMatches = testResults.filter(r => r.primary_emotion.match).length;
  const sentimentMatches = testResults.filter(r => r.sentiment.match).length;
  const emotionAccuracy = (emotionMatches / totalSamples * 100).toFixed(1);
  const sentimentAccuracy = (sentimentMatches / totalSamples * 100).toFixed(1);
  
  // Calculate average differences for numeric metrics
  const avgFormalityDiff = testResults.reduce((sum, r) => sum + r.formality.difference, 0) / totalSamples;
  const avgToxicityDiff = testResults.reduce((sum, r) => sum + r.toxicity.difference, 0) / totalSamples;
  const avgEmpathyDiff = testResults.reduce((sum, r) => sum + r.empathy.difference, 0) / totalSamples;
  
  // Prepare data for charts
  const accuracyData = [
    { name: 'Emotion', accuracy: parseFloat(emotionAccuracy) },
    { name: 'Sentiment', accuracy: parseFloat(sentimentAccuracy) }
  ];
  
  const differenceData = [
    { name: 'Formality', difference: avgFormalityDiff },
    { name: 'Toxicity', difference: avgToxicityDiff },
    { name: 'Empathy', difference: avgEmpathyDiff }
  ];
  
  // Prepare detailed comparison data based on selected metric
  const getDetailData = () => {
    if (selectedMetric === 'all') {
      return testResults.map(r => ({
        id: r.id,
        sample: `Sample ${r.id}`,
        formality_expected: r.formality.expected,
        formality_actual: r.formality.actual,
        toxicity_expected: r.toxicity.expected,
        toxicity_actual: r.toxicity.actual,
        empathy_expected: r.empathy.expected,
        empathy_actual: r.empathy.actual
      }));
    } else {
      return testResults.map(r => ({
        id: r.id,
        sample: `Sample ${r.id}`,
        expected: r[selectedMetric].expected,
        actual: r[selectedMetric].actual,
        difference: r[selectedMetric].difference
      }));
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Sentiment Analysis Test Results</h2>
      
      <div className="summary-metrics">
        <div className="metric-card">
          <h3>Sample Size</h3>
          <p className="metric-value">{totalSamples}</p>
        </div>
        <div className="metric-card">
          <h3>Emotion Accuracy</h3>
          <p className="metric-value">{emotionAccuracy}%</p>
        </div>
        <div className="metric-card">
          <h3>Sentiment Accuracy</h3>
          <p className="metric-value">{sentimentAccuracy}%</p>
        </div>
        <div className="metric-card">
          <h3>Avg Metric Difference</h3>
          <p className="metric-value">{((avgFormalityDiff + avgToxicityDiff + avgEmpathyDiff) / 3).toFixed(2)}</p>
        </div>
      </div>
      
      <div className="charts-container">
        <div className="chart-section">
          <h3>Classification Accuracy</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={accuracyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="chart-section">
          <h3>Average Metric Differences</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={differenceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 0.1]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="difference" fill="#82ca9d" name="Avg Difference" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="metric-details">
        <h3>Detailed Comparison</h3>
        
        <div className="metric-selector">
          <label>Select Metric: </label>
          <select 
            value={selectedMetric} 
            onChange={(e) => setSelectedMetric(e.target.value)}
          >
            <option value="all">All Metrics</option>
            <option value="formality">Formality</option>
            <option value="toxicity">Toxicity</option>
            <option value="empathy">Empathy</option>
          </select>
        </div>
        
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Sample</th>
                {selectedMetric === 'all' ? (
                  <>
                    <th>Formality (Expected)</th>
                    <th>Formality (Actual)</th>
                    <th>Toxicity (Expected)</th>
                    <th>Toxicity (Actual)</th>
                    <th>Empathy (Expected)</th>
                    <th>Empathy (Actual)</th>
                  </>
                ) : (
                  <>
                    <th>Expected</th>
                    <th>Actual</th>
                    <th>Difference</th>
                  </>
                )}
              </tr>
            </thead>
            <tbody>
              {getDetailData().map(item => (
                <tr key={item.id}>
                  <td>{item.sample}</td>
                  {selectedMetric === 'all' ? (
                    <>
                      <td>{item.formality_expected.toFixed(2)}</td>
                      <td>{item.formality_actual.toFixed(2)}</td>
                      <td>{item.toxicity_expected.toFixed(2)}</td>
                      <td>{item.toxicity_actual.toFixed(2)}</td>
                      <td>{item.empathy_expected.toFixed(2)}</td>
                      <td>{item.empathy_actual.toFixed(2)}</td>
                    </>
                  ) : (
                    <>
                      <td>{typeof item.expected === 'number' ? item.expected.toFixed(2) : item.expected}</td>
                      <td>{typeof item.actual === 'number' ? item.actual.toFixed(2) : item.actual}</td>
                      <td>{typeof item.difference === 'number' ? item.difference.toFixed(2) : 'N/A'}</td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AccuracyDashboard;
