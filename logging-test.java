import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import java.io.IOException;

import static org.mockito.Mockito.*;

class RequestResponseLoggingFilterTest {

    private RequestResponseLoggingFilter requestResponseLoggingFilter;
    private MockHttpServletRequest request;
    private MockHttpServletResponse response;
    private FilterChain filterChain;

    @BeforeEach
    void setUp() {
        requestResponseLoggingFilter = new RequestResponseLoggingFilter();
        request = new MockHttpServletRequest();
        response = new MockHttpServletResponse();
        filterChain = mock(FilterChain.class);
    }

    @Test
    void testDoFilter_logsRequestAndResponse() throws IOException, ServletException {
        // Act
        requestResponseLoggingFilter.doFilter(request, response, filterChain);

        // Assert
        verify(filterChain).doFilter(request, response);
        // You can also add additional asserts for any log messages or timing you want to validate.
    }

    @Test
    void testDoFilter_executesWithinTimeLimit() throws IOException, ServletException {
        long startTime = System.currentTimeMillis();

        // Act
        requestResponseLoggingFilter.doFilter(request, response, filterChain);

        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;

        // Assert
        assertTrue(executionTime < 500, "Filter execution took too long");
        verify(filterChain, times(1)).doFilter(request, response);
    }
}
