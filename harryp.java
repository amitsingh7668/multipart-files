import org.openqa.selenium.*;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import java.util.List;

public class AdvanceFormFiller {

    public static void contactUs(String contactUsUrl, FormValues formValues, WebDriver driver) {
        driver.get(contactUsUrl);

        // Find all input fields on the form
        List<WebElement> inputElements = driver.findElements(By.tagName("input"));

        for (WebElement input : inputElements) {
            if (!input.isDisplayed()) {
                continue; // Ignore hidden fields
            }

            String fieldName = "";
            // Identify input fields using multiple attributes
            if (input.getAttribute("id") != null) fieldName = input.getAttribute("id");
            else if (input.getAttribute("name") != null) fieldName = input.getAttribute("name");
            else if (input.getAttribute("placeholder") != null) fieldName = input.getAttribute("placeholder");
            else if (input.getAttribute("aria-label") != null) fieldName = input.getAttribute("aria-label");

            // Fill the form based on mapped fields
            switch (fieldName.toLowerCase()) {
                case "first_name":
                    input.sendKeys(formValues.getFirstName());
                    break;
                case "last_name":
                    input.sendKeys(formValues.getLastName());
                    break;
                case "email":
                    input.sendKeys(formValues.getEmail());
                    break;
                case "phone":
                    input.sendKeys(formValues.getPhone());
                    break;
                case "agreement":
                    input.sendKeys(formValues.getAgreement());
                    break;
                case "identify":
                    input.sendKeys(formValues.getIdentify());
                    break;
                case "help":
                    input.sendKeys(formValues.getHelp());
                    break;
                case "newsletter":
                    input.sendKeys(formValues.getNewsletter());
                    break;
                default:
                    input.sendKeys("None"); // Default value if field is not recognized
            }
        }

        // Submit the form
        WebElement submitButton = driver.findElement(By.cssSelector("button[type='submit']"));
        submitButton.click();
    }

    // DO NOT MODIFY
    public static String getValues(String contactUsUrl, WebDriver driver) {
        driver.get(contactUsUrl);
        return driver.getPageSource();
    }
}
