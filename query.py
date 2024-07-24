java -cp "main/feeds-service-1.11.1-SNAPSHOT.jar:lib/*" \
     -Djsse.enableSNIExtension=false \
     -Doracle.jdbc.autoCommitSpecCompliant=false \
     -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 \
     com.ubs.workbench.feeds.WbIntegrator $1 $2 $$ &
