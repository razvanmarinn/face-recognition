import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

public class Main {
    public static void main(String[] args) {
        KafkaImageConsumer _kafkaImageConsumer = new KafkaImageConsumer();
        KafkaResponseProducer _kafkaResponseProducer = new KafkaResponseProducer();
        HttpClient httpClient = HttpClients.createDefault();

        String apiUrl = "http://127.0.0.1:8000/face_recognition/recognize";
        String faceName = "Razvan";

        Map<String, Integer> userImageCount = new HashMap<>();

        Map<String, Double> userConfidenceSum = new HashMap<>();

        System.out.println("Started listening");
        while (true) {
            ConsumerRecords<String, byte[]> records = _kafkaImageConsumer._consumer.poll(Duration.ofMillis(100));

            for (ConsumerRecord<String, byte[]> record : records) {
                byte[] imageBytes = record.value();
                String jwtToken = record.key();
                String userId = JWTHandler.getUserIdFromJWT(jwtToken);
                System.out.println(userId);

                System.out.println("Received image data with size: " + imageBytes.length + " bytes for user: " + userId);

                int imageCount = userImageCount.getOrDefault(userId, 0);

                String desktopPath = System.getProperty("user.home") + File.separator + "Desktop";
                String imageFileName = "kafka_image_" + userId + "_" + imageCount + ".jpg";

                try (FileOutputStream fos = new FileOutputStream(Paths.get(desktopPath, imageFileName).toString())) {
                    fos.write(imageBytes);
                    fos.flush();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                MultipartEntityBuilder entityBuilder = MultipartEntityBuilder.create();
                entityBuilder.addBinaryBody("image", imageBytes, ContentType.APPLICATION_OCTET_STREAM, imageFileName);
                entityBuilder.addTextBody("face_name", faceName, ContentType.TEXT_PLAIN);
                entityBuilder.addTextBody("authorization", jwtToken, ContentType.TEXT_PLAIN);

                try {
                    HttpPost request = new HttpPost(apiUrl);
                    request.setEntity(entityBuilder.build());
                    HttpResponse response = httpClient.execute(request);
                    String responseContent = EntityUtils.toString(response.getEntity());
                    System.out.println(responseContent);

                    double confidenceLevel = parseConfidenceLevel(responseContent);

                    if (!userConfidenceSum.containsKey(userId)) {
                        userConfidenceSum.put(userId, 0.0);
                    }
                    double currentSum = userConfidenceSum.get(userId);
                    userConfidenceSum.put(userId, currentSum + confidenceLevel);
                    System.out.println("Updated confidence sum for user " + userId + ": " + userConfidenceSum.get(userId));

                    if (imageCount == 5) {
                        double averageConfidence = userConfidenceSum.get(userId) / 6;
                        if (averageConfidence > 60.0) {
                             _kafkaResponseProducer.sendMessage("face_auth_response", "11" , "success".getBytes(StandardCharsets.UTF_8));
                            System.out.println("Added to new hashmap for user " + userId + " : " + averageConfidence);
                        }
                        imageCount = 0;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                System.out.println("Received and saved an image from Kafka to the desktop for user: " + userId);

                userImageCount.put(userId, imageCount + 1);
            }
        }
    }

    private static double parseConfidenceLevel(String responseContent) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode jsonArray = objectMapper.readTree(responseContent);

            if (jsonArray.isArray() && jsonArray.size() > 0) {
                JsonNode firstElement = jsonArray.get(0);
                String confidenceString = firstElement.get("details").get("confidence_level").asText();
                confidenceString = confidenceString.substring(0, confidenceString.length() - 1);
                return Double.parseDouble(confidenceString);
            } else {
                return 0.0;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return 0.0;
        }
    }
}
