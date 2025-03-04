# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import pipeline
# import time

# app = Flask(__name__)
# CORS(app)

# # Load models with detailed score returns
# sentiment_analyzer = pipeline("sentiment-analysis", return_all_scores=True)
# emotion_analyzer = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", return_all_scores=True)
# formality_analyzer = pipeline("text-classification", model="s-nlp/roberta-base-formality-ranker", return_all_scores=True)
# toxicity_analyzer = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)
# empathy_analyzer = pipeline("text-classification", model="michellejieli/emotion_text_classifier", return_all_scores=True)

# def get_top_label(results):
#     """Helper to get the highest confidence label from results"""
#     return max(results, key=lambda x: x['score'])

# def analyze_metrics(text):
#     # Initialize testing metrics collection
#     testing_metrics = {
#         "model_versions": {},
#         "inference_times": {},
#         "confidence_breakdown": {},
#         "text_statistics": {}
#     }
    
#     # Text statistics
#     testing_metrics["text_statistics"] = {
#         "text_length": len(text),
#         "word_count": len(text.split()),
#         "estimated_tokens": len(sentiment_analyzer.tokenizer.tokenize(text))
#     }

#     # Sentiment analysis
#     start = time.time()
#     sentiment_results = sentiment_analyzer(text)[0]
#     testing_metrics["inference_times"]["sentiment"] = time.time() - start
#     sentiment_top = get_top_label(sentiment_results)
#     testing_metrics["confidence_breakdown"]["sentiment"] = sentiment_results
#     testing_metrics["model_versions"]["sentiment"] = sentiment_analyzer.model.config._name_or_path

#     # Emotion analysis
#     start = time.time()
#     emotion_results = emotion_analyzer(text)[0]
#     testing_metrics["inference_times"]["emotion"] = time.time() - start
#     emotion_top = get_top_label(emotion_results)
#     testing_metrics["confidence_breakdown"]["emotion"] = emotion_results
#     testing_metrics["model_versions"]["emotion"] = emotion_analyzer.model.config._name_or_path

#     # Formality analysis
#     start = time.time()
#     formality_results = formality_analyzer(text)[0]
#     testing_metrics["inference_times"]["formality"] = time.time() - start
#     formality_top = get_top_label(formality_results)
#     formality_score = formality_top['score'] if formality_top['label'] == 'formal' else 1 - formality_top['score']
#     testing_metrics["confidence_breakdown"]["formality"] = formality_results
#     testing_metrics["model_versions"]["formality"] = formality_analyzer.model.config._name_or_path

#     # Toxicity analysis
#     start = time.time()
#     toxicity_results = toxicity_analyzer(text)[0]
#     testing_metrics["inference_times"]["toxicity"] = time.time() - start
#     toxicity_score = max(item['score'] for item in toxicity_results)
#     testing_metrics["confidence_breakdown"]["toxicity"] = toxicity_results
#     testing_metrics["model_versions"]["toxicity"] = toxicity_analyzer.model.config._name_or_path

#     # Empathy analysis (Note: Verify model labels match your use case)
#     start = time.time()
#     empathy_results = empathy_analyzer(text)[0]
#     testing_metrics["inference_times"]["empathy"] = time.time() - start
#     empathy_top = get_top_label(empathy_results)
#     empathy_score = empathy_top['score'] if empathy_top['label'] == 'empathy' else 1 - empathy_top['score']
#     testing_metrics["confidence_breakdown"]["empathy"] = empathy_results
#     testing_metrics["model_versions"]["empathy"] = empathy_analyzer.model.config._name_or_path

#     return {
#         "social_awareness": formality_score,
#         "communication_style": empathy_score,
#         "emotional_tone": {
#             "primary_emotion": emotion_top['label'],
#             "emotion_confidence": emotion_top['score'],
#             "sentiment": sentiment_top['label'],
#             "sentiment_score": sentiment_top['score']
#         },
#         "confidence_score": 1 - toxicity_score,
#         "positivity_ratio": sentiment_top['score'] if sentiment_top['label'] == 'POSITIVE' else 1 - sentiment_top['score'],
#         "toxicity_risk": toxicity_score,
#         "emotional_intelligence": empathy_score * formality_score,
#         "testing_metrics": testing_metrics
#     }

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.get_json()
#         text = data.get('text', '')
        
