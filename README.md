# Полезная инфа для работы

1. создание `.env.local`

    ```bash
    touch .env.local
    ```

    заполняем с заглушками в свой .env.local 

1. при развертывании проекта, создаем `.env` для заполнения 

    ```bash
    cp .env.local .env
    ```

1. чтобы не вспоминать какие пакеты должны быть установлены в виртуальном окружении, создаём файл `requirements.txt`

    ```bash
    pip freeze > requirements.txt
    ```

1. установка пакетов из `requirements.txt`

    ```bash
    pip install -r requirements.txt
    ```
