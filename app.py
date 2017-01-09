import os
import datetime

from flask import Flask, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from keys import *

app = Flask(__name__)
mysql = MySQL()
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = YOUR_MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = YOUR_MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = YOUR_MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = YOUR_MYSQL_DATABASE_HOST
mysql.init_app(app)


# ---------- UTILITY ROUTES ----------
@app.route('/')
def main():
    return "You are on the index page of Friend Match!"


@app.route('/test')
def test():
    return json.dumps({'message': 'Friend Match working.', 'code': 200})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return json.dumps({'message': 'Unauthorised access.', 'code': 401})
        return f(*args, **kwargs)

    return decorated_function


# ---------- SIGN-IN/SIGN-OUT ROUTES ----------
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    cursor = None
    con = None
    try:
        _name = request.args['inputName']
        _email = request.args['inputEmail']
        _password = request.args['inputPassword']

        # validate the received values
        if _name and _email and _password:

            con = mysql.connect()
            cursor = con.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                con.commit()
                return json.dumps({'message': 'User created successfully.', 'code': 201})
            else:
                return json.dumps({'message': str(data[0]), 'code': 400})
        else:
            return json.dumps({'message': 'Invalid input', 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/validate_login', methods=['POST'])
def validate_login():
    cursor = None
    con = None
    try:
        _email = request.args['inputEmail']
        _password = request.args['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_email,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return json.dumps({'message': 'User validated.', 'user_id': data[0][0], 'code': 200})
            else:
                return json.dumps({'message': 'Incorrect username or password.', 'code': 401})
        else:
            return json.dumps({'message': 'Incorrect username or password.', 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user', None)
        return json.dumps({'message': 'Logged Out.', 'code': 200})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


# ---------- GET ALL ROUTES ----------
@app.route('/all/hobby')
@login_required
def get_all_hobbies():
    con = None
    cursor = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getAllHobbies')
        result1 = cursor.fetchall()

        hobby_dict = []

        for hobby in result1:
            user_id = session.get('user')
            cursor.callproc('sp_isUserHobby',
                            (user_id, hobby[0]))
            result2 = cursor.fetchall()

            if result2[0][0] == "TRUE":
                h_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1],
                    'is_user_hobby': True
                }
            else:
                h_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1],
                    'is_user_hobby': False
                }

            hobby_dict.append(h_dict)

        return json.dumps({'message': {'hobby': hobby_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/all/event')
@login_required
def get_all_events():
    con = None
    cursor = None
    now = datetime.datetime.now()
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getAllEvents', (now.strftime("%Y-%m-%d"),))
        result1 = cursor.fetchall()

        event_dict = []

        for event in result1:
            user_id = session.get('user')
            cursor.callproc('sp_isAttending',
                            (user_id, event[0]))
            result2 = cursor.fetchall()

            if result2[0][0] == "TRUE":
                e_dict = {
                    'event_id': event[0],
                    'event_name': event[1],
                    'event_city': event[2],
                    'event_date': event[3].strftime("%Y-%m-%d"),
                    'is_user_attending': True
                }
            else:
                e_dict = {
                    'event_id': event[0],
                    'event_name': event[1],
                    'event_city': event[2],
                    'event_date': event[3].strftime("%Y-%m-%d"),
                    'is_user_attending': False
                }

            event_dict.append(e_dict)

        return json.dumps({'message': {'event': event_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


# ---------- CURRENT USER ROUTES ----------
@app.route('/user/info')
@login_required
def get_my_info():
    try:
        user_id = session.get('user')
        return redirect(url_for('get_user_info', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/friends')
@login_required
def get_my_friends():
    try:
        user_id = session.get('user')
        return redirect(url_for('get_user_friends', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/hobby')
@login_required
def get_my_hobby():
    try:
        user_id = session.get('user')
        return redirect(url_for('get_user_hobby', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/event')
@login_required
def get_my_event():
    try:
        user_id = session.get('user')
        return redirect(url_for('get_user_event', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/common/hobby/<int:user_id>')
@login_required
def get_my_common_hobbies_with(user_id):
    try:
        user_id_1 = session.get('user')
        user_id_2 = user_id
        return redirect(url_for('get_common_hobbies_between', user_id_1=user_id_1, user_id_2=user_id_2))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/related/hobby/<int:user_id>')
@login_required
def get_my_related_hobbies_with(user_id):
    try:
        user_id_1 = session.get('user')
        user_id_2 = user_id
        return redirect(url_for('get_related_hobbies_between', user_id_1=user_id_1, user_id_2=user_id_2))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/profile')
@login_required
def get_my_profile():
    try:
        user_id = session.get('user')
        return redirect(url_for('get_user_profile', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/suggest/friends')
@login_required
def suggest_my_friends():
    try:
        user_id = session.get('user')
        return redirect(url_for('suggest_user_friends', user_id=user_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/suggest/events')
def suggest_my_events():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('suggest_user_events', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/add/friend/<int:user_id>')
@login_required
def add_my_friend(user_id):
    try:
        user_id_1 = session.get('user')
        user_id_2 = user_id
        return redirect(url_for('add_user_friend', user_id_1=user_id_1, user_id_2=user_id_2))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/delete/friend/<int:user_id>')
@login_required
def delete_my_friend(user_id):
    try:
        user_id_1 = session.get('user')
        user_id_2 = user_id
        return redirect(url_for('delete_user_friend', user_id_1=user_id_1, user_id_2=user_id_2))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/add/event/<int:event_id>')
@login_required
def add_my_event(event_id):
    try:
        user_id = session.get('user')
        return redirect(url_for('add_user_event', user_id=user_id, event_id=event_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/delete/event/<int:event_id>')
@login_required
def delete_my_event(event_id):
    try:
        user_id = session.get('user')
        return redirect(url_for('delete_user_event', user_id=user_id, event_id=event_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/add/hobby/<int:hobby_id>')
@login_required
def add_my_hobby(hobby_id):
    try:
        user_id = session.get('user')
        return redirect(url_for('add_user_hobby', user_id=user_id, hobby_id=hobby_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


@app.route('/user/delete/hobby/<int:hobby_id>')
@login_required
def delete_my_hobby(hobby_id):
    try:
        user_id = session.get('user')
        return redirect(url_for('delete_user_hobby', user_id=user_id, hobby_id=hobby_id))

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})


# ---------- OTHER USER ROUTES ----------
@app.route('/user/<int:user_id>/info')
@login_required
def get_user_info(user_id):
    cursor = None
    con = None
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getUserInfo', (_req_user,))
        result = cursor.fetchall()

        info = {
            'id': result[0][0],
            'user_name': result[0][1],
            'user_email': result[0][2],
            'age': result[0][3],
            'gender': result[0][4],
            'city': result[0][5],
            'location': result[0][6],
            'phone_number': result[0][7]
        }
        return json.dumps({'message': {'info': info}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/friends')
@login_required
def get_user_friends(user_id):
    cursor = None
    con = None
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getUserFriends', (_req_user,))
        result1 = cursor.fetchall()

        friends_dict = []

        if _req_user == session.get('user'):
            for info in result1:
                info_dict = {
                    'friend_id': info[0],
                    'user_name': info[1],
                    'gender': info[2],
                    'is_your_friend': True
                }
                friends_dict.append(info_dict)

        else:
            for info in result1:
                cursor.callproc('sp_isFriend', (session.get('user'), info[0]))
                result2 = cursor.fetchall()

                if result2[0][0] == "TRUE":
                    info_dict = {
                        'friend_id': info[0],
                        'user_name': info[1],
                        'gender': info[2],
                        'is_your_friend': True
                    }
                else:
                    info_dict = {
                        'friend_id': info[0],
                        'user_name': info[1],
                        'gender': info[2],
                        'is_your_friend': False
                    }
                friends_dict.append(info_dict)

        return json.dumps({'message': {'friends': friends_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/hobby')
@login_required
def get_user_hobby(user_id):
    cursor = None
    con = None
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getUserHobby', (_req_user,))
        result1 = cursor.fetchall()

        hobby_dict = []

        if _req_user == session.get('user'):
            for hobby in result1:
                h_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1],
                    'is_user_hobby': True
                }
                hobby_dict.append(h_dict)

        else:
            for hobby in result1:
                cursor.callproc('sp_isUserHobby',
                                (session.get('user'), hobby[0]))
                result2 = cursor.fetchall()

                if result2[0][0] == "TRUE":
                    h_dict = {
                        'hobby_id': hobby[0],
                        'hobby_name': hobby[1],
                        'is_user_hobby': True
                    }
                else:
                    h_dict = {
                        'hobby_id': hobby[0],
                        'hobby_name': hobby[1],
                        'is_user_hobby': False
                    }
                hobby_dict.append(h_dict)

        return json.dumps({'message': {'hobby': hobby_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/event')
@login_required
def get_user_event(user_id):
    cursor = None
    con = None
    now = datetime.datetime.now()
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getUserEvent',
                        (_req_user, now.strftime("%Y-%m-%d")))
        result1 = cursor.fetchall()

        event_dict = []

        if _req_user == session.get('user'):
            for event in result1:
                e_dict = {
                    'event_id': event[0],
                    'event_name': event[1],
                    'event_city': event[2],
                    'event_date': event[3].strftime("%Y-%m-%d"),
                    'is_user_attending': True
                }
                event_dict.append(e_dict)

        else:
            for event in result1:
                cursor.callproc('sp_isAttending',
                                (session.get('user'), event[0]))
                result2 = cursor.fetchall()

                if result2[0][0] == "TRUE":
                    e_dict = {
                        'event_id': event[0],
                        'event_name': event[1],
                        'event_city': event[2],
                        'event_date': event[3].strftime("%Y-%m-%d"),
                        'is_user_attending': True
                    }
                else:
                    e_dict = {
                        'event_id': event[0],
                        'event_name': event[1],
                        'event_city': event[2],
                        'event_date': event[3].strftime("%Y-%m-%d"),
                        'is_user_attending': False
                    }
                event_dict.append(e_dict)

        return json.dumps({'message': {'event': event_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id_1>/common/hobby/<int:user_id_2>')
@login_required
def get_common_hobbies_between(user_id_1, user_id_2):
    cursor = None
    con = None
    try:
        _user_id_1 = user_id_1
        _user_id_2 = user_id_2

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_showCommonHobby',
                        (_user_id_1, _user_id_2))
        result = cursor.fetchall()

        common_hobby_dict = []

        if _user_id_1 != _user_id_2:
            for hobby in result:
                hobby_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1],
                    'is_user_hobby': True
                }
                common_hobby_dict.append(hobby_dict)
            return json.dumps({'message': {'common_hobby': common_hobby_dict}, 'code': 200})

        else:
            return json.dumps({'message': {
                'common_hobby': "Self. No need to show common hobbies."},
                'code': 204})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id_1>/related/hobby/<int:user_id_2>')
@login_required
def get_related_hobbies_between(user_id_1, user_id_2):
    cursor = None
    con = None
    try:
        _user_id_1 = user_id_1
        _user_id_2 = user_id_2

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_isFriend', (_user_id_1, _user_id_2))
        result1 = cursor.fetchall()

        related_hobby_dict = []

        if result1[0][0] == "FALSE" and _user_id_1 != _user_id_2:
            cursor.callproc('sp_showRelatedHobby',
                            (_user_id_1, _user_id_2))
            result2 = cursor.fetchall()

            for hobby in result2:
                hobby_dict = {
                    'related_hobby_id': hobby[0],
                    'hobby_name': hobby[1],
                    'is_user_hobby': False  # not yet added to hobby list that is why not in common hobby
                }
                related_hobby_dict.append(hobby_dict)

            return json.dumps({'message': {'related_hobby': related_hobby_dict}, 'code': 200})

        else:
            return json.dumps({'message': {
                'related_hobby': "Friends/Self. No need to show related hobbies."},
                'code': 204})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


# ---------- ADD/DELETE ROUTES ----------
@app.route('/user/<int:user_id_1>/add/friend/<int:user_id_2>')
@login_required
def add_user_friend(user_id_1, user_id_2):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_addUserFriend', (user_id_1, user_id_2))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Friend added successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id_1>/delete/friend/<int:user_id_2>')
@login_required
def delete_user_friend(user_id_1, user_id_2):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_deleteUserFriend', (user_id_1, user_id_2))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Friend deleted successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/add/event/<int:event_id>')
@login_required
def add_user_event(user_id, event_id):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_addUserEvent', (user_id, event_id))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Event added successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/delete/event/<int:event_id>')
@login_required
def delete_user_event(user_id, event_id):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_deleteUserEvent', (user_id, event_id))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Event deleted successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/add/hobby/<int:hobby_id>')
@login_required
def add_user_hobby(user_id, hobby_id):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_addUserHobby', (user_id, hobby_id))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Hobby added successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/delete/hobby/<int:hobby_id>')
@login_required
def delete_user_hobby(user_id, hobby_id):
    cursor = None
    con = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_deleteUserHobby', (user_id, hobby_id))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return json.dumps({'message': 'Hobby deleted successfully.', 'code': 200})
        else:
            return json.dumps({'message': str(data[0]), 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


# ---------- SUGGESTION ROUTES ----------
@app.route('/user/<int:user_id>/suggest/events')
@login_required
def suggest_user_events(user_id):
    cursor = None
    con = None
    now = datetime.datetime.now()
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_suggestEvent',
                        (_req_user, now.strftime("%Y-%m-%d")))
        result = cursor.fetchall()

        event_dict = []

        for event in result:
            e_dict = {
                'event_id': event[0],
                'event_name': event[1],
                'event_city': event[2],
                'event_date': event[3].strftime("%Y-%m-%d")
            }
            event_dict.append(e_dict)

        return json.dumps({'message': {'suggested_event': event_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/suggest/friends')
@login_required
def suggest_user_friends(user_id):
    cursor = None
    con = None
    try:
        _req_user = user_id

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_suggestFriend', (_req_user,))
        result = cursor.fetchall()

        suggestion_dict = []

        for friend in result:
            suggestion = {
                'id': friend[0],
                'user_name': friend[1],
                'age': friend[2],
                'gender': friend[3]
            }
            suggestion_dict.append(suggestion)

        return json.dumps({'message': {'suggestions': suggestion_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


# ---------- PROFILE ROUTES ----------
@app.route('/user/<int:user_id>/profile')
@login_required
def get_user_profile(user_id):
    _req_user = user_id

    # fetch user info
    user_info = json.loads(get_user_info(_req_user))
    info = user_info['message']['info']
    code_i = user_info['code']

    # fetch user friends
    friends_dict = json.loads(get_user_friends(_req_user))
    friends = friends_dict['message']['friends']
    code_f = friends_dict['code']

    # fetch user hobby
    hobby_dict = json.loads(get_user_hobby(_req_user))
    hobby = hobby_dict['message']['hobby']
    code_h = hobby_dict['code']

    # fetch user events
    event_dict = json.loads(get_user_event(_req_user))
    event = event_dict['message']['event']
    code_e = event_dict['code']

    # show common and related hobby if not checking own profile
    if session.get('user') != _req_user:
        _user_id_1 = session.get('user')
        _user_id_2 = _req_user

        common_hobby_dict = json.loads(get_common_hobbies_between(
            _user_id_1, _user_id_2))
        common_hobby = common_hobby_dict['message']['common_hobby']
        code_ch = common_hobby_dict['code']

        related_hobby_dict = json.loads(get_related_hobbies_between(
            _user_id_1, _user_id_2))
        related_hobby = related_hobby_dict['message']['related_hobby']
        code_rh = related_hobby_dict['code']

    else:
        common_hobby = "Self. No need to show common hobbies."
        code_ch = 204

        related_hobby = "Self. No need to show related hobbies."
        code_rh = 204

    final_list = []
    ij = {'info': info, 'code': code_i}
    fj = {'friends': friends, 'code': code_f}
    hj = {'hobby': hobby, 'code': code_h}
    chj = {'common_hobby': common_hobby, 'code': code_ch}
    rhj = {'related_hobby': related_hobby, 'code': code_rh}
    ej = {'event': event, 'code': code_e}

    final_list.append(ij)
    final_list.append(fj)
    final_list.append(hj)
    final_list.append(chj)
    final_list.append(rhj)
    final_list.append(ej)

    return json.dumps({'message': final_list, 'code': 200})


@app.route('/user/<int:user_id>/edit/profile', methods=['POST'])
@login_required
def edit_user_profile(user_id):
    cursor = None
    con = None
    try:
        _gender = request.args['gender']
        _age = request.args['age']
        _phone = request.args['phone']
        _location = request.args['location']
        _city = request.args['city']

        if _gender and _age and _phone and _location and _city:

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_updateProfile',
                            (user_id, _gender, _age,
                             _phone, _location, _city))
            data = cursor.fetchall()

            if len(data) is 0:
                con.commit()
                return json.dumps({'message': 'User updated successfully.', 'code': 200})
            else:
                return json.dumps({'message': str(data[0]), 'code': 400})

        else:
            return json.dumps({'message': 'Invalid input', 'code': 400})

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
