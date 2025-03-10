from sqlalchemy import create_engine

# Replace with your details
hostname = "your-db-hostname.com"  # e.g., db.example.com
port = 1521                       # Default Oracle port
sid = "ORCL"                      # Your database SID (or Service Name)
username = "your_username"
password = "your_password"

# Create a direct connection string without TNS
engine = create_engine(f'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{sid}')

# Test connection
connection = engine.connect()
print("Connection successful!")
connection.close()
