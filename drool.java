import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

@RestController
@RequestMapping("/api")
public class FileUploadController {
    private static final Logger log = LoggerFactory.getLogger(FileUploadController.class);

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<String> uploadFileAndMetadata(
            @RequestPart("file") MultipartFile file, 
            @RequestPart("metadata") YourMetadataObject metadata) {

        try {
            log.info("Processing file: " + file.getOriginalFilename());
            log.info("Received metadata: " + metadata.toString());

            // Save file locally
            File localFile = saveFileLocally(file);

            // Process the saved file using Drools
            String compiledRules = compileRules(localFile.getAbsolutePath());

            // Process your JSON metadata as needed
            
            return ResponseEntity.ok("File and metadata processed successfully!");
        } catch (Exception e) {
            log.error("Error processing file and metadata", e);
            return ResponseEntity.status(500).body("Failed to process request");
        }
    }

    // Save file to local directory
    private File saveFileLocally(MultipartFile file) throws IOException {
        String uploadDir = "/tmp";  // You can choose any directory you want
        File localFile = new File(uploadDir, file.getOriginalFilename());
        try (FileOutputStream fos = new FileOutputStream(localFile)) {
            fos.write(file.getBytes());
        }
        log.info("File saved locally at: " + localFile.getAbsolutePath());
        return localFile;
    }

    // Example method to handle Drools processing
    public String compileRules(String filePath) throws Exception {
        log.info("Compiling rules from file: " + filePath);

        // Load file as InputStream
        FileInputStream fis = new FileInputStream(new File(filePath));
        SpreadsheetCompiler sc = new SpreadsheetCompiler();
        
        // Compile rules
        String rules = sc.compile(fis, InputType.XLS);
        
        log.info("Rules file compiled successfully.");
        return rules;
    }
}
