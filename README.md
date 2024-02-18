# Тестовое задание 
Вам требуется написать сервис на Python согласно техническому заданию ниже.
При разработке предлагается использовать Python версии не ниже 3.8, pip / poetry.
Описание системы
К реализации предлагается система учета и анализа данных, поступающих с условного устройства. Полученные данные привязываются к временной метке и устройству, с которого пришли данные, и сохраняются в БД. Набор данных используется для дальнейшего анализа. 
Требования к системе
## Функциональные выполнены
###	В системе реализован сбор статистики с устройства по его идентификатору
###	формат получаемой статистики - {“x”: float, “y”: float, “z”:float}
###	В системе реализован анализ собранной статистики с устройства за определенный период и за все время
###	Результатами анализа являются числовые характеристики величины:
-	минимальное значение
-	максимальное значение
-	количество
-	сумма
-	медиана
###	Система поддерживает добавление пользователей устройств
###	В системе реализован функционал получения анализа показаний устройств по идентификатору пользователя*:
-	агрегированные результаты для всех устройств
-	для каждого устройства отдельно
## Нефункциональные 
-	архитектура REST
-	фреймворк реализации сервиса FastApi 
-	собранные данные хранятся в БД на выбор разработчика
-	Сервис и его окружение разворачивается средствами docker + docker-compose 

## Getting Started

To set up and run the app, please follow these steps:

1. Move to the directory where `pyproject.toml` is located:

   ```shell
   cd DeviceStats
   ```
2. Install the dependencies:

   ```shell
   poetry install
   ```

   If you don't want to install the dev packages,
   you can use the following command instead:
   ```shell
   poetry install --without dev
   ```

3. Activate the virtual environment:

   ```shell
   poetry shell
   ```

4. All necessary commands to start with the project can be found in Makefile.
   To see all available commands, run the following command:

   ```shell
   make help
   ```

5. Build and start the Docker containers:

   ```shell
   make build
   ```

6. Open your browser and go to `http://localhost:8000` to see the app running.


7. To check the documentation of the API, go to `http://localhost:8000/docs`.

8. To check the database you can use hosted `pgAdmin` tool, just go to `http://localhost:5050` and login with the credentials from `.env` file:
   - Email: `$PGADMIN_EMAIL`
   - Password: `$PGADMIN_PASSWORD`

