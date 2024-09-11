
# Проект Blogicum  

## Описание
Blogicum - сайт для публикаций постов, для которых определены категории и опционально месторасположение. Зарегистрированные пользователи могут комментировать чужие посты. 

## Используемые технологии:

- Django 3.2
- SQLite
- Bootstrap

В проекте используется Python 3.9

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:SergeyZheludkov/django_sprint4.git
```

```
cd django_sprint4
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить пакетный менеджер и зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в рабочую папку и выполнить миграции:

```
cd blogicum/
```

```
python manage.py migrate
```

Загрузить тестовые данные:

```
python manage.py loaddata db.json
```

Запустить проект:

```
python manage.py runserver
```

В корень проекта необходимо поместить файл .env  с содержанием SECRET_KEY= '<секретный ключ Django>'

Сайт будет доступен по адресу http://127.0.0.1:8000/

____

**Сергей Желудков** 

Github: [@SergeyZheludkov](https://github.com/SergeyZheludkov/)
