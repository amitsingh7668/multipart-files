import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

class BigPandaAlertingTest {

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private BigPandaAlerting bigPandaAlerting;

    private static final String BIG_PANDA_API_URL = "http://bigpanda.api";

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        bigPandaAlerting = new BigPandaAlerting(restTemplate);
        bigPandaAlerting.bigPandaApi = BIG_PANDA_API_URL;
    }

    @Test
    void testSendAlertToBigPanda() {
        String description = "Test alert description";
        String category = "Test category";

        Map<String, Object> mockResponseBody = new HashMap<>();
        mockResponseBody.put("key", "value"); // Mock response data

        ResponseEntity<Map> mockResponse = new ResponseEntity<>(mockResponseBody, null, 200);
        when(restTemplate.exchange(eq(BIG_PANDA_API_URL), eq(HttpMethod.POST), any(HttpEntity.class), eq(Map.class)))
                .thenReturn(mockResponse);

        ResponseEntity<ApiResponse> responseEntity = bigPandaAlerting.sendAlertToBigPanda(description, category);

        assertNotNull(responseEntity);
        assertEquals(BigPandaAlerting.SUCCESS, responseEntity.getBody().getStatus());
        assertEquals(mockResponseBody, responseEntity.getBody().getData());
        verify(restTemplate).exchange(eq(BIG_PANDA_API_URL), eq(HttpMethod.POST), any(HttpEntity.class), eq(Map.class));
    }
}
