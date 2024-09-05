import org.springframework.stereotype.Component;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Collections;
import java.util.Enumeration;
import java.util.Map;
import java.util.stream.Collectors;

@Component
public class RequestResponseLoggingFilter extends javax.servlet.Filter {

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
}
