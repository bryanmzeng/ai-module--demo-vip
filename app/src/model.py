from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import numpy as np

app = Flask(__name__)
CORS(app)

# Load multiple analysis models
sentiment_analyzer = pipeline("sentiment-analysis")
emotion_analyzer = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")
formality_analyzer = pipeline("text-classification", model="s-nlp/roberta-base-formality-ranker")
toxicity_analyzer = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)
empathy_analyzer = pipeline("text-classification", model="michellejieli/emotion_text_classifier")

def analyze_metrics(text):
    sentiment_result = sentiment_analyzer(text)[0]
    
    # emotion analysis - 6 basic emotions from model
    emotion_result = emotion_analyzer(text)[0]
    
    # formality score: 0-1 where 1= most formal
    formality_result = formality_analyzer(text)[0]
    formality_score = formality_result['score'] if formality_result['label'] == 'formal' else 1 - formality_result['score']
    
    # toxicity analysis - toxicity of text
    toxicity_scores = [item['score'] for item in toxicity_analyzer(text)[0]]
    toxicity_score = max(toxicity_scores)
    
    # empathy/emotional awareness score
    empathy_result = empathy_analyzer(text)[0]
    empathy_score = empathy_result['score'] if empathy_result['label'] == 'empathy' else 1 - empathy_result['score']

    return {
        "social_awareness": formality_score,
        "communication_style": empathy_score,
        "emotional_tone": {
            "primary_emotion": emotion_result['label'],
            "emotion_confidence": emotion_result['score'],
            "sentiment": sentiment_result['label'],
            "sentiment_score": sentiment_result['score']
        },
        "confidence_score": 1 - toxicity_score,  # Inverse of toxicity as confidence proxy- will connect to model in future version
        "positivity_ratio": sentiment_result['score'] if sentiment_result['label'] == 'POSITIVE' else 1 - sentiment_result['score'],
        "toxicity_risk": toxicity_score,
        "emotional_intelligence": empathy_score * formality_score
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        metrics = analyze_metrics(text)
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

#test blurbs

#"Hello, my name is Bob, and I’m a passionate AI researcher and developer with a strong background in machine learning, NLP, and data-driven solutions. I thrive on solving complex problems, whether it’s optimizing financial models, enhancing AI-driven applications, or developing intuitive tools that bridge the gap between research and real-world impact. My experience spans academia, industry, and mentorship, where I’ve had the privilege of guiding others while continuously learning myself. I believe in the power of innovation, collaboration, and thoughtful execution to push boundaries in AI and data science. If you’re excited about cutting-edge AI, let’s connect and build something incredible together!"

#"Hey... I guess I should introduce myself. I’m Joe, and honestly, I don’t know why I’m even doing this. I work with AI and machine learning, but half the time, it feels like I’m just throwing data at models and hoping for the best. Sure, I’ve done some cool projects, but nothing ever seems good enough. The tech world moves too fast, and everyone else seems miles ahead. Anyway, if you want to talk about AI, trading, or whatever, I guess I’m around. Just don’t expect me to be the one who has all the answers."