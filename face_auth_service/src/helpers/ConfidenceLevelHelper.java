package helpers;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ConfidenceLevelHelper {

    public static double parseConfidenceLevel(String responseContent) {
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
