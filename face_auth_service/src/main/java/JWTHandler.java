import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Base64;

public class JWTHandler {
    public static String getUserIdFromJWT(String token){
        try {
            Base64.Decoder decoder = Base64.getUrlDecoder();
            String[] splitToken = token.split("\\.");
            String header = new String(decoder.decode(splitToken[0]));
            String payload = new String(decoder.decode(splitToken[1]));

            ObjectMapper objectMapper = new ObjectMapper();

            JsonNode jsonNode = objectMapper.readTree(payload);

            String userId = String.valueOf(jsonNode.get("user_id"));

            return userId;
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    };
}
