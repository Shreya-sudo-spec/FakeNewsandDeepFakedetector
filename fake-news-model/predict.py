import joblib

# Load the trained model and TF-IDF vectorizer
model = joblib.load("fake-news-model/fake_news_model.pkl")
vectorizer = joblib.load("fake-news-model/tfidf_vectorizer.pkl")

# Get news from the user
title = input("Enter the news title: ")
text = input("Enter the news article: ")

# Combine title and article
content = title + " " + text
if len(content.split()) < 20:
    print("\nPlease enter a complete news article.")
    print("The article should contain at least 20 words.")
    exit()

# Convert text into TF-IDF features
content_tfidf = vectorizer.transform([content])

# Make prediction
prediction = model.predict(content_tfidf)[0]

# Get prediction probability
probabilities = model.predict_proba(content_tfidf)[0]
confidence = max(probabilities) * 100

# Display result
if prediction == 1:
    result = "REAL"
else:
    result = "FAKE"

print("\nPrediction:", result)
print("Confidence: {:.2f}%".format(confidence))