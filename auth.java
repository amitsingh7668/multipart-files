import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.apache.http.impl.client.CloseableHttpClient;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import java.util.List;

class RestTemplateConfigurationTest {

    @Mock
    private RestTemplateBuilder builder;

    @InjectMocks
    private RestTemplateConfiguration config;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testRestTemplateCreation() throws Exception {
        // Mock the builder behavior
        when(builder.setConnectTimeout(any())).thenReturn(builder);
        when(builder.setReadTimeout(any())).thenReturn(builder);
        when(builder.messageConverters(any(List.class))).thenReturn(builder);
        when(builder.build()).thenReturn(new RestTemplate());

        // Call the method under test
        RestTemplate restTemplate = config.restTemplate("https://bigpanda.api", builder);

        // Verify that the RestTemplate is properly created
        assertNotNull(restTemplate);
        verify(builder).setConnectTimeout(any());
        verify(builder).setReadTimeout(any());
        verify(builder).messageConverters(any(List.class));
    }
}
