import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;

@Component
public class RequestResponseLoggingFilter implements Filter {

    private static final Logger log = LoggerFactory.getLogger(RequestResponseLoggingFilter.class);

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        // Generate a UUID for tracking this request
        String uuid = UUID.randomUUID().toString();
        
        // Add UUID to the request attributes to propagate it through the request
        request.setAttribute("requestUUID", uuid);

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        Long startTime = System.currentTimeMillis();

        // Log the incoming request with UUID
        logRequest(httpRequest, uuid);

        chain.doFilter(request, response);

        // Log the outgoing response with UUID
        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;
        logResponse(httpResponse, executionTime, uuid);
    }

    private void logRequest(HttpServletRequest request, String uuid) {
        log.info("Incoming Request - UUID: {}, Method: {}, URI: {}", uuid, request.getMethod(), request.getRequestURI());
    }

    private void logResponse(HttpServletResponse response, long executionTime, String uuid) {
        log.info("Outgoing Response - UUID: {}, Status: {}, Execution Time: {} ms", uuid, response.getStatus(), executionTime);
    }
}
