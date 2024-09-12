import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.io.IOException;

import static org.mockito.Mockito.*;

class RequestResponseLoggingFilterTest {

    private RequestResponseLoggingFilter filter;
    private HttpServletRequest request;
    private HttpServletResponse response;
    private FilterChain filterChain;
    private RequestWrapper requestWrapper;
    private ResponseWrapper responseWrapper;

    @BeforeEach
    void setUp() {
        filter = new RequestResponseLoggingFilter();
        request = mock(HttpServletRequest.class);
        response = mock(HttpServletResponse.class);
        filterChain = mock(FilterChain.class);

        // Mock the custom wrappers as well
        requestWrapper = mock(RequestWrapper.class);
        responseWrapper = mock(ResponseWrapper.class);
    }

    @Test
    void testDoFilter() throws IOException, ServletException {
        // Mock request data
        when(request.getMethod()).thenReturn("GET");
        when(request.getRequestURI()).thenReturn("/test");
        when(request.getHeaderNames()).thenReturn(Collections.enumeration(Collections.emptyList()));
        when(request.getParameterNames()).thenReturn(Collections.enumeration(Collections.emptyList()));
        when(requestWrapper.getBody()).thenReturn("");  // Simulate an empty request body

        // Mock response data
        when(responseWrapper.getStatus()).thenReturn(200);
        when(responseWrapper.getContent()).thenReturn("OK");

        // Execute the filter's doFilter method
        filter.doFilter(request, response, filterChain);

        // Verify the filter chain continues as expected
        verify(filterChain).doFilter(any(RequestWrapper.class), any(ResponseWrapper.class));

        // Verify request logging logic
        verify(request).getMethod();
        verify(request).getRequestURI();
    }

    @Test
    void testLogRequestAndResponse() throws IOException, ServletException {
        // Capture logs and simulate a request and response cycle
        when(requestWrapper.getBody()).thenReturn("Test request body");
        when(responseWrapper.getContent()).thenReturn("Test response content");

        // Capture the wrapped response and request for verification
        ArgumentCaptor<RequestWrapper> requestCaptor = ArgumentCaptor.forClass(RequestWrapper.class);
        ArgumentCaptor<ResponseWrapper> responseCaptor = ArgumentCaptor.forClass(ResponseWrapper.class);

        // Execute the filter
        filter.doFilter(request, response, filterChain);

        // Verify that the filter has passed the wrapped request and response to the chain
        verify(filterChain).doFilter(requestCaptor.capture(), responseCaptor.capture());

        // Ensure that the captured request and response match the expected wrapped objects
        assertNotNull(requestCaptor.getValue());
        assertNotNull(responseCaptor.getValue());

        // Verify that the logRequest and logResponse methods were called correctly
        verify(requestWrapper).getBody();
        verify(responseWrapper).getContent();
    }
}
