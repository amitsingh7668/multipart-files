import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import org.json.JSONArray;
import org.json.JSONObject;

public class GroupMemberFetcher {

    public static void main(String[] args) {
        // Your comma-separated string of groups
        String groups = "group1,group2,group3";
        
        // Split the string into individual groups
        String[] groupArray = groups.split(",");
        
        // CSV file to store the output
        String csvFile = "group_members.csv";
        
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvFile))) {
            // Write the header of the CSV file
            writer.write("Group Name,User Name");
            writer.newLine();
            
            // Iterate over each group
            for (String group : groupArray) {
                // Call API and get members of the group
                String[] members = getGroupMembers(group.trim());
                
                // Write each member to the CSV file
                for (String member : members) {
                    writer.write(group + "," + member);
                    writer.newLine();
                }
            }
            
            System.out.println("Data has been written to " + csvFile);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    // Method to get members of a group by calling the API
    private static String[] getGroupMembers(String groupName) {
        String apiUrl = "https://api.example.com/groups/" + groupName + "/members";
        HttpURLConnection connection = null;
        try {
            URL url = new URL(apiUrl);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();
            
            int responseCode = connection.getResponseCode();
            if (responseCode != 200) {
                throw new RuntimeException("HttpResponseCode: " + responseCode);
            } else {
                Scanner scanner = new Scanner(url.openStream());
                String inline = "";
                while (scanner.hasNext()) {
                    inline += scanner.nextLine();
                }
                scanner.close();
                
                // Parse JSON response
                JSONArray jsonArray = new JSONArray(inline);
                String[] members = new String[jsonArray.length()];
                for (int i = 0; i < jsonArray.length(); i++) {
                    JSONObject memberObject = jsonArray.getJSONObject(i);
                    members[i] = memberObject.getString("name");
                }
                return members;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new String[0];
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
