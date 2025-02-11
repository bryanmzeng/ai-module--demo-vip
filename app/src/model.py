from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import numpy as np

app = Flask(__name__)
CORS(app)

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_metrics(text):
    # Get base sentiment
    sentiment_result = sentiment_analyzer(text)[0]
    
    # Generate mock scores for different metrics (replace with actual model inferences)
    # These are example metrics - modify as needed
    return {
        "social_level": sentiment_result['score'] * 2,
        "communication_style": sentiment_result['score'] * 1.5,
        "emotional_tone": sentiment_result['score'],
        "confidence_score": sentiment_result['score'] * 0.5,
        "positivity": sentiment_result['score'] if sentiment_result['label'] == 'POSITIVE' else 0,
        "sentiment_label": sentiment_result['label'],
        "sentiment_score": sentiment_result['score']
    }

@app.route('/analyze', methods=['POST'])
@app.route('/analyze', methods=['POST'])
def analyze():
    print("\n--- Received Request ---")  # Debug log
    try:
        data = request.get_json()
        print("Received data:", data)    # Debug log
        text = data.get('text', '')
        
        if not text:
            print("Empty text error")    # Debug log
            return jsonify({"error": "No text provided"}), 400
        
        metrics = analyze_metrics(text)
        print("Response data:", metrics) # Debug log
        return jsonify(metrics)
        
    except Exception as e:
        print("Error:", str(e))          # Debug log
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)