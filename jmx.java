import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import javax.management.MBeanServer;
import javax.management.ObjectName;
import java.lang.management.ManagementFactory;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

class MBeanConfigTest {

    private JmxAdminUtil jmxAdminUtil;
    private MBeanConfig mBeanConfig;
    private MBeanServer mBeanServer;

    @BeforeEach
    void setUp() {
        jmxAdminUtil = mock(JmxAdminUtil.class);
        mBeanConfig = new MBeanConfig(jmxAdminUtil);
        mBeanServer = ManagementFactory.getPlatformMBeanServer();
    }

    @Test
    void testJmxMBeanConfig() throws Exception {
        ObjectName objectName = mBeanConfig.jmxMBeanConfig();
        
        assertNotNull(objectName);
        
        // Verifying that the MBean was registered correctly
        verify(mBeanServer).registerMBean(jmxAdminUtil, objectName);
    }
}
