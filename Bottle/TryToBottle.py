from bottle import route, run, request, post, get
import DataBaseForRestGuy as Base

# LIST OF FUNCTIONS
#   LOGINS
#       1) InsertTableLogins - register
#       2) CheckPassword - login
#       3) UpdateStepsAndOrders - update
#       4) UpdatePassword - change_password
#       5) UpdateName - name
#       6) DeleteUser - delete
#       7) GetAll - see_all_users
#   RATING BY USER
#       1) AddRating - add_rating
#       2) ChangeRating - change_rating
#       3) DeleteRatingByMap -
#       4) DeleteRatingByUser -
#       5) GetRatingByUser - get_rating_by_user
#       6) ChangeUserInRating - get_rating_by_user
#       7) GetAll - see_users_rating
#   RATING
#       1) GetAll -


@get('/login')  # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''


@post('/login')  # or @route('/login', method='POST')
def do_login():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = Base.CheckPassword(base, username, password)
    base.close()
    if type(result) != int:
        return result
    else:
        return "<p>Login failed.</p>"


@get('/register')  # or @route('/register')
def register():
    return '''
        <form action="/register" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Register" type="submit" />
        </form>
    '''


@post('/register')  # or @route('/register', method='POST')
def do_register():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = Base.InsertTableLogins(Base.Connect('Base'), username, password)
    base.close()
    if type(result) != int:
        return result
    else:
        if result == -7:
            return "<p>User with that name has already been.</p>"
        else:
            return "Strange error"


@get('/delete')  # or @route('/delete')
def delete():
    return '''
        <form action="/delete" method="post">
            Username: <input name="username" type="text" />
            <input value="delete" type="submit" />
        </form>
    '''


@post('/delete')  # or @route('/delete', method='POST')
def do_delete():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    result = Base.DeleteUser(base, username)
    base.close()
    if result == 0:
        return "<p>Successful delete.</p>"
    elif result == -10:
        return "<p>Update not successfully</p>"
    elif result == -2:
        return "Cursor not created</p>"
    else:
        return "Strange error"


@get('/password')  # or @route('/password')
def change_password():
    return '''
        <form action="/password" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            NewPassword: <input name="newpassword" type="password" />
            <input value="password" type="submit" />
        </form>
    '''


@post('/password')  # or @route('/password', method='POST')
def do_change_password():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    password = request.forms.get('password')
    newpassword = request.forms.get('newpassword')
    result = Base.CheckPassword(base, username, password)
    base.close()
    if type(result) != int:
        result = Base.UpdatePassword(base, username, newpassword)
        if result == 0:
            return "<p>Successful changes.</p>"
        elif result == -10:
            return "<p>Update not successfully</p>"
        elif result == -2:
            return "Cursor not created</p>"
        else:
            return "Strange error"
    else:
        return "Login Failed"


@route('/users')
def see_all_users():
    Users = ''
    base = Base.Connect('Base')
    Result = Base.GetAll(base, 'Users')
    base.close()
    for users in Result:
        Users = Users + users[0] + ' - ' + users[1] + ' - ' + str(users[2]) + ' - ' + str(users[3]) + ' | '
    return Users


@route('/ratings/users')
def see_users_rating():
    Users = ''
    base = Base.Connect('Base')
    Result = Base.GetAll(base, 'UsersRating')
    base.close()
    for users in Result:
        Users = Users + users[0] + ' - ' + str(users[1]) + ' - ' + users[2] + ' | '
    return Users


@get('/update')  # or @route('/update')
def update():
    return '''
        <form action="/update" method="post">
            Username: <input name="username" type="text" />
            Steps: <input name="steps" type="text" />
            Orders: <input name="orders" type="text" />
            <input value="update" type="submit" />
        </form>
    '''


@post('/update')  # or @route('/update', method='POST')
def do_update():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    steps = int(request.forms.get('steps'))
    orders = int(request.forms.get('orders'))
    result = Base.UpdateStepsAndOrders(base, username, steps, orders)
    base.close()
    if result == 0:
        return "<p>Successful update.</p>"
    elif result == -10:
        return "<p>Update not successfully</p>"
    elif result == -2:
        return "Cursor not created</p>"
    else:
        return "Strange error"


@get('/name')  # or @route('/name')
def name():
    return '''
        <form action="/name" method="post">
            Username: <input name="username" type="text" />
            NewUsername: <input name="newusername" type="text" />
            <input value="name" type="submit" />
        </form>
    '''


@post('/name')  # or @route('/name', method='POST')
def do_name():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    newusername = request.forms.get('newusername')
    result = Base.UpdateName(base, username, newusername)
    base.close()
    if result == 0:
        return "<p>Successful update.</p>"
    elif result == -10:
        return "<p>Update not successfully</p>"
    elif result == -2:
        return "Cursor not created</p>"
    else:
        return "Strange error"


@get('/ratings/add')  # or @route('/ratings/add')
def add_rating():
    return '''
        <form action="/ratings/add" method="post">
            Map: <input name="map" type="text" />
            Rating: <input name="rating" type="text" />
            Username: <input name="username" type="text" />
            <input value="add" type="submit" />
        </form>
    '''


@post('/ratings/add')  # or @route('/ratings/add', method='POST')
def add_rating():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    maps = request.forms.get('map')
    rating = request.forms.get('rating')
    result = Base.AddRating(base, maps, rating, username)
    base.close()
    if result == 0:
        return "Successful added"
    else:
        return result


@get('/ratings/change')  # or @route('/ratings/change')
def change_rating():
    return '''
        <form action="/ratings/change" method="post">
            Map: <input name="map" type="text" />
            Rating: <input name="rating" type="text" />
            Username: <input name="username" type="text" />
            <input value="change" type="submit" />
        </form>
    '''


@post('/ratings/change')  # or @route('/ratings/change', method='POST')
def do_change_rating():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    maps = request.forms.get('map')
    rating = request.forms.get('rating')
    result = Base.ChangeRating(base, maps, rating, username)
    base.close()
    if result == 0:
        return "Successful added"
    else:
        return result


@get('/ratings/get')  # or @route('/ratings/get')
def get_rating_by_user():
    return '''
        <form action="/ratings/get" method="post">
            Username: <input name="username" type="text" />
            <input value="get" type="submit" />
        </form>
    '''


@post('/ratings/get')  # or @route('/ratings/get', method='POST')
def do_get_rating_by_user():
    base = Base.Connect('Base')
    Users = ''
    username = request.forms.get('username')
    result = Base.GetRatingByUser(base, username)
    base.close()
    if type(result) != int:
        for users in result:
            Users = Users + users[0] + ' - ' + str(users[1]) + ' - ' + users[2] + ' | '
        return Users
    else:
        return result


run(host='localhost', port=8080)
