from bottle import route, run, request, post, get
import DataBaseForRestGuy as Base

# LIST OF FUNCTIONS
#   LOGINS
#       1) InsertTableLogins - register                     - added to request
#       2) CheckPassword - login                            - added to request
#       3) UpdateStepsAndOrders - update                    - added to request
#       4) UpdatePassword - change_password                 - added to request
#       5) UpdateName - name                                - added to request
#       6) DeleteUser - delete                              - added to request
#       7) GetAll - see_all_users                           - added to request
#   RATING BY USER
#       1) AddRating - add_rating                           - added to request
#       2) ChangeRating - change_rating                     - added to request
#       3) DeleteRatingByMap - delete_rating_by_map         - added to request
#       4) DeleteRatingByUser - do_delete_rating_by_user    - added to request
#       5) GetRatingByUser - get_rating_by_user             - added to request
#       7) GetAll - see_users_rating                        - added to request
#   RATING
#       1) GetAll - see_maps_rating                         - added to request


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
        return "Login failed."


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
    if result != 0:
        return result
    else:
        if result == -7:
            return "User with that name has already been."
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
        return "Successful delete."
    elif result == -10:
        return "Update not successfully"
    elif result == -2:
        return "Cursor not created"
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
    if type(result) != int:
        result = Base.UpdatePassword(base, username, newpassword)
        base.close()
        if result == 0:
            return "Successful changes."
        elif result == -10:
            return "Update not successfully"
        elif result == -2:
            return "Cursor not created"
        else:
            return "Strange error"
    else:
        base.close()
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


@route('/ratings')
def see_maps_rating():
    Maps = ''
    base = Base.Connect('Base')
    Result = Base.GetAll(base, 'MapRating')
    base.close()
    for maps in Result:
        Maps = Maps + maps[0] + ' - ' + str(maps[1]) + ' - ' + str(maps[2]) + ' | '
    return Maps


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
        return "Successful update."
    elif result == -10:
        return "Update not successfully"
    elif result == -2:
        return "Cursor not created"
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
        return "Successful update."
    elif result == -10:
        return "Update not successfully"
    elif result == -2:
        return "Cursor not created"
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


@get('/ratings/delete/map')  # or @route('/ratings/delete/map')
def delete_rating_by_map():
    return '''
        <form action="/ratings/delete/map" method="post">
            Map: <input name="map" type="text" />
            <input value="delete_rating_by_map" type="submit" />
        </form>
    '''


@post('/ratings/delete/map')  # or @route('/ratings/delete/map', method='POST')
def do_delete_rating_by_map():
    base = Base.Connect('Base')
    maps = request.forms.get('map')
    result = Base.DeleteRatingByMap(base, maps)
    base.close()
    if result == 0:
        return "Successful delete"
    elif result == -10:
        return "Update not successfully"
    elif result == -2:
        return "Cursor not created"
    else:
        return "Strange error"


@get('/ratings/delete/user')  # or @route('/ratings/delete/user')
def delete_rating_by_user():
    return '''
        <form action="/ratings/delete/user" method="post">
            Username: <input name="username" type="text" />
            <input value="delete_rating_by_user" type="submit" />
        </form>
    '''


@post('/ratings/delete/user')  # or @route('/ratings/delete/user', method='POST')
def do_delete_rating_by_user():
    base = Base.Connect('Base')
    username = request.forms.get('username')
    result = Base.DeleteRatingByUser(base, username)
    base.close()
    if result == 0:
        return "Successful delete."
    elif result == -10:
        return "Update not successfully"
    elif result == -2:
        return "Cursor not created"
    else:
        return "Strange error"


run(host='localhost', port=8080)
# run(host='0.0.0.0', port=8080)
