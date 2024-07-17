
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

public class MetadataService {

    private MetadataRepository metadataRepository;

    public MetadataService(MetadataRepository metadataRepository) {
        this.metadataRepository = metadataRepository;
    }

    public CompletableFuture<List<Metadata>> getPendingMetadataByArpRolesAndActorAsync(Set<String> groups, String email) {
        // Call repository methods asynchronously
        CompletableFuture<Set<Metadata>> pendingMetadataFuture = CompletableFuture.supplyAsync(() -> 
            new HashSet<>(metadataRepository.getPendingMetadataldByArpRoles(groups, email))
        );

        CompletableFuture<Set<Metadata>> actorMetadataFuture = CompletableFuture.supplyAsync(() -> 
            new HashSet<>(metadataRepository.getActorMetadataIdSByActorEmail(email))
        );

        // Combine the results
        return pendingMetadataFuture.thenCombine(actorMetadataFuture, (pendingMetadata, actorMetadata) -> {
            Set<Metadata> result = new HashSet<>();
            result.addAll(pendingMetadata);
            result.addAll(actorMetadata);
            return new ArrayList<>(result);
        });
    }

    public List<Metadata> getPendingMetadataByArpRolesAndActor(Set<String> groups, String email) {
        try {
            return getPendingMetadataByArpRolesAndActorAsync(groups, email).get();
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
            return Collections.emptyList();
        }
    }
}
