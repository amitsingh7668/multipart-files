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
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // Log the incoming request
        logRequest(httpRequest);

        chain.doFilter(request, response);

        // Log the outgoing response
        logResponse(httpResponse);
    }

    private void logRequest(HttpServletRequest request) throws IOException {
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
    }

    private void logResponse(HttpServletResponse response) {
        System.out.println("Response Status: " + response.getStatus());
        // You can add more details if needed
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
