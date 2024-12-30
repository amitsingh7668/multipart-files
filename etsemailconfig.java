import org.junit.jupiter.api.Test;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;

import static org.assertj.core.api.Assertions.assertThat;

@EnableConfigurationProperties(EtsEmailPropertyConfiguration.class)
public class EtsEmailPropertyConfigurationTest {

    private final ApplicationContextRunner contextRunner = new ApplicationContextRunner()
            .withPropertyValues(
                    "ets.lmf-neo-inbox-dashboard=lmfValue",
                    "ets.clips-neo-inbox-dashboard=clipsValue",
                    "ets.mailbox-name=mailboxNameValue",
                    "ets.request-requires-flow-group-assignment-to=toValue",
                    "ets.request-requires-flow-group-assignment-cc=ccValue",
                    "ets.mail-host=mailHostValue",
                    "ets.mail-notification-from=notificationFromValue"
            )
            .withUserConfiguration(EtsEmailPropertyConfiguration.class);

    @Test
    public void testEtsEmailPropertyConfigurationPropertiesBinding() {
        contextRunner.run(context -> {
            assertThat(context).hasSingleBean(EtsEmailPropertyConfiguration.class);
            
            EtsEmailPropertyConfiguration properties = context.getBean(EtsEmailPropertyConfiguration.class);
            assertThat(properties.getLmfNeoInboxDashboard()).isEqualTo("lmfValue");
            assertThat(properties.getClipsNeoInboxDashboard()).isEqualTo("clipsValue");
            assertThat(properties.getMailboxName()).isEqualTo("mailboxNameValue");
            assertThat(properties.getRequestRequiresFlowGroupAssignmentTo()).isEqualTo("toValue");
            assertThat(properties.getRequestRequiresFlowGroupAssignmentCc()).isEqualTo("ccValue");
            assertThat(properties.getMailHost()).isEqualTo("mailHostValue");
            assertThat(properties.getMailNotificationFrom()).isEqualTo("notificationFromValue");
        });
    }
}
