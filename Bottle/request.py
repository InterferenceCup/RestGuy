import requests

# LIST OF COMMANDS
#   -------command-------|--first art--|--second arg--|--third arg--|--fourth arg--|
#   1) login             |  username   |   password   |             |              |
#   2) change password   |  username   |   password   | newpassword |              |
#   3) update name       |  username   |   newusername|             |              |
#   4) register          |  username   |   password   |             |              |
#   5) see all users     |             |              |             |              |
#   6) delete user       |  username   |              |             |              |
#   7) update scores     |  username   |   steps      | orders      |              |
#   8) see all maps      |             |              |             |              |
#   9) see all rating    |             |              |             |              |
#   10) delete rating-m  |  map        |              |             |              |
#   11) delete rating-u  |  username   |              |             |              |
#   12) change rating    |  map        |   newrating  | username    |              |
#   13) see rating       |  username   |              |             |              |

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    while True:
        command = input()
        print(" -" + command)
        command = command.split(sep=' ')

        if command[0] == 'login':
            if len(command) == 3:
                payload = {
                    'username': command[1],
                    'password': command[2]
                }
                print(str(s.post('http://localhost:8080/login', data=payload).content))
            else:
                print("Incorrect use of function 'login'")
        elif command[0] == 'change':
            if command[1] == 'password':
                if len(command) == 5:
                    payload = {
                        'username': command[2],
                        'password': command[3],
                        'newpassword': command[4]
                    }
                    print(str(s.post('http://localhost:8080/password', data=payload).content))
                else:
                    print("Incorrect use of function 'change password'")
            elif command[1] == 'rating':
                if len(command) == 5:
                    payload = {
                        'map': command[2],
                        'rating': command[3],
                        'username': command[4]
                    }
                    print(str(s.post('http://localhost:8080/ratings/change', data=payload).content))
                else:
                    print("Incorrect use of function 'change rating'")
            else:
                print("Incorrect use of function 'change'")
        elif command[0] == 'delete':
            if command[1] == 'user':
                if len(command) == 3:
                    payload = {
                        'username': command[2]
                    }
                    print(str(s.post('http://localhost:8080/delete', data=payload).content))
                else:
                    print("Incorrect use of function 'delete user'")
            if command[1] == 'rating-m':
                if len(command) == 3:
                    payload = {
                        'map': command[2]
                    }
                    print(str(s.post('http://localhost:8080/ratings/delete/map', data=payload).content))
                else:
                    print("Incorrect use of function 'delete rating-m'")
            if command[1] == 'rating-u':
                if len(command) == 3:
                    payload = {
                        'username': command[2]
                    }
                    print(str(s.post('http://localhost:8080/ratings/delete/user', data=payload).content))
                else:
                    print("Incorrect use of function 'change rating-u'")
            else:
                print("Incorrect use of function 'change'")
        elif command[0] == 'update':
            if command[1] == 'name':
                if len(command) == 4:
                    payload = {
                        'username': command[2],
                        'newusername': command[3]
                    }
                    print(str(s.post('http://localhost:8080/name', data=payload).content))
                else:
                    print("Incorrect use of function 'update name'")
            elif command[1] == 'score':
                if len(command) == 5:
                    payload = {
                        'username': command[2],
                        'steps': int(command[3]),
                        'orders': int(command[4])
                    }
                    print(str(s.post('http://localhost:8080/update', data=payload).content))
                else:
                    print("Incorrect use of function 'update score'")
        elif command[0] == 'register':
            if len(command) == 3:
                payload = {
                    'username': command[1],
                    'password': command[2]
                }
                print(str(s.post('http://localhost:8080/register', data=payload).content))
            else:
                print("Incorrect use of function 'register'")
        elif command[0] == 'see':
            if command[1] == 'all':
                if command[2] == 'users':
                    print(s.get('http://localhost:8080/users').text)
                elif command[2] == 'maps':
                    print(s.get('http://localhost:8080/ratings/users').text)
                elif command[2] == 'rating':
                    print(s.get('http://localhost:8080/ratings').text)
                else:
                    print("Incorrect use of function 'see all'")
            elif command[1] == 'rating':
                payload = {
                    'username': command[2]
                }
                print(str(s.post('http://localhost:8080/ratings/get', data=payload).content))
            else:
                print("Incorrect use of function 'see'")
        elif command[0] == 'add':
            if len(command) == 4:
                payload = {
                    'map': command[1],
                    'rating': int(command[2]),
                    'username': command[3]
                }
                print(str(s.post('http://localhost:8080/ratings/add', data=payload).content))
            else:
                print("Incorrect use of function 'add'")
        else:
            print("Incorrect input of function'")
