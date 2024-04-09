docker build -t fastapi-app .

docker run -d -p 8000:8000 fastapi-app

# Set environment variables
ENV INDEX_URL=https://example.com/pypi/simple/
ENV TRUSTED_HOSTS=example.com
