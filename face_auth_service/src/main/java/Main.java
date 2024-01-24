import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.codec.binary.Base64;
import org.apache.http.HttpHeaders;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static helpers.ConfidenceLevelHelper.parseConfidenceLevel;

public class Main {
    public static void main(String[] args) {

        KafkaImageConsumer _kafkaImageConsumer = new KafkaImageConsumer();
        KafkaResponseProducer _kafkaResponseProducer = new KafkaResponseProducer();
        HttpClient httpClient = HttpClients.createDefault();

        String apiUrl = System.getenv("API_URL");
        Map<String, Double> userConfidenceSum = new HashMap<>();

        System.out.println("Started listening");
        while (true) {
            ConsumerRecords<String, byte[]> records = _kafkaImageConsumer._consumer.poll(Duration.ofMillis(100));
            for (ConsumerRecord<String, byte[]> record : records) {
                byte[] serializedImageList = record.value();
                String userId = record.key();
                String jwtToken = JWTHandler.getTempJWTToken(Integer.parseInt(userId));
                ObjectMapper mapper = new ObjectMapper();
                try {
                    JsonNode userDataNode = mapper.readTree(serializedImageList);
                    List<String> imageList = mapper.convertValue(userDataNode.get("images"), new TypeReference<List<String>>() {
                    });

                    for (int i = 0; i < imageList.size(); i++) {
                        byte[] imageBytes = Base64.decodeBase64(imageList.get(i));

                        System.out.println("Received image data with size: " + imageBytes.length + " bytes for user: " + userId);

                        String imageFileName = "kafka_image_" + userId + "_" + i + ".jpg";

                        printToDesktop(imageBytes, imageFileName);

                        MultipartEntityBuilder entityBuilder = MultipartEntityBuilder.create();
                        entityBuilder.addTextBody("user_id", userId, ContentType.TEXT_PLAIN);
                        entityBuilder.addBinaryBody("image", imageBytes, ContentType.APPLICATION_OCTET_STREAM, imageFileName);
                        entityBuilder.addTextBody("default_face_auth", "true", ContentType.TEXT_PLAIN);


                        HttpPost request = new HttpPost(apiUrl);

                        request.addHeader(HttpHeaders.AUTHORIZATION, "Bearer " + jwtToken);
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

                        if (i == 5) {
                            double averageConfidence = userConfidenceSum.get(userId) / 6;
                            if (averageConfidence > 70.0) {
                                _kafkaResponseProducer.sendMessage("face_auth_response", userId, "1".getBytes(StandardCharsets.UTF_8));
                                System.out.println("Added to new hashmap for user " + userId + " : " + averageConfidence);
                            }
                            userConfidenceSum.put(userId, 0.0);
                        }
                        _kafkaImageConsumer._consumer.commitSync();
                    }

                } catch (Exception e) {
                    throw new RuntimeException(e);
                }

            }
        }
    }

    private static void printToDesktop(byte[] imageBytes, String imageFileName) {
        String desktopPath = System.getProperty("user.home") + File.separator + "Desktop";

        try (FileOutputStream fos = new FileOutputStream(Paths.get(desktopPath, imageFileName).toString())) {
            fos.write(imageBytes);
            fos.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
