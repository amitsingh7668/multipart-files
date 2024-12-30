import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.core.io.ClassPathResource;
import org.springframework.ui.freemarker.SpringResourceTemplateResolver;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import org.modelmapper.ModelMapper;

import java.io.IOException;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@SpringJUnitConfig
public class EmailConfigurationTest {

    @Mock
    private EtsEmailPropertyConfiguration etsEmailPropertyConfiguration;

    @Mock
    private ApplicationContext applicationContext;

    private EmailConfiguration emailConfiguration;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        emailConfiguration = new EmailConfiguration(etsEmailPropertyConfiguration);
    }

    @Test
    public void testModelMapperBean() {
        ModelMapper modelMapper = emailConfiguration.modelMapper();
        assertNotNull(modelMapper, "ModelMapper bean should not be null");
    }

    @Test
    public void testTemplateResolverBean() {
        SpringResourceTemplateResolver templateResolver = emailConfiguration.templateResolver(applicationContext);
        assertNotNull(templateResolver, "TemplateResolver bean should not be null");
        assertEquals("classpath:/", templateResolver.getPrefix(), "TemplateResolver prefix is incorrect");
        assertEquals(".html", templateResolver.getSuffix(), "TemplateResolver suffix is incorrect");
        assertTrue(templateResolver.getResolvablePatterns().contains("templates/**"), "TemplateResolver resolvable patterns are incorrect");
    }

    @Test
    public void testEtsPropertyLoaderBean() throws IOException {
        when(etsEmailPropertyConfiguration.getLmfNeoInboxDashboard()).thenReturn("lmf.neo.inbox.dashboard.value");
        when(etsEmailPropertyConfiguration.getClipsNeoInboxDashboard()).thenReturn("clips.neo.inbox.dashboard.value");
        when(etsEmailPropertyConfiguration.getMailboxName()).thenReturn("mailbox.name.value");
        when(etsEmailPropertyConfiguration.getRequestRequiresFlowGroupAssignmentTo()).thenReturn("flow.group.assignment.to.value");
        when(etsEmailPropertyConfiguration.getRequestRequiresFlowGroupAssignmentCcO()).thenReturn("flow.group.assignment.cc.value");

        Properties properties = emailConfiguration.etsPropertyLoader();

        assertNotNull(properties, "Properties should not be null");
        assertEquals("lmf.neo.inbox.dashboard.value", properties.getProperty("lmf.neo.inbox.dashboard"));
        assertEquals("clips.neo.inbox.dashboard.value", properties.getProperty("ets.neo.inbox.dashboard"));
        assertEquals("mailbox.name.value", properties.getProperty("ets.mailbox.name"));
        assertEquals("flow.group.assignment.to.value", properties.getProperty("ets.request.requires.flow.group.assignment.to"));
        assertEquals("flow.group.assignment.cc.value", properties.getProperty("ets.request.requires.flow.group.assignment.cc"));

        verify(etsEmailPropertyConfiguration).getLmfNeoInboxDashboard();
        verify(etsEmailPropertyConfiguration).getClipsNeoInboxDashboard();
        verify(etsEmailPropertyConfiguration).getMailboxName();
        verify(etsEmailPropertyConfiguration).getRequestRequiresFlowGroupAssignmentTo();
        verify(etsEmailPropertyConfiguration).getRequestRequiresFlowGroupAssignmentCcO();
    }
}
