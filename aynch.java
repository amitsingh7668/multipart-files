@Configuration
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10); // Number of core threads
        executor.setMaxPoolSize(50); // Maximum threads for scaling
        executor.setQueueCapacity(100); // Queue size before rejecting tasks
        executor.setThreadNamePrefix("AsyncExecutor-");
        executor.initialize();
        return executor;
    }
}
