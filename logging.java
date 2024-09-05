import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.FilterConfig;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Collections;
import java.util.stream.Collectors;

@Component
public class RequestResponseLoggingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
            throws IOException, ServletException {

        // Wrap the request and response to log their payloads
        RequestWrapper wrappedRequest = new RequestWrapper((HttpServletRequest) request);
        ResponseWrapper wrappedResponse = new ResponseWrapper((HttpServletResponse) response);

        // Record the start time before processing the request
        long startTime = System.currentTimeMillis();

        // Log the request details
        logRequest(wrappedRequest);

        // Continue the request-response chain
        chain.doFilter(wrappedRequest, wrappedResponse);

        // Record the end time after processing the request
        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;

        // Log the response details and execution time
        logResponse(wrappedResponse, executionTime);
    }

    private void logRequest(RequestWrapper request) throws IOException {
        String headers = Collections.list(request.getHeaderNames())
            .stream()
            .map(header -> header + ": " + request.getHeader(header))
            .collect(Collectors.joining("\n"));

        String params = Collections.list(request.getParameterNames())
            .stream()
            .map(param -> param + "=" + request.getParameter(param))
            .collect(Collectors.joining("&"));

        System.out.println("Request Method: " + request.getMethod());
        System.out.println("Request URI: " + request.getRequestURI());
        System.out.println("Request Headers: \n" + headers);
        System.out.println("Request Parameters: " + params);
        System.out.println("Request Body: " + request.getBody());
    }

    private void logResponse(ResponseWrapper response, long executionTime) throws IOException {
        System.out.println("Response Status: " + response.getStatus());
        System.out.println("Response Body: " + response.getContent());
        System.out.println("Total Execution Time: " + executionTime + " ms");
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // Optional: filter initialization
    }

    @Override
    public void destroy() {
        // Optional: cleanup resources
    }
}
