import os
import pickle
import re
from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
_model = None

# Transparent phrase checks are a small safety layer, not a complete threat detector.
THREAT_PATTERNS = [
    r"\b(i will|i'm going to|im going to|we will|you will)\s+(hurt|harm|attack|kill|beat)\s+(you|him|her|them)\b",
    r"\b(i know where you live|you won't be safe|you are dead|watch your back)\b",
    r"\b(jaan se maar|maar dunga|maar dungi|nuksan pahuchaunga|nuksan pahuchaungi)\b",
    r"\b(i will come to your house|i am coming for you)\b",
]
HARASSMENT_PATTERNS = [
    r"\b(you are worthless|you are a loser|nobody likes you|shut up)\b",
    r"\b(stupid|idiot|loser|worthless|pathetic)\b",
    r"\b(tum bekar ho|tu bekar hai|kisi ko tum pasand nahi)\b",
]


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("model.pkl missing")
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def phrase_signals(message):
    text = message.lower()
    threat = any(re.search(p, text, flags=re.IGNORECASE) for p in THREAT_PATTERNS)
    harassment = any(re.search(p, text, flags=re.IGNORECASE) for p in HARASSMENT_PATTERNS)
    signals = []
    if threat:
        signals.append("Possible direct-threat phrase")
    if harassment:
        signals.append("Possible insult / harassment phrase")
    return threat, harassment, signals


def safety_guidance(threat, harmful):
    if threat:
        return {
            "level": "high",
            "title": "Serious threat cue — get human help",
            "steps": [
                "Agar danger abhi ya real-world mein lag raha hai, safe jagah par jao aur India mein 112 par call karo.",
                "Parent, teacher, guardian ya kisi trusted adult ko turant batao; akele handle mat karo.",
                "Message, profile link, username aur time ke screenshots/evidence safe rakho; reply ya retaliation mat karo.",
                "Platform par report karo. Zaroorat par cybercrime.gov.in par complaint file karo.",
            ],
        }
    if harmful:
        return {
            "level": "review",
            "title": "Review recommended",
            "steps": [
                "Message ka context check karo; AI ka result final judgement nahi hai.",
                "Agar yeh tumhare saath ho raha hai, trusted adult/teacher ko batao.",
                "Repeated harassment ho to evidence save karke platform par report/block karo.",
            ],
        }
    return {
        "level": "low",
        "title": "No strong harmful-language signal",
        "steps": [
            "Model ko context, sarcasm aur Hindi/Hinglish samajhne mein galti ho sakti hai.",
            "Agar tum uncomfortable ya unsafe feel karte ho, trusted adult se baat karo.",
        ],
    }


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_file_present": os.path.exists(MODEL_PATH), "app": "ToxiSense AI"})


@app.get("/api/info")
def info():
    try:
        with open(os.path.join(BASE_DIR, "metrics.json"), encoding="utf-8") as f:
            metrics = json.load(f)
    except Exception:
        metrics = {}
    return jsonify({"metrics": metrics, "model_language": "English training data", "stores_text": False})


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    message = str(data.get("text", "")).strip()
    if not message:
        return jsonify({"error": "Pehle ek message likhein."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Message 1000 characters se chhota rakhein."}), 400

    try:
        model = get_model()
        prediction = int(model.predict([message])[0])
        harmful = prediction == 1
        confidence = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([message])[0]
            classes = list(model.classes_)
            confidence = round(float(probs[classes.index(prediction)]) * 100, 1)
        threat, harassment, signals = phrase_signals(message)
        guidance = safety_guidance(threat, harmful or harassment)
        if not signals and harmful:
            signals.append("ML model flagged potentially harmful language")
        return jsonify({
            "label": "potentially_harmful" if harmful else "likely_safe",
            "result": "Potentially harmful language — review context" if harmful else "No strong harmful-language signal found",
            "confidence": confidence,
            "signals": signals,
            "threat_detected": threat,
            "harassment_detected": harassment,
            "risk": guidance,
            "note": "English social-media dataset par trained model ka estimate hai. Hindi/Hinglish, sarcasm aur context mein galti ho sakti hai. Confidence correctness ki guarantee nahi hai.",
            "privacy": "Submitted text is not saved by this demo.",
        })
    except Exception:
        app.logger.exception("Analysis failed")
        return jsonify({"error": "Analysis complete nahi ho paayi. Server configuration check karein."}), 500


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Message bahut lamba hai."}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
