from requests import get, post

print(get('http://127.0.0.1:8080/api/v2/users/').json())