from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector
import json

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotionDetector():
    # uzmi tekst iz POST JSON zahteva
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # pozovi funkciju iz paketa
    result_json = emotion_detector(text)
    
    try:
        result_dict = json.loads(result_json)
    except Exception as e:
        return jsonify({"error": "Failed to process result"}), 500
    
    # odredi dominantnu emociju
    dominant_emotion = max(result_dict, key=result_dict.get)
    result_dict["dominant_emotion"] = dominant_emotion
    
    # vratimo response kao JSON
    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {result_dict.get('anger',0)}, "
        f"'disgust': {result_dict.get('disgust',0)}, "
        f"'fear': {result_dict.get('fear',0)}, "
        f"'joy': {result_dict.get('joy',0)}, "
        f"and 'sadness': {result_dict.get('sadness',0)}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    
    return jsonify({"result": response_str, "details": result_dict})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)