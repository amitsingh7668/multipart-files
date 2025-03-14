from elasticsearch import Elasticsearch

# Elasticsearch host (use the correct URL)
ELASTICSEARCH_HOST = "http://your-elasticsearch-host:9200"  # Replace with your host

# Kibana credentials
USERNAME = "your-kibana-username"
PASSWORD = "your-kibana-password"

# Connect to Elasticsearch with authentication
es = Elasticsearch(
    [ELASTICSEARCH_HOST],
    basic_auth=(USERNAME, PASSWORD)
)

# Define your query (Modify as needed)
query = {
    "query": {
        "match_all": {}  # Example query to fetch all documents
    }
}

# Specify your index
INDEX_NAME = "your-index-name"  # Change to your index name

# Run the query
response = es.search(index=INDEX_NAME, body=query)

# Print results
print(response)
