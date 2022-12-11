import requests


# LIST OF COMMANDS
#   -------command-------|--first art--|--second arg--|--third arg--|---SUCCESSFUL RESULT---
#   1) login             |  username   |   password   |             |   username
#   2) change password   |  username   |   password   | newpassword |   Successful changes.
#   3) update name       |  username   |   newusername|             |   Successful update.
#   4) register          |  username   |   password   |             |   Successful register.
#   5) see all users     |             |              |             |   -----------------
#   6) delete user       |  username   |              |             |   Successful delete.
#   7) update scores     |  username   |   steps      | orders      |   Successful update.
#   8) see all maps      |             |              |             |   -----------------
#   9) see all rating    |             |              |             |   -----------------
#   10) delete rating-m  |  map        |              |             |   Successful delete"
#   11) delete rating-u  |  username   |              |             |   Successful delete"
#   12) change rating    |  map        |   newrating  | username    |   Successful added
#   13) see rating       |  username   |              |             |   -----------------

def Request(command):
    with requests.Session() as s:
        command = command.split(sep=' ')
        if command[0] == 'login':
            if len(command) == 3:
                payload = {
                    'username': command[1],
                    'password': command[2]
                }
                return str(s.post('http://localhost:8080/login', data=payload).content.decode())
            else:
                return "Incorrect use of function 'login'"
        elif command[0] == 'change':
            if command[1] == 'password':
                if len(command) == 5:
                    payload = {
                        'username': command[2],
                        'password': command[3],
                        'newpassword': command[4]
                    }
                    return str(s.post('http://localhost:8080/password', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'change password'"
            elif command[1] == 'rating':
                if len(command) == 5:
                    payload = {
                        'map': command[2],
                        'rating': command[3],
                        'username': command[4]
                    }
                    return str(s.post('http://localhost:8080/ratings/change', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'change rating'"
            else:
                return "Incorrect use of function 'change'"
        elif command[0] == 'delete' and len(command) > 2:
            if command[1] == 'user':
                if len(command) == 3:
                    payload = {
                        'username': command[2]
                    }
                    return str(s.post('http://localhost:8080/delete', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'delete user'"
            if command[1] == 'rating-m':
                if len(command) == 3:
                    payload = {
                        'map': command[2]
                    }
                    return str(s.post('http://localhost:8080/ratings/delete/map', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'delete rating-m'"
            if command[1] == 'rating-u':
                if len(command) == 3:
                    payload = {
                        'username': command[2]
                    }
                    return str(s.post('http://localhost:8080/ratings/delete/user', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'change rating-u'"
            else:
                return "Incorrect use of function 'change'"
        elif command[0] == 'update':
            if command[1] == 'name':
                if len(command) == 4:
                    payload = {
                        'username': command[2],
                        'newusername': command[3]
                    }
                    return str(s.post('http://localhost:8080/name', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'update name'"
            elif command[1] == 'score':
                if len(command) == 5:
                    payload = {
                        'username': command[2],
                        'steps': int(command[3]),
                        'orders': int(command[4])
                    }
                    return str(s.post('http://localhost:8080/update', data=payload).content.decode())
                else:
                    return "Incorrect use of function 'update score'"
        elif command[0] == 'register':
            if len(command) == 3:
                payload = {
                    'username': command[1],
                    'password': command[2]
                }
                return str(s.post('http://localhost:8080/register', data=payload).content.decode())
            else:
                return "Incorrect use of function 'register'"
        elif command[0] == 'see':
            if command[1] == 'all':
                if command[2] == 'users':
                    return s.get('http://localhost:8080/users').text
                elif command[2] == 'maps':
                    return s.get('http://localhost:8080/ratings/users').text
                elif command[2] == 'rating':
                    return s.get('http://localhost:8080/ratings').text
                else:
                    return "Incorrect use of function 'see all'"
            elif command[1] == 'rating':
                payload = {
                    'username': command[2]
                }
                return str(s.post('http://localhost:8080/ratings/get', data=payload).content.decode())
            else:
                return "Incorrect use of function 'see'"
        elif command[0] == 'add':
            if len(command) == 4:
                payload = {
                    'map': command[1],
                    'rating': int(command[2]),
                    'username': command[3]
                }
                return str(s.post('http://localhost:8080/ratings/add', data=payload).content.decode())
            else:
                return "Incorrect use of function 'add'"
        else:
            return "Incorrect input of function"
