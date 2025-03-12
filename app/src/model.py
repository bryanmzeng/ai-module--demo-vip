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

# # We won't use an additional model for personality analysis
# # Instead, we'll use existing models and text statistics for complexity assessment

# def get_top_label(results):
#     """Helper to get the highest confidence label from results"""
#     return max(results, key=lambda x: x['score'])

# def check_text_complexity(text):
#     """
#     Check if the text has sufficient complexity based on various linguistic metrics
#     Returns a dictionary with complexity assessment
#     """
#     import re
#     import string
#     from collections import Counter
    
#     # Get basic text statistics
#     words = text.split()
    
#     stats = {
#         "text_length": len(text),
#         "word_count": len(words),
#         "estimated_tokens": len(sentiment_analyzer.tokenizer.tokenize(text))
#     }
    
#     # Text is too short - quick rejection
#     if stats["word_count"] < 15:
#         return {
#             "complex_enough": False,
#             "reason": "Text is too short (minimum 15 words required)",
#             "complexity_score": 0.0,
#             "stats": stats
#         }
    
#     # Calculate additional metrics for complexity
    
#     # 1. Lexical diversity (unique words ratio)
#     unique_words = len(set([w.lower() for w in words]))
#     lexical_diversity = unique_words / stats["word_count"] if stats["word_count"] > 0 else 0
    
#     # 2. Average word length
#     avg_word_length = sum(len(word) for word in words) / stats["word_count"] if stats["word_count"] > 0 else 0
    
#     # 3. Personal pronouns (indicates self-disclosure)
#     personal_pronouns = ['i', 'me', 'my', 'mine', 'myself']
#     personal_pronoun_count = sum(1 for word in words if word.lower() in personal_pronouns)
#     personal_pronoun_ratio = personal_pronoun_count / stats["word_count"] if stats["word_count"] > 0 else 0
    
#     # 4. Emotional content analysis using existing model
#     emotion_results = emotion_analyzer(text)[0]
#     emotion_scores = {item['label']: item['score'] for item in emotion_results}
#     emotion_diversity = sum(score for label, score in emotion_scores.items() if score > 0.1)
    
#     # 5. Sentence complexity: average sentence length
#     sentences = re.split(r'[.!?]+', text)
#     sentences = [s.strip() for s in sentences if s.strip()]
#     avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
#     # Normalize all factors to 0-1 range
#     len_factor = min(stats["word_count"] / 50, 1.0)  # Cap at 50 words
#     diversity_factor = min(lexical_diversity * 2.5, 1.0)  # Typically 0.4-0.7 is good
#     word_length_factor = min((avg_word_length - 3) / 3, 1.0)  # 3-6 letter words
#     pronoun_factor = min(personal_pronoun_ratio * 10, 1.0)  # Personal content
#     emotion_factor = min(emotion_diversity * 2, 1.0)  # Emotional range
#     sentence_factor = min(avg_sentence_length / 15, 1.0)  # Sentence complexity
    
#     # Combine factors with weights to get complexity score
#     complexity_score = (
#         0.25 * len_factor +             # Length matters
#         0.20 * diversity_factor +       # Vocabulary diversity
#         0.10 * word_length_factor +     # Word sophistication
#         0.25 * pronoun_factor +         # Personal disclosure (important)
#         0.15 * emotion_factor +         # Emotional range
#         0.05 * sentence_factor          # Sentence structure
#     )
    
#     # Ensure score is in 0-1 range
#     complexity_score = max(0.0, min(1.0, complexity_score))
    
#     # Check if it meets threshold
#     threshold = 0.55  # Slightly lower than before since this is more rigorous
#     complex_enough = complexity_score >= threshold
    
#     # Generate explanation
#     if complex_enough:
#         reason = "Text has sufficient complexity for analysis"
#     else:
#         if len_factor < 0.5:
#             reason = f"Text is too brief (score: {complexity_score:.2f}, minimum: {threshold})"
#         elif pronoun_factor < 0.3:
#             reason = f"Text lacks personal context (score: {complexity_score:.2f}, minimum: {threshold})"
#         elif diversity_factor < 0.3:
#             reason = f"Text vocabulary is too limited (score: {complexity_score:.2f}, minimum: {threshold})"
#         elif emotion_factor < 0.3:
#             reason = f"Text lacks emotional depth (score: {complexity_score:.2f}, minimum: {threshold})"
#         else:
#             reason = f"Text lacks overall complexity (score: {complexity_score:.2f}, minimum: {threshold})"
    
#     # Get primary emotion for feedback
#     top_emotion = get_top_label(emotion_results)
    
