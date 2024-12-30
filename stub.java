import org.junit.jupiter.api.Test;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;

import static org.assertj.core.api.Assertions.assertThat;

public class EmailStubConfigurationTest {

    private final ApplicationContextRunner contextRunner = new ApplicationContextRunner()
            .withUserConfiguration(EmailStubConfiguration.class);

    @Test
    public void testEmailSenderServiceStubBeanExistsWhenPropertyIsTrue() {
        contextRunner
                .withPropertyValues("ets.mail.stub=true") // Simulate property being set to true
                .run(context -> {
                    // Assert the EmailSenderServiceStub bean is created
                    assertThat(context).hasSingleBean(EmailSenderServiceStub.class);
                });
    }

    @Test
    public void testEmailSenderServiceStubBeanDoesNotExistWhenPropertyIsFalse() {
        contextRunner
                .withPropertyValues("ets.mail.stub=false") // Simulate property being set to false
                .run(context -> {
                    // Assert the EmailSenderServiceStub bean is not created
                    assertThat(context).doesNotHaveBean(EmailSenderServiceStub.class);
                });
    }
}
