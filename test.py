# перед тестированием нужно запустить сервер (server.py)
from requests import get, post, delete

# Получение списка всех новостей
print(get('http://localhost:8080/news').json())

# Получение одной новости по id
print(get('http://localhost:8080/news/1').json())
print(get('http://localhost:8080/news/8').json())  # новости с id=8 нет в базе

# Добавление новости
print(post('http://localhost:8080/news').json())  # ошибка Empty request
print(post('http://localhost:8080/news', json={'title': 'Заголовок'}).json())  # ошибка Bad request
print(post('http://localhost:8080/news', json={'title': 'Заголовок', 'content': 'Текст новости', 'user_id': 1}).json())

# Удаление новости
print(delete('http://localhost:8080/news/8').json())  # новости с id=8 нет в базе
print(delete('http://localhost:8080/news/3').json())

