const analyzeButton = document.getElementById("analyzeButton");

const titleInput = document.getElementById("title");
const articleInput = document.getElementById("article");

const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction");
const confidenceText = document.getElementById("confidence");

const newsMode = document.getElementById("newsMode");
const mediaMode = document.getElementById("mediaMode");

const newsSection = document.getElementById("newsSection");
const mediaSection = document.getElementById("mediaSection");


// Analyze news article
analyzeButton.addEventListener("click", async () => {

    const title = titleInput.value.trim();
    const article = articleInput.value.trim();

    if (!title || !article) {
        alert("Please enter both a title and an article.");
        return;
    }

    if ((title + " " + article).split(/\s+/).length < 20) {
        alert("Please enter a complete news article with at least 20 words.");
        return;
    }

    analyzeButton.textContent = "Analyzing...";
    analyzeButton.disabled = true;

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                text: article
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        resultBox.classList.remove("hidden");
if (data.prediction === "REAL") {
    predictionText.textContent = "🟢 LIKELY REAL";
    resultBox.style.border = "2px solid #16a34a";
} else {
    predictionText.textContent = "🔴 LIKELY FAKE";
    resultBox.style.border = "2px solid #dc2626";
}

confidenceText.textContent =
    "Confidence: " + data.confidence + "%";

    } catch (error) {

        alert(
            "Could not connect to the AI server.\n\n" +
            "Make sure the Flask backend is running."
        );

    } finally {

        analyzeButton.textContent = "🔍 Analyze Article";
        analyzeButton.disabled = false;
    }
});


// Fake News mode
newsMode.addEventListener("click", () => {

    newsMode.classList.add("active");
    mediaMode.classList.remove("active");

    newsSection.classList.remove("hidden");
    mediaSection.classList.add("hidden");
});


// Deepfake mode
mediaMode.addEventListener("click", () => {

    mediaMode.classList.add("active");
    newsMode.classList.remove("active");

    mediaSection.classList.remove("hidden");
    newsSection.classList.add("hidden");
});