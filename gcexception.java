private <T> ResponseEntity<T> doWithRetry(Supplier<T> operation) {
    for (var retries = 0; retries < MAX_RETRIES; retries++) {
        try {
            // Attempt the operation
            T result = operation.get();
            System.out.println("Operation successful, result: " + result);
            return ResponseEntity.ok(result); // Return successful ResponseEntity
        } catch (HttpServerErrorException e) {
            // Check if the error body contains "globalcds"
            if (e.getResponseBodyAsString().contains("globalcds")) {
                log.info("GlobalCDS-specific error detected, returning dummy ResponseEntity");
                return createDummyResponseEntity(); // Return a dummy ResponseEntity
            }
            log.info("Request failed, retrying attempt " + (retries + 1), e);
        }
    }
    throw new RestClientException(EXCEPTION_DURING_CALL_TO_GCDS);
}

// Helper method to create a dummy ResponseEntity
private <T> ResponseEntity<T> createDummyResponseEntity() {
    // Return a ResponseEntity with a dummy body and status
    T dummyBody = (T) "Dummy Response"; // Replace with your dummy object
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(dummyBody);
}
