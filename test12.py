from fastapi import FastAPI
import unittest
import io
import sys

app = FastAPI()

@app.get("/run-tests")
def run_tests():
    # Capture the output of the tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')  # Discover tests in the "tests" folder
    test_runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
    
    test_results = test_runner.run(test_suite)
    
    # Collect results
    results = {
        "testsRun": test_results.testsRun,
        "failures": len(test_results.failures),
        "errors": len(test_results.errors),
        "skipped": len(test_results.skipped),
        "failures_details": [
            {"test": str(f[0]), "reason": str(f[1])} for f in test_results.failures
        ],
        "errors_details": [
            {"test": str(e[0]), "reason": str(e[1])} for e in test_results.errors
        ],
    }
    
    return results
