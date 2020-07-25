docker rm -f sentiment_backend
docker build -t docker_for_sentiment_backend .
docker run -d -p 8081:8081 --name sentiment_backend docker_for_sentiment_backend:latest