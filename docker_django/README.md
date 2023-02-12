# Сайт генератор паролей

Для запуска потребуется ввести следующие косанды в консоль:

Эта команда создаст docker image paaswordgen на основе [Dockerfile](Dockerfile).

    docker build --tag=paaswordgen .

Эта команда создаст и запустит docker container paaswordgen, PORT = 7777


    docker run -d --name paaswordgen -p 7777:8000 paaswordgen

Основная страница будет доступна по адресу [localhost:7777](localhost:7777)