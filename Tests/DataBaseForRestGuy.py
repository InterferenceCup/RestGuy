import sqlite3


# ERRORS
#   -1. Base not connected
#   -2. Cursor not created
#   -3. Table can't be created
#   -4. Can't select all
#   -5. Can't add element
#   -6. Can't select one element
#   -7. Element has already been \ -6 error
#   -8. Incorrect password
#   -9. Can't find login because error
#   -10. Update not successful

# ALL
def Connect(string):
    try:
        Base = sqlite3.connect(string + '.db')
        return Base
    except:
        return -1


def CreateCursor(Base):
    try:
        Cursor = Base.cursor()
        return Cursor
    except:
        return -2


def CreateTable(Base, Name, Params):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Base.execute("CREATE TABLE " + Name + " (" + Params + ")")
            Base.commit()
            return 0
        except:
            return -3
    else:
        return -2


def GetAll(Base, Table):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT * FROM " + Table)
            return Cursor.fetchall()
        except:
            return -4
    else:
        return -2


# LOGINS
def InsertTableLogins(Base, Username, Password):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            if not FindLogin(Base, Username):
                values = (Username, Password, 0, 0)
                Cursor.execute("""
                             INSERT INTO
                             Users (username, password, steps, orders) 
                             VALUES (?, ?, ?, ?)
                             """,
                               values)
                Base.commit()
                return 0
            else:
                return -7
        except:
            return -5
    else:
        return -2


def FindLogin(Base, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT * FROM 'Users' WHERE username = '" + Username + "'")
            return Cursor.fetchall()
        except:
            return -6
    else:
        return -2


def CheckPassword(Base, Username, Password):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Original = FindLogin(Base, Username)
            if type(Original) != int:
                if Original[0][1] == Password:
                    return Username
                else:
                    return -8
            else:
                return Original
        except:
            return -9
    else:
        return -2


def UpdateStepsAndOrders(Base, Username, Steps, Orders):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("UPDATE 'Users' SET steps = "
                           + str(Steps) + ", orders = "
                           + str(Orders) + " WHERE username = '" + Username + "'")
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


def UpdatePassword(Base, Username, Password):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("UPDATE 'Users' SET password = '"
                           + Password + "' WHERE username = '" + Username + "'")
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


def UpdateName(Base, Username, NewUsername):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("UPDATE 'Users' SET username = '"
                           + NewUsername + "' WHERE username = '" + Username + "'")
            ChangeUserInRating(Base, Username, NewUsername)
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


def DeleteUser(Base, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("DELETE FROM 'Users' WHERE username = '" + Username + "'")
            DeleteRatingByUser(Base, Username)
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


# RATING BY USERS
def FindRatingByName(Base, Map, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT * FROM 'UsersRating' WHERE map = '" + Map + "' AND username = '" + Username + "'")
            return Cursor.fetchall()
        except:
            return -6
    else:
        return -2


def AddRating(Base, Map, Rating, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        if not FindRatingByName(Base, Map, Username):
            values = (Map, Rating, Username)
            Cursor.execute("""
                                     INSERT INTO
                                     'UsersRating' (map, rating, username) 
                                     VALUES (?, ?, ?)
                                     """,
                           values)
            if not FindReview(Base, Map):
                AddReview(Base, Map, Rating)
            else:
                UpdateRating(Base, Map, Rating)
            Base.commit()
            return 0
    else:
        return -2


def ChangeRating(Base, Map, Rating, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Rat = int(GetRatingByUser(Base, Username)[0][1])
            DeUpdateRating(Base, Map, Rat)
            if not FindReview(Base, Map):
                AddReview(Base, Map, Rating)
            else:
                UpdateRating(Base, Map, Rating)
            Cursor.execute("UPDATE 'UsersRating' SET rating = "
                           + str(Rating)
                           + " WHERE map = '" + Map + "' AND username = '" + Username + "'")
            Base.commit()
            return 0
        except:
            return -5
    else:
        return -2


def DeleteRatingByMap(Base, Map):
    CursorDelete = CreateCursor(Base)
    if CursorDelete != -2:
        try:
            CursorDelete.execute("DELETE FROM 'UsersRating' WHERE map = '" + Map + "'")
            print(DeleteRating(Base, Map))
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


def DeleteRatingByUser(Base, Username):
    CursorFindMaps = CreateCursor(Base)
    CursorDelete = CreateCursor(Base)
    if CursorFindMaps != -2 and CursorDelete != -2:
        try:
            CursorFindMaps.execute("SELECT * FROM 'UsersRating' WHERE username = '" + Username + "'")
            Result = CursorFindMaps.fetchall()
            print(Result)
            for result in Result:

                DeUpdateRating(Base, result[0], result[1])

            CursorDelete.execute("DELETE FROM 'UsersRating' WHERE username = '" + Username + "'")
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


def GetRatingByUser(Base, Username):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT * FROM 'UsersRating' WHERE username = '" + Username + "'")
            return Cursor.fetchall()
        except:
            return -6
    else:
        return -2


def ChangeUserInRating(Base, Username, NewUsername):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("UPDATE 'UsersRating' SET username = '"
                           + NewUsername
                           + "' WHERE username = '" + Username + "'")
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2


# RATING
def FindReview(Base, Map):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT * FROM 'MapRating' WHERE map = '" + Map + "'")
            return Cursor.fetchall()
        except:
            return -6
    else:
        return -2


def AddReview(Base, Map, Rating):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            values = (Map, Rating, 1)
            Cursor.execute("""
                           INSERT INTO
                           'MapRating' (map, rating, review) 
                           VALUES (?, ?, ?)
                           """,
                           values)
            Base.commit()
            return 0
        except:
            return -5
    else:
        return -2


def GetRating(Base, Map):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT rating FROM 'MapRating' WHERE map = '" + Map + "'")
            Result = Cursor.fetchall()
            if Result:
                return Result[0][0]
        except:
            return -6
    else:
        return -2


def GetReview(Base, Map):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("SELECT review FROM 'MapRating' WHERE map = '" + Map + "'")
            return Cursor.fetchall()[0][0]
        except:
            return -6
    else:
        return -2


def UpdateRating(Base, Map, Rating):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Review = GetReview(Base, Map)
            Rat = int(GetRating(Base, Map))
            Review = Review + 1
            print(Rat)
            print(Rating)
            Rat = (Rat + int(Rating)) / 2
            Cursor.execute("UPDATE 'MapRating' SET rating = "
                           + str(Rat) + ", review = " + str(Review) +
                           " WHERE map = '" + Map + "'")
            Base.commit()
            return 0
        except:
            return -6
    else:
        return -2


def DeUpdateRating(Base, Map, Rating):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Review = int(GetReview(Base, Map))
            Rat = int(GetRating(Base, Map))
            Review = Review - 1
            if Review != 0:
                Rat = (Rat * (Review + 1) - int(Rating)) / Review
                Cursor.execute("UPDATE 'MapRating' "
                               "SET rating = " + str(Rat) + ", review = " + str(Review) +
                               " WHERE map = '" + Map + "'")
            else:
                DeleteRating(Base, Map)
            Base.commit()
            return 0
        except:
            return -6
    else:
        return -2


def DeleteRating(Base, Map):
    Cursor = CreateCursor(Base)
    if Cursor != -2:
        try:
            Cursor.execute("DELETE FROM 'MapRating' WHERE map = '" + Map + "'")
            Base.commit()
            return 0
        except:
            return -10
    else:
        return -2
'''
def main():
    Base = Connect("Base")
    if Base != -1:
        print(UpdateRating(Base, 'map1'))
        Base.close()
    else:
        print("Base not created")


main()
'''