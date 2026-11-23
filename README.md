# ToxiSense AI — Cyber Safety Intelligence

**Developed by Shreya Agarwal**  
An educational cyberbullying / harmful-language detection prototype with a cyber-themed dashboard and safety guidance. No login or signup.

## Features
- Real Flask API connected to the included TF-IDF + Logistic Regression model (not a random/demo result).
- Harmful-language signal with model confidence.
- Separate, transparent phrase checks for a small set of possible threat and harassment phrases. These checks are limited and are not a complete threat detector.
- Context-sensitive next steps when a possible direct-threat phrase is detected.
- India safety contacts: Emergency 112, Child Helpline 1098, and the National Cyber Crime Reporting Portal. 1930 is identified only for financial cyber fraud.
- Responsive dark cyber dashboard, quick sample messages, model limitations and privacy notice.
- Submitted message text is not stored by this app.

## Model facts and limitations
The classifier was trained on the supplied English-language dataset (47,692 rows) and is binary: likely safe vs potentially harmful. Held-out test metrics from the earlier training run are in `metrics.json` (accuracy 81.11%, precision 96.69%, recall 80.08%, F1 87.60%). These metrics describe that dataset split only; they do not guarantee real-world accuracy. Hindi/Hinglish, slang, sarcasm, context and new forms of abuse may be misclassified. The separate phrase checks cover only a small set of English and Hindi threat/harassment expressions. A missing alert does not mean a message is safe. Confidence is not correctness.

This is a school demonstration, not a real-time monitoring, emergency response or professional risk-assessment system. Never use it to automatically punish, label or make disciplinary decisions about a student. Do not paste real private conversations, names, phone numbers, school details or other identifying information.

## Run locally (Termux / Linux / Windows)
1. Extract the ZIP. Open the `ToxiSense-AI` folder in Termux.
2. Install Python and packages:
   ```bash
   pkg update && pkg upgrade -y
   pkg install python -y
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser. Keep Termux open while using it.

On some Android/Termux versions, scientific Python packages may not have compatible wheels. If installation fails, deploy using the cloud steps below instead.

## Deploy to Render
1. Upload the **contents** of this folder to the root of a GitHub repository. `app.py`, `model.pkl`, `requirements.txt`, `templates/`, and `static/` must be at repository root.
2. In Render, create a Web Service and connect the repository.
3. Use Python 3.11 if a Python version setting is requested.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy, then check `/health` and try the homepage.

Free hosting may sleep or change limits; do not promise uninterrupted availability. Never commit API keys or personal data. This app does not need an API key.

## Help and safety (India)
- **112** — emergency response. If danger is immediate, move to a safer place with trusted people and call 112.
- **1098** — Child Helpline for children in distress.
- **cybercrime.gov.in** — official National Cyber Crime Reporting Portal.
- **1930** — mainly for financial cyber-fraud assistance; it is not presented as a dedicated cyberbullying helpline.

If someone makes a serious threat: do not meet or confront them; tell a parent/guardian/teacher or trusted adult; preserve screenshots, account/profile links, usernames and dates; report the account/content on its platform; and use the official portal or emergency service as appropriate.

## Source and attribution
The included classifier and dataset are carried forward from the source project provided for this school demonstration. See `ORIGINAL_LICENSE.txt` for the original repository license note. Government contact information should be rechecked before public/production use.

devloped by sumit 
