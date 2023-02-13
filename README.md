# *API* для благотворительного фонда *QRKot*
## Оглавление
1. [Описание](https://github.com/TomatoInOil/cat_charity_fund/README.md#описание)
2. [Технологии](https://github.com/TomatoInOil/cat_charity_fund/README.md#технологии)
3. [Установка](https://github.com/TomatoInOil/cat_charity_fund/README.md#установка)
4. [Примеры запросов](https://github.com/TomatoInOil/cat_charity_fund/README.md#примеры-запросов)
    1. [Благотворительные проекты](https://github.com/TomatoInOil/cat_charity_fund/README.md#благотворительные-проекты)
    2. [Пожертвования](https://github.com/TomatoInOil/cat_charity_fund/README.md#пожертвования)
    3. [Пользователи](https://github.com/TomatoInOil/cat_charity_fund/README.md#пользователи)
5. [Автор](https://github.com/TomatoInOil/cat_charity_fund/README.md#автор)
## Описание
Фонд собирает пожертвования на различные целевые проекты. С помощью *API* можно создавать целевые проекты с названием, описанием и целевой суммой. Пожертвования направляются в первый открытый проект и когда он закрывается, переходят к следующему по принципу `First In, First Out`. Перейти к [примерам запросов](https://github.com/TomatoInOil/cat_charity_fund/README.md#примеры-запросов).
## Технологии
- `Python 3.7.9`
- `FastAPI`
- `FastAPI-users`
- `SQLAlchemy`
- `Pydantic`
- `Asyncio`
## Установка
1. Клонируйте проект 
```BASH
git clone https://github.com/TomatoInOil/cat_charity_fund.git
```
2. Перейдите в корневую директорию проекта 
```BASH
cd cat_charity_fund/
```
3. Установите виртуальное окружение с `Python 3.7.9` и активируйте его  
4. Далее установите зависимости 
```BASH
pip install -r requirements.txt
```
5. Заполните `.env` по образцу `example.env`, который лежит в корневой директории    
6. Примините миграции
```BASH
alembic upgrade head
```
7. Запустите *ASGI*-сервер. Можно добавить флаг `--reload`, тогда при изменении файлов приложение будет перезапускаться
```BASH
uvicorn app.main:app
```
## Примеры запросов
После развёртывания проекта документацию можно найти на эндпоинте `.../docs/`
### Благотворительные проекты
POST-запрос .../charity_project/:
```JSON
{
  "name": "На корм для кошек",
  "description": "Кошки нуждаются в еде",
  "full_amount": 2500
}
```
Ответ (200):
```JSON
{
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-02-13T15:11:47.980127",
  "name": "На корм для кошек",
  "description": "Кошки нуждаются в еде",
  "full_amount": 2500,
  "id": 10
}
```
### Пожертвования
POST-запрос .../donation/
```JSON
{
  "comment": "Очень люблю хвостатых, пусть у них всё будет замечательно",
  "full_amount": 125000
}
```
Ответ (200):
```JSON
{
  "comment": "Очень люблю хвостатых, пусть у них всё будет замечательно",
  "full_amount": 125000,
  "id": 2,
  "create_date": "2023-02-13T15:15:16.679223"
}
```
### Пользователи
Эндпоинты для авторизации и управления пользователями реализованы на `fastapi-users`.
## Автор
Проект выполнен в рамках прохождения курса Яндекс.Практикума Даниилом Паутовым.
