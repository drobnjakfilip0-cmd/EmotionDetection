from flask import Flask, request
from EmotionDetection.emotion_detection import emotion_detector
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Emotion Detection API is running!"

@app.route("/emotionDetector")
def emotion_detector_route():
    text = request.args.get('text')

    # call emotion detector
    response = emotion_detector(text)
    response_dict = json.loads(response)

    # EXACT blank input handling
    if response_dict['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    # formatted output
    result = (
        f"For the given statement, the system response is "
        f"'anger': {response_dict['anger']}, "
        f"'disgust': {response_dict['disgust']}, "
        f"'fear': {response_dict['fear']}, "
        f"'joy': {response_dict['joy']}, "
        f"and 'sadness': {response_dict['sadness']}. "
        f"The dominant emotion is {response_dict['dominant_emotion']}."
    )

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