#     return {
#         "complex_enough": complex_enough,
#         "reason": reason,
#         "complexity_score": complexity_score,
#         "primary_emotion": top_emotion['label'],
#         "emotion_confidence": top_emotion['score'],
#         "stats": stats,
#         "detailed_metrics": {
#             "length_score": len_factor,
#             "vocabulary_diversity": diversity_factor,
#             "word_sophistication": word_length_factor,
#             "personal_disclosure": pronoun_factor,
#             "emotional_range": emotion_factor,
#             "sentence_complexity": sentence_factor
#         }
#     }

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

#     # Empathy analysis
#     start = time.time()
#     empathy_results = empathy_analyzer(text)[0]
#     testing_metrics["inference_times"]["empathy"] = time.time() - start
#     empathy_top = get_top_label(empathy_results)
#     empathy_score = empathy_top['score'] if empathy_top['label'] == 'empathy' else 1 - empathy_top['score']
#     testing_metrics["confidence_breakdown"]["empathy"] = empathy_results
#     testing_metrics["model_versions"]["empathy"] = empathy_analyzer.model.config._name_or_path
    
#     # We don't need to add personality analysis since we're using the existing models

#     return {
#         "social_awareness": formality_score,
#         "communication_style": empathy_score,
#         "emotional_tone": {
#             "primary_emotion": emotion_top['label'],
#             "emotion_confidence": emotion_top['score'],
#             "sentiment": sentiment_top['label'],
#             "sentiment_score": sentiment_top['score']
#         },
#         # Removed personality type
#         "confidence_score": 1 - toxicity_score,
#         "positivity_ratio": sentiment_top['score'] if sentiment_top['label'] == 'POSITIVE' else 1 - sentiment_top['score'],
#         "toxicity_risk": toxicity_score,
#         "emotional_intelligence": empathy_score * formality_score,
#         "testing_metrics": testing_metrics
#     }

# @app.route('/check-complexity', methods=['POST'])
# def check_complexity():
#     try:
#         data = request.get_json()
#         text = data.get('text', '')
        
#         if not text:
#             return jsonify({"error": "No text provided"}), 400
        
#         complexity_assessment = check_text_complexity(text)
#         return jsonify(complexity_assessment)
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.get_json()
#         text = data.get('text', '')
        
#         if not text:
#             return jsonify({"error": "No text provided"}), 400
        
#         # First check complexity
#         complexity_assessment = check_text_complexity(text)
        
#         # If text isn't complex enough, return the assessment without full analysis
#         if not complexity_assessment["complex_enough"]:
#             return jsonify({
#                 "error": "Text complexity check failed",
#                 "complexity_assessment": complexity_assessment
#             }), 400
        
#         # Text passed complexity check, do full analysis
#         metrics = analyze_metrics(text)
        
#         # Include complexity assessment in the response
#         metrics["complexity_assessment"] = complexity_assessment
        
#         return jsonify(metrics)
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

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

def predict_mbti(metrics, complexity_assessment):
    """
    Predict Myers-Briggs Type Indicator (MBTI) based on text analysis metrics
    
    Returns a dictionary with MBTI prediction, confidence scores, and dimension explanations
    """
    # Extract relevant metrics
    formality_score = metrics["social_awareness"]
    empathy_score = metrics["communication_style"]
    emotion_info = metrics["emotional_tone"]
    positivity = metrics["positivity_ratio"]
    toxicity = metrics["toxicity_risk"]
    
    # Extract text complexity metrics
    complexity = complexity_assessment["detailed_metrics"]
    personal_disclosure = complexity["personal_disclosure"]
    vocabulary_diversity = complexity["vocabulary_diversity"]
    sentence_complexity = complexity["sentence_complexity"]
    
    # Analyze primary emotion
    primary_emotion = emotion_info["primary_emotion"].lower()
    emotion_confidence = emotion_info["emotion_confidence"]
    is_emotional = primary_emotion in ["joy", "love", "sadness"] and emotion_confidence > 0.6
    is_logical = primary_emotion in ["neutral", "surprise"] or emotion_confidence < 0.4
    
    # 1. Extraversion (E) vs. Introversion (I)
    # Higher personal disclosure often correlates with extraversion
    # Higher positive emotions associated with extraversion
    # Higher formality often associated with introversion
    e_score = (
        personal_disclosure * 0.4 + 
        positivity * 0.3 + 
        (1 - formality_score) * 0.3
    )
    
    # 2. Sensing (S) vs. Intuition (N)
    # Higher vocabulary diversity and sentence complexity associated with intuition
    # Concrete language associated with sensing
    n_score = (
        vocabulary_diversity * 0.5 + 
        sentence_complexity * 0.3 + 
        complexity["word_sophistication"] * 0.2
    )
    
    # 3. Thinking (T) vs. Feeling (F)
    # Lower empathy associated with thinking
    # Emotional language associated with feeling
    f_score = (
        empathy_score * 0.5 + 
        (0.8 if is_emotional else 0.2) * 0.3 + 
        (1 - (0.8 if is_logical else 0.2)) * 0.2
    )
    
    # 4. Judging (J) vs. Perceiving (P)
    # Higher formality often associated with judging
    # Lower positivity ratio sometimes associated with judging
    # Structure and organization in language (sentence complexity)
    j_score = (
        formality_score * 0.5 + 
        (1 - positivity) * 0.2 + 
        sentence_complexity * 0.3
    )
    
    # Determine type based on scores
    mbti = ""
    mbti += "E" if e_score >= 0.5 else "I"
    mbti += "N" if n_score >= 0.5 else "S"
    mbti += "F" if f_score >= 0.5 else "T"
    mbti += "J" if j_score >= 0.5 else "P"
    
    # Calculate confidence scores for each dimension
    confidence = {
        "E-I": abs(e_score - 0.5) * 2,  # Convert 0-0.5 range to 0-1
        "N-S": abs(n_score - 0.5) * 2,
        "F-T": abs(f_score - 0.5) * 2,
        "J-P": abs(j_score - 0.5) * 2
    }
    
    # Calculate overall confidence (average of individual confidences)
    overall_confidence = sum(confidence.values()) / 4
    
    # Map types to their common descriptors
    type_descriptions = {
        "ISTJ": "The Inspector",
        "ISFJ": "The Protector",
        "INFJ": "The Counselor",
        "INTJ": "The Mastermind",
        "ISTP": "The Craftsman",
        "ISFP": "The Composer",
        "INFP": "The Healer",
        "INTP": "The Architect",
        "ESTP": "The Dynamo",
        "ESFP": "The Performer",
        "ENFP": "The Champion",
        "ENTP": "The Visionary",
        "ESTJ": "The Supervisor",
        "ESFJ": "The Provider",
        "ENFJ": "The Teacher",
        "ENTJ": "The Commander"
    }
    
    # Generate dimension explanations
    dimension_explanations = {
        "E-I": f"{'Extraversion' if e_score >= 0.5 else 'Introversion'} ({e_score*100:.0f}%): " + 
               (f"text suggests an outward energy focus and social engagement" 
                if e_score >= 0.5 else 
                f"text suggests a more reflective, internal focus"),
               
        "N-S": f"{'Intuition' if n_score >= 0.5 else 'Sensing'} ({n_score*100:.0f}%): " + 
               (f"text shows abstract thinking and pattern recognition" 
                if n_score >= 0.5 else 
                f"text demonstrates concrete, practical thinking"),
                
        "F-T": f"{'Feeling' if f_score >= 0.5 else 'Thinking'} ({f_score*100:.0f}%): " + 
               (f"text prioritizes emotional consideration and values" 
                if f_score >= 0.5 else 
                f"text emphasizes logical analysis and objectivity"),
                
        "J-P": f"{'Judging' if j_score >= 0.5 else 'Perceiving'} ({j_score*100:.0f}%): " + 
               (f"communication style suggests structure and decisiveness" 
                if j_score >= 0.5 else 
                f"communication style indicates flexibility and openness")
    }
    
    # Disclaimer about accuracy
    disclaimer = (
        "can use these above dimension scores as part of algo if needed"
    )
    
    return {
        "mbti_type": mbti,
        "type_name": type_descriptions.get(mbti, ""),
        "confidence": overall_confidence,
        "dimension_scores": {
            "extraversion_score": e_score,
            "intuition_score": n_score,
            "feeling_score": f_score,
            "judging_score": j_score
        },
        "dimension_confidence": confidence,
        "dimension_explanations": dimension_explanations,
        "disclaimer": disclaimer
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
        
        # Add personality prediction using metrics and complexity assessment
        personality_prediction = predict_mbti(metrics, complexity_assessment)
        metrics["personality"] = personality_prediction
        
        # Include complexity assessment in the response
        metrics["complexity_assessment"] = complexity_assessment
        
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a dedicated endpoint for just MBTI prediction
@app.route('/predict-mbti', methods=['POST'])
def predict_mbti_endpoint():
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
        
        # Generate personality prediction
        personality_prediction = predict_mbti(metrics, complexity_assessment)
        
        return jsonify({
            "personality": personality_prediction,
            "complexity_assessment": complexity_assessment
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)