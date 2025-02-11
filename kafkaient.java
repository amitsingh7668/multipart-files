import org.apache.kafka.clients.admin.*;
import java.util.*;
import java.util.concurrent.ExecutionException;

public class KafkaTopicPurger {

    public static void main(String[] args) {
        // Kafka configuration
        String bootstrapServers = "your-kafka-bootstrap-server:9092";
        String topicName = "your-topic-name";

        // SSL configuration
        Map<String, Object> config = new HashMap<>();
        config.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put("security.protocol", "SSL");
        config.put("ssl.keystore.location", "/path/to/your/keystore.jks");
        config.put("ssl.keystore.password", "your-keystore-password");
        config.put("ssl.key.password", "your-key-password");
        config.put("ssl.truststore.location", "/path/to/your/truststore.jks");
        config.put("ssl.truststore.password", "your-truststore-password");

        try (AdminClient adminClient = AdminClient.create(config)) {
            // Delete and recreate the topic
            deleteAndRecreateTopic(adminClient, topicName);
            System.out.println("Successfully purged the Kafka topic: " + topicName);
        } catch (Exception e) {
            System.err.println("Failed to purge the Kafka topic: " + e.getMessage());
        }
    }

    private static void deleteAndRecreateTopic(AdminClient adminClient, String topicName) throws ExecutionException, InterruptedException {
        // Delete the topic
        adminClient.deleteTopics(Collections.singletonList(topicName)).all().get();
        System.out.println("Topic deleted: " + topicName);

        // Wait for a short period to ensure the topic is fully deleted
        Thread.sleep(5000);

        // Recreate the topic with default settings
        NewTopic newTopic = new NewTopic(topicName, 1, (short) 1); // Change partitions and replication factor as needed
        adminClient.createTopics(Collections.singletonList(newTopic)).all().get();
        System.out.println("Topic recreated: " + topicName);
    }
}
