import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Load datasets
true_news = pd.read_csv("data/True.csv")
fake_news = pd.read_csv("data/Fake.csv")

# Add labels
true_news["label"] = 1
fake_news["label"] = 0

# Combine datasets
data = pd.concat([true_news, fake_news], ignore_index=True)

# Keep required columns
data = data[["title", "text", "label"]]

# Remove missing values
data = data.dropna()

# Combine title and article text
data["content"] = data["title"] + " " + data["text"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    data["content"],
    data["label"],
    test_size=0.2,
    random_state=42,
    stratify=data["label"]
)
# Convert text into numerical features
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Training features:", X_train_tfidf.shape)
print("Testing features:", X_test_tfidf.shape)

print("Total articles:", len(data))
print("Training articles:", len(X_train))
print("Testing articles:", len(X_test))
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Create the model
model = LogisticRegression(max_iter=1000)

# Train the model
model.fit(X_train_tfidf, y_train)

# Make predictions on test data
y_pred = model.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel accuracy:", accuracy)
print("Model accuracy percentage:", accuracy * 100, "%")
from sklearn.metrics import classification_report, confusion_matrix

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["FAKE", "REAL"]
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
import joblib

joblib.dump(model, "fake-news-model/fake_news_model.pkl")
joblib.dump(vectorizer, "fake-news-model/tfidf_vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")