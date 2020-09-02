docker rm -f vixDailySuggestion
docker build -t vix_daily_suggestion_docker .
docker run -d -p 8081:8081 --name vixDailySuggestion vix_daily_suggestion_docker:latest
crontab cronjob