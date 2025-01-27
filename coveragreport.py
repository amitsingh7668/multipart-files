from fastapi import FastAPI
import unittest
import coverage
import io

app = FastAPI()

@app.get("/run-tests")
def run_tests_with_coverage():
    # Initialize coverage measurement
    cov = coverage.Coverage()
    cov.start()

    # Run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern="test_*.py")
    test_runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
    result_stream = io.StringIO()
    test_runner = unittest.TextTestRunner(stream=result_stream, verbosity=2)
    result = test_runner.run(test_suite)

    # Stop coverage measurement
    cov.stop()
    cov.save()

    # Calculate coverage percentage
    cov_report = io.StringIO()
    cov.report(file=cov_report)
    coverage_percentage = cov.report()  # Returns the overall coverage percentage

    # Collect results
    response = {
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failures_details": [
            {"test": str(f[0]), "reason": str(f[1])} for f in result.failures
        ],
        "errors_details": [
            {"test": str(e[0]), "reason": str(e[1])} for e in result.errors
        ],
        "coverage_percentage": coverage_percentage,
    }

    return response