#         if not text:
#             return jsonify({"error": "No text provided"}), 400
        
#         metrics = analyze_metrics(text)
#         return jsonify(metrics)
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

# #test blurbs

# #"Hello, my name is Bob, and I’m a passionate AI researcher and developer with a strong background in machine learning, NLP, and data-driven solutions. I thrive on solving complex problems, whether it’s optimizing financial models, enhancing AI-driven applications, or developing intuitive tools that bridge the gap between research and real-world impact. My experience spans academia, industry, and mentorship, where I’ve had the privilege of guiding others while continuously learning myself. I believe in the power of innovation, collaboration, and thoughtful execution to push boundaries in AI and data science. If you’re excited about cutting-edge AI, let’s connect and build something incredible together!"

# #"Hey... I guess I should introduce myself. I’m Joe, and honestly, I don’t know why I’m even doing this. I work with AI and machine learning, but half the time, it feels like I’m just throwing data at models and hoping for the best. Sure, I’ve done some cool projects, but nothing ever seems good enough. The tech world moves too fast, and everyone else seems miles ahead. Anyway, if you want to talk about AI, trading, or whatever, I guess I’m around. Just don’t expect me to be the one who has all the answers."
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

# We won't use an additional model for personality analysis
# Instead, we'll use existing models and text statistics for complexity assessment

def get_top_label(results):
    """Helper to get the highest confidence label from results"""
    return max(results, key=lambda x: x['score'])

