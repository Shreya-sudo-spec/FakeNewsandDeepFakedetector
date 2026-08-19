import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws Exception {

        Scanner scanner = new Scanner(System.in);

        System.out.println("================================");
        System.out.println("       FAKE NEWS DETECTOR");
        System.out.println("================================");

        System.out.print("\nEnter news title: ");
        String title = scanner.nextLine();

        System.out.print("Enter news article: ");
        String text = scanner.nextLine();

        if ((title + " " + text).trim().split("\\s+").length < 20) {
            System.out.println("\nPlease enter a complete news article.");
            System.out.println("The article should contain at least 20 words.");
            return;
        }

        String json = """
                {
                    "title": "%s",
                    "text": "%s"
                }
                """.formatted(
                        title.replace("\"", "\\\""),
                        text.replace("\"", "\\\"")
                );

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:5000/predict"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        System.out.println("\nAnalyzing...");

        HttpResponse<String> response =
                client.send(request, HttpResponse.BodyHandlers.ofString());

       String result = response.body();

if (result.contains("\"prediction\":\"REAL\"")) {
    System.out.println("\nRESULT: 🟢 LIKELY REAL");
} else if (result.contains("\"prediction\":\"FAKE\"")) {
    System.out.println("\nRESULT: 🔴 LIKELY FAKE");
} else {
    System.out.println("\nRESULT: Unable to analyze");
}

int confidenceStart = result.indexOf("\"confidence\":") + 13;
int confidenceEnd = result.indexOf("}", confidenceStart);

if (confidenceStart > 12 && confidenceEnd > confidenceStart) {
    String confidence = result.substring(confidenceStart, confidenceEnd);

    System.out.println("CONFIDENCE: " + confidence + "%");
}

System.out.println("\n================================");

        scanner.close();
    }
}
