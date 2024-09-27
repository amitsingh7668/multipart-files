import org.apache.poi.ss.usermodel.*;
import org.springframework.core.io.ClassPathResource;
import java.io.InputStream;
import java.util.HashSet;
import java.util.Set;

public class ExcelReaderService {

    public Set<String> readColumnValues(String filePath, int columnIndex) {
        Set<String> values = new HashSet<>();

        try {
            // Load the XLS file from the resource folder of another module
            InputStream inputStream = new ClassPathResource(filePath).getInputStream();
            Workbook workbook = WorkbookFactory.create(inputStream);
            Sheet sheet = workbook.getSheetAt(0); // Read the first sheet
            
            for (Row row : sheet) {
                Cell cell = row.getCell(columnIndex);
                if (cell != null) {
                    values.add(cell.toString());  // Add the cell value to the set
                }
            }

            workbook.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return values;
    }
}
