import requests

# Fill in your details here to be posted to the login form.
payload = {
    'username': 'User',
    'password': 'Password'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('http://localhost:8080/login', data=payload)

print(p.text)
