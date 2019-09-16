Запуск контейнера на 5000 порту:

docker build -t pchech/rot .

docker run -p 5000:5000 -e TOKEN=<bot_token> -e CHAT_ID=<chat_id> pchech/rot
