from flask import Flask, render_template, request, jsonify
import joblib
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "fake_news_model.pkl")

app = Flask(__name__)

model = joblib.load(MODEL_PATH)

def clean_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or request.form
    news_text = clean_text(data.get("news_text", ""))

    if len(news_text) < 20:
        response = {
            "error": "Please enter a longer news article or headline."
        }
        if request.is_json:
            return jsonify(response), 400
        return render_template("index.html", error=response["error"], news_text=news_text)

    prediction = model.predict([news_text])[0]
    probabilities = model.predict_proba([news_text])[0]
    classes = list(model.classes_)
    confidence = float(max(probabilities) * 100)

    result = {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "fake_probability": round(float(probabilities[classes.index("FAKE")] * 100), 2),
        "real_probability": round(float(probabilities[classes.index("REAL")] * 100), 2)
    }

    if request.is_json:
        return jsonify(result)

    return render_template("index.html", result=result, news_text=news_text)

@app.route("/health")
def health():
    return jsonify({"status": "running", "database": "not used"})

if __name__ == "__main__":
    app.run(debug=True)
