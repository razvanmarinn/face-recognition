
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class JWTHandler {


    public static String getTempJWTToken(int user_id) {
        String baseUrl = "http://127.0.0.1:8001/login/temp_jwt/";
        String jwtToken = null;

        try {
            URL url = new URL(baseUrl + user_id);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            reader.close();

            jwtToken = response.toString();

            jwtToken = jwtToken.substring(1, jwtToken.length() - 1);

            connection.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jwtToken;
    }


}
