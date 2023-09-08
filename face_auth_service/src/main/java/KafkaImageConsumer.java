import org.apache.kafka.clients.consumer.*;

import java.time.Duration;
import java.util.Collections;
import java.util.HashMap;
import java.util.Properties;
import java.io.*;


public class KafkaImageConsumer {
    private Properties properties;
    public KafkaConsumer<String, byte[]> _consumer;
    private String consumeTopic = "test";

    public void setProperties() {
        this.properties = new Properties();
        properties.put("bootstrap.servers", "localhost:9092");
        properties.put("group.id", "tests");
        properties.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        properties.put("value.deserializer", "org.apache.kafka.common.serialization.ByteArrayDeserializer");
    }

    public KafkaImageConsumer() {
        setProperties();
        this._consumer = new KafkaConsumer<>(this.properties);
        this._consumer.subscribe(Collections.singletonList(consumeTopic));
    }

}