def check_text_complexity(text):
    """
    Check if the text has sufficient complexity based on various linguistic metrics
    Returns a dictionary with complexity assessment
    """
    import re
    import string
    from collections import Counter
    
    # Get basic text statistics
    words = text.split()
    
    stats = {
        "text_length": len(text),
        "word_count": len(words),
        "estimated_tokens": len(sentiment_analyzer.tokenizer.tokenize(text))
    }
    
    # Text is too short - quick rejection
    if stats["word_count"] < 15:
        return {
            "complex_enough": False,
            "reason": "Text is too short (minimum 15 words required)",
            "complexity_score": 0.0,
            "stats": stats
        }
    
    # Calculate additional metrics for complexity
    
    # 1. Lexical diversity (unique words ratio)
    unique_words = len(set([w.lower() for w in words]))
    lexical_diversity = unique_words / stats["word_count"] if stats["word_count"] > 0 else 0
    
    # 2. Average word length
    avg_word_length = sum(len(word) for word in words) / stats["word_count"] if stats["word_count"] > 0 else 0
    
    # 3. Personal pronouns (indicates self-disclosure)
    personal_pronouns = ['i', 'me', 'my', 'mine', 'myself']
    personal_pronoun_count = sum(1 for word in words if word.lower() in personal_pronouns)
    personal_pronoun_ratio = personal_pronoun_count / stats["word_count"] if stats["word_count"] > 0 else 0
    
    # 4. Emotional content analysis using existing model
    emotion_results = emotion_analyzer(text)[0]
    emotion_scores = {item['label']: item['score'] for item in emotion_results}
    emotion_diversity = sum(score for label, score in emotion_scores.items() if score > 0.1)
    
    # 5. Sentence complexity: average sentence length
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    # Normalize all factors to 0-1 range
    len_factor = min(stats["word_count"] / 50, 1.0)  # Cap at 50 words
    diversity_factor = min(lexical_diversity * 2.5, 1.0)  # Typically 0.4-0.7 is good
    word_length_factor = min((avg_word_length - 3) / 3, 1.0)  # 3-6 letter words
    pronoun_factor = min(personal_pronoun_ratio * 10, 1.0)  # Personal content
    emotion_factor = min(emotion_diversity * 2, 1.0)  # Emotional range
    sentence_factor = min(avg_sentence_length / 15, 1.0)  # Sentence complexity
    
    # Combine factors with weights to get complexity score
    complexity_score = (
        0.25 * len_factor +             # Length matters
        0.20 * diversity_factor +       # Vocabulary diversity
        0.10 * word_length_factor +     # Word sophistication
        0.25 * pronoun_factor +         # Personal disclosure (important)
        0.15 * emotion_factor +         # Emotional range
        0.05 * sentence_factor          # Sentence structure
    )
    
    # Ensure score is in 0-1 range
    complexity_score = max(0.0, min(1.0, complexity_score))
    
    # Check if it meets threshold
    threshold = 0.55  # Slightly lower than before since this is more rigorous
    complex_enough = complexity_score >= threshold
    
    # Generate explanation
    if complex_enough:
        reason = "Text has sufficient complexity for analysis"
    else:
        if len_factor < 0.5:
            reason = f"Text is too brief (score: {complexity_score:.2f}, minimum: {threshold})"
        elif pronoun_factor < 0.3:
            reason = f"Text lacks personal context (score: {complexity_score:.2f}, minimum: {threshold})"
        elif diversity_factor < 0.3:
            reason = f"Text vocabulary is too limited (score: {complexity_score:.2f}, minimum: {threshold})"
        elif emotion_factor < 0.3:
            reason = f"Text lacks emotional depth (score: {complexity_score:.2f}, minimum: {threshold})"
        else:
            reason = f"Text lacks overall complexity (score: {complexity_score:.2f}, minimum: {threshold})"
    
    # Get primary emotion for feedback
    top_emotion = get_top_label(emotion_results)
    
    return {
        "complex_enough": complex_enough,
        "reason": reason,
        "complexity_score": complexity_score,
        "primary_emotion": top_emotion['label'],
        "emotion_confidence": top_emotion['score'],
        "stats": stats,
        "detailed_metrics": {
            "length_score": len_factor,
            "vocabulary_diversity": diversity_factor,
            "word_sophistication": word_length_factor,
            "personal_disclosure": pronoun_factor,
            "emotional_range": emotion_factor,
            "sentence_complexity": sentence_factor
        }
    }

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

    # Empathy analysis
    start = time.time()
    empathy_results = empathy_analyzer(text)[0]
    testing_metrics["inference_times"]["empathy"] = time.time() - start
    empathy_top = get_top_label(empathy_results)
    empathy_score = empathy_top['score'] if empathy_top['label'] == 'empathy' else 1 - empathy_top['score']
    testing_metrics["confidence_breakdown"]["empathy"] = empathy_results
    testing_metrics["model_versions"]["empathy"] = empathy_analyzer.model.config._name_or_path
    
    # We don't need to add personality analysis since we're using the existing models

    return {
        "social_awareness": formality_score,
        "communication_style": empathy_score,
        "emotional_tone": {
            "primary_emotion": emotion_top['label'],
            "emotion_confidence": emotion_top['score'],
            "sentiment": sentiment_top['label'],
            "sentiment_score": sentiment_top['score']
        },
        # Removed personality type
        "confidence_score": 1 - toxicity_score,
        "positivity_ratio": sentiment_top['score'] if sentiment_top['label'] == 'POSITIVE' else 1 - sentiment_top['score'],
        "toxicity_risk": toxicity_score,
        "emotional_intelligence": empathy_score * formality_score,
        "testing_metrics": testing_metrics
    }

@app.route('/check-complexity', methods=['POST'])
def check_complexity():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        complexity_assessment = check_text_complexity(text)
        return jsonify(complexity_assessment)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # First check complexity
        complexity_assessment = check_text_complexity(text)
        
        # If text isn't complex enough, return the assessment without full analysis
        if not complexity_assessment["complex_enough"]:
            return jsonify({
                "error": "Text complexity check failed",
                "complexity_assessment": complexity_assessment
            }), 400
        
        # Text passed complexity check, do full analysis
        metrics = analyze_metrics(text)
        
        # Include complexity assessment in the response
        metrics["complexity_assessment"] = complexity_assessment
        
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)