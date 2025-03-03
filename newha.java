public static void contactUs(String contactUsUrl, FormValues formValues, WebDriver driver) {
    System.out.println(contactUsUrl);
    driver.get(contactUsUrl);

    // Ensure the page is fully loaded (wait for a specific element to appear, e.g., a submit button)
    WebDriverWait wait = new WebDriverWait(driver, 10);
    wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("submitButton"))); // Replace with a real element on your page

    // Fill the form using the values from formValues
    driver.findElement(By.id("firstName")).sendKeys(formValues.getFirstName());
    driver.findElement(By.id("lastName")).sendKeys(formValues.getLastName());
    driver.findElement(By.id("email")).sendKeys(formValues.getEmail());
    driver.findElement(By.id("phone")).sendKeys(formValues.getPhone());
    driver.findElement(By.id("newsletter")).click(); // assuming this is a checkbox
    driver.findElement(By.id("occupation")).sendKeys(formValues.getOccupation());
    driver.findElement(By.id("message")).sendKeys(formValues.getMessage());

    // Submit the form (optional depending on the test case)
    driver.findElement(By.id("submitButton")).click();
}
