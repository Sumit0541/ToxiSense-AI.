import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("cyberbullying_tweets.csv", encoding="latin1", on_bad_lines="skip")
df = df.dropna(subset=["tweet_text", "cyberbullying_type"]).copy()
df["tweet_text"] = df["tweet_text"].astype(str).str.strip()
df = df[df["tweet_text"].str.len() > 0]
df["label"] = (df["cyberbullying_type"] != "not_cyberbullying").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df["tweet_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=12000,
                              ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print("Precision:", precision_score(y_test, pred, zero_division=0))
print("Recall:", recall_score(y_test, pred, zero_division=0))
print("F1:", f1_score(y_test, pred, zero_division=0))
with open("model.pkl", "wb") as f:
    pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
print("Saved model.pkl")
