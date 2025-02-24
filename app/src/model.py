from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import time

app = Flask(__name__)
CORS(app)

# Load models with detailed score returns
sentiment_analyzer = pipeline("sentiment-analysis", return_all_scores=True)
emotion_analyzer = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", return_all_scores=True)
formality_analyzer = pipeline("text-classification", model="s-nlp/roberta-base-formality-ranker", return_all_scores=True)
toxicity_analyzer = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)
empathy_analyzer = pipeline("text-classification", model="michellejieli/emotion_text_classifier", return_all_scores=True)

def get_top_label(results):
    """Helper to get the highest confidence label from results"""
    return max(results, key=lambda x: x['score'])

def analyze_metrics(text):
    # Initialize testing metrics collection
    testing_metrics = {
        "model_versions": {},
        "inference_times": {},
        "confidence_breakdown": {},
        "text_statistics": {}
    }
    
    # Text statistics
    testing_metrics["text_statistics"] = {
        "text_length": len(text),
        "word_count": len(text.split()),
        "estimated_tokens": len(sentiment_analyzer.tokenizer.tokenize(text))
    }

    # Sentiment analysis
    start = time.time()
    sentiment_results = sentiment_analyzer(text)[0]
    testing_metrics["inference_times"]["sentiment"] = time.time() - start
    sentiment_top = get_top_label(sentiment_results)
    testing_metrics["confidence_breakdown"]["sentiment"] = sentiment_results
    testing_metrics["model_versions"]["sentiment"] = sentiment_analyzer.model.config._name_or_path

    # Emotion analysis
    start = time.time()
    emotion_results = emotion_analyzer(text)[0]
    testing_metrics["inference_times"]["emotion"] = time.time() - start
    emotion_top = get_top_label(emotion_results)
    testing_metrics["confidence_breakdown"]["emotion"] = emotion_results
    testing_metrics["model_versions"]["emotion"] = emotion_analyzer.model.config._name_or_path

    # Formality analysis
    start = time.time()
    formality_results = formality_analyzer(text)[0]
    testing_metrics["inference_times"]["formality"] = time.time() - start
    formality_top = get_top_label(formality_results)
    formality_score = formality_top['score'] if formality_top['label'] == 'formal' else 1 - formality_top['score']
    testing_metrics["confidence_breakdown"]["formality"] = formality_results
    testing_metrics["model_versions"]["formality"] = formality_analyzer.model.config._name_or_path

    # Toxicity analysis
    start = time.time()
    toxicity_results = toxicity_analyzer(text)[0]
    testing_metrics["inference_times"]["toxicity"] = time.time() - start
    toxicity_score = max(item['score'] for item in toxicity_results)
    testing_metrics["confidence_breakdown"]["toxicity"] = toxicity_results
    testing_metrics["model_versions"]["toxicity"] = toxicity_analyzer.model.config._name_or_path

    # Empathy analysis (Note: Verify model labels match your use case)
    start = time.time()
    empathy_results = empathy_analyzer(text)[0]
    testing_metrics["inference_times"]["empathy"] = time.time() - start
    empathy_top = get_top_label(empathy_results)
    empathy_score = empathy_top['score'] if empathy_top['label'] == 'empathy' else 1 - empathy_top['score']
    testing_metrics["confidence_breakdown"]["empathy"] = empathy_results
    testing_metrics["model_versions"]["empathy"] = empathy_analyzer.model.config._name_or_path

    return {
        "social_awareness": formality_score,
        "communication_style": empathy_score,
        "emotional_tone": {
            "primary_emotion": emotion_top['label'],
            "emotion_confidence": emotion_top['score'],
            "sentiment": sentiment_top['label'],
            "sentiment_score": sentiment_top['score']
        },
        "confidence_score": 1 - toxicity_score,
        "positivity_ratio": sentiment_top['score'] if sentiment_top['label'] == 'POSITIVE' else 1 - sentiment_top['score'],
        "toxicity_risk": toxicity_score,
        "emotional_intelligence": empathy_score * formality_score,
        "testing_metrics": testing_metrics
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