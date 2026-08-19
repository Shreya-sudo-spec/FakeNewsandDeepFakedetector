from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load the trained model and TF-IDF vectorizer
model = joblib.load("models/fake_news_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    title = data.get("title", "")
    text = data.get("text", "")

    content = title + " " + text

    # Check for very short input
    if len(content.split()) < 20:
        return jsonify({
            "error": "Please provide a complete news article."
        }), 400

    # Convert text to TF-IDF
    content_tfidf = vectorizer.transform([content])

    # Predict
    prediction = model.predict(content_tfidf)[0]

    # Get probability
    probabilities = model.predict_proba(content_tfidf)[0]
    confidence = max(probabilities) * 100

    if prediction == 1:
        result = "REAL"
    else:
        result = "FAKE"

    return jsonify({
        "prediction": result,
        "confidence": round(confidence, 2)
    })


if __name__ == "__main__":
    app.run(port=5000)