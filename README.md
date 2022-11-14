![example workflow](https://github.com/shlenskov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# API для Проекта YaMDb.
### *Проект YaMDb собирает отзывы пользователей на авторские произведения.*

*Общедоступный API с системой JWT-аутентификации для расширения действий пользователя.
Общий доступ позволяет просматривать произведения, отзывы и комментарии к ним.
Аутентифицированные пользователи могут оставлять отзывы на произведения и комментарии к отзывам, ставить оценки произведениям.
Произведения делятся по жанрам и категориям (книги, фильмы, музыка и т.д.)
Произведениям присваивается рейтинг на основе отзывов пользователей.
В проекте реализованы права администратора и модератора.*
***


### Примеры запросов

|Действие|Тип запроса|Адрес|
|---|---|---|
|__Регистрация пользователя__|POST| .../api/v1/auth/signup/|
|__Редактирование своего профиля пользоватем__|PATCH| .../api/v1/users/me/|
|__Просмотр списка произведений__|GET| .../api/v1/titles/|
|__Удаление категории администратором__|DELETE| .../api/v1/categories/{slug}/|
|__Пользователь оставляет комментарий__|POST| .../api/v1/titles/{title_id}/reviews/{review_id}/comments/|
|__Удалить отзыв__|DELETE| .../api/v1/titles/{title_id}/reviews/{review_id}/|



### Технологии

- [Django] - веб-фреймворк на Python.
- [Django REST framework] - инструментарий для создания веб-API.
- [Simple JWT] - плагин аутентификации веб-токенов JSON для платформы Django REST
- [Django-filter] - приложение для динамической фильтрации запросов из параметров URL

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:shlenskov/yamdb_final.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv && . venv/bin/activate
```

Установить pip и зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Для загрузки csv из папки /static/data/ в базу:

```
python manage.py fillbase
```

Запустить проект:

```
python manage.py runserver
```

### Шаблон наполнения env-файла:

```
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT

```

### Развертывание контейнеров и заполнение БД

```

Сборка и развёртывание контейнеров в «фоновом режиме»:

docker-compose up -d --build

Выполнение миграций:

docker-compose exec web python manage.py migrate

Создание суперпользователя:

docker-compose exec web python manage.py createsuperuser

Сборка статики:

docker-compose exec web python manage.py collectstatic --no-input

Зайдите на http://localhost/admin/ и убедитесь, что страница отображается полностью

Создание дампа (резервную копию) базы данных:

docker-compose exec web python manage.py dumpdata > fixtures.json 

Останавка контейнеров:

docker-compose down -v

```

## Разработчики

- [Алексей Дубинин]
- [Владимир Шленсков]
- [Наталья Банникова]
- [Команда Яндекс.Практикум]

[//]: #

   [Django REST framework]: <https://www.django-rest-framework.org/>
   [Django]: <https://www.djangoproject.com/>
   [Simple JWT]: <https://pypi.org/project/djangorestframework-simplejwt/>
   [Django-filter]: <https://pypi.org/project/django-filter/2.4.0/>

   [Наталья Банникова]: <https://github.com/natalie731>
   [Алексей Дубинин]: <https://github.com/devdub>
   [Владимир Шленсков]: <https://github.com/shlenskov>
   [Команда Яндекс.Практикум]: <https://practicum.yandex.ru/>