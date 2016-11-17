import os
import datetime

from flask import Flask, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'devipriya'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'friend_match'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Default setting
pageLimit = 5


@app.route('/')
def main():
    return "You are on the index page of Friend Match!"


@app.route('/test')
def test():
    return json.dumps({'message': 'Friend Match working.', 'code': 200})


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
        cursor.callproc('sp_validateLogin', (_email, ))
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


@app.route('/user/info')
def get_my_info():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_info', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/friends')
def get_my_friends():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_friends', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/suggest/friends')
def suggest_my_friends():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('suggest_user_friends', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/hobby')
def get_my_hobby():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_hobby', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/common/hobby/<int:user_id>')
def get_my_common_hobbies_with(user_id):
    if session.get('user'):
        try:
            user_id_1 = session.get('user')
            user_id_2 = user_id
            return redirect(url_for('get_common_hobbies_between', user_id_1=user_id_1, user_id_2=user_id_2))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/related/hobby/<int:user_id>')
def get_my_related_hobbies_with(user_id):
    if session.get('user'):
        try:
            user_id_1 = session.get('user')
            user_id_2 = user_id
            return redirect(url_for('get_related_hobbies_between', user_id_1=user_id_1, user_id_2=user_id_2))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/profile')
def get_my_profile():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_profile', user_id=user_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/add/friend/<int:user_id>')
def add_my_friend(user_id):
    if session.get('user'):
        try:
            user_id_1 = session.get('user')
            user_id_2 = user_id
            return redirect(url_for('add_user_friend', user_id_1=user_id_1, user_id_2=user_id_2))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/delete/friend/<int:user_id>')
def delete_my_friend(user_id):
    if session.get('user'):
        try:
            user_id_1 = session.get('user')
            user_id_2 = user_id
            return redirect(url_for('delete_user_friend', user_id_1=user_id_1, user_id_2=user_id_2))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/add/event/<int:hobby_id>')
def add_my_event(hobby_id):
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('add_user_event', user_id=user_id, hobby_id=hobby_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/delete/event/<int:hobby_id>')
def delete_my_event(hobby_id):
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('delete_user_event', user_id=user_id, hobby_id=hobby_id))

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/info')
def get_user_info(user_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _req_user = user_id

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_getUserInfo', (_req_user, ))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/friends')
def get_user_friends(user_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _req_user = user_id

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_getUserFriends', (_req_user, ))
            result = cursor.fetchall()

            friends_dict = []

            for info in result:
                info_dict = {
                    'friend_id': info[0],
                    'user_name': info[1],
                    'gender': info[2]
                }
                friends_dict.append(info_dict)

            return json.dumps({'message': {'friends': friends_dict}, 'code': 200})

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/suggest/friends')
def suggest_user_friends(user_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _req_user = user_id

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_suggestFriend', (_req_user, ))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/hobby')
def get_user_hobby(user_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _req_user = user_id

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_getUserHobby', (_req_user, ))
            result = cursor.fetchall()

            hobby_dict = []

            for hobby in result:
                h_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1]
                }
                hobby_dict.append(h_dict)

            return json.dumps({'message': {'hobby': hobby_dict}, 'code': 200})

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id_1>/common/hobby/<int:user_id_2>')
def get_common_hobbies_between(user_id_1, user_id_2):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _user_id_1 = user_id_1
            _user_id_2 = user_id_2

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_showCommonHobby', (_user_id_1, _user_id_2))
            result = cursor.fetchall()

            common_hobby_dict = []

            for hobby in result:
                hobby_dict = {
                    'hobby_id': hobby[0],
                    'hobby_name': hobby[1]
                }
                common_hobby_dict.append(hobby_dict)

            return json.dumps({'message': {'common_hobby': common_hobby_dict}, 'code': 200})

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id_1>/related/hobby/<int:user_id_2>')
def get_related_hobbies_between(user_id_1, user_id_2):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _user_id_1 = user_id_1
            _user_id_2 = user_id_2

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_isFriend', (_user_id_1, _user_id_2))
            result = cursor.fetchall()

            related_hobby_dict = []

            if result[0][0] == "FALSE":
                cursor.callproc('sp_showRelatedHobby', (_user_id_1, _user_id_2))
                result = cursor.fetchall()

                for hobby in result:
                    hobby_dict = {
                        'related_hobby_id': hobby[0],
                        'hobby_name': hobby[1]
                    }
                    related_hobby_dict.append(hobby_dict)

                return json.dumps({'message': {'related_hobby': related_hobby_dict}, 'code': 200})

            else:
                return json.dumps({'message': {'related_hobby': "Friends. No need to show related hobbies."}, 'code': 204})

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/profile')
def get_user_profile(user_id):
    if session.get('user'):

        _req_user = user_id
        _current_user = session.get('user')     # the one who called the route

        user_info = None
        friends_dict = []
        hobby_dict = []
        common_hobby_dict = []
        related_hobby_dict = []

        code_i = code_f = code_h = code_ch = code_rh = 400

        con = None
        cursor = None

        try:
            con = mysql.connect()
            cursor = con.cursor()

            # fetch user info
            try:
                cursor.callproc('sp_getUserInfo', (_req_user,))
                result = cursor.fetchall()

                user_info = {
                    'id': result[0][0],
                    'user_name': result[0][1],
                    'user_email': result[0][2],
                    'age': result[0][3],
                    'gender': result[0][4],
                    'city': result[0][5],
                    'location': result[0][6],
                    'phone_number': result[0][7]
                }

                code_i = 200

            except Exception as e:
                return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

            # fetch user friends
            try:

                cursor.callproc('sp_getUserFriends', (_req_user, ))
                result1 = cursor.fetchall()

                for info in result1:
                    cursor.callproc('sp_isFriend', (_current_user, info[0]))
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

                code_f = 200

            except Exception as e:
                return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

            # fetch user hobby
            try:

                cursor.callproc('sp_getUserHobby', (_req_user,))
                result = cursor.fetchall()

                for hobby in result:
                    h_dict = {
                        'hobby_id': hobby[0],
                        'hobby_name': hobby[1]
                    }
                    hobby_dict.append(h_dict)

                code_h = 200

            except Exception as e:
                return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

            # show common and related hobby if not checking own profile
            if session.get('user') != _req_user:
                try:

                    _user_id_1 = session.get('user')
                    _user_id_2 = _req_user

                    cursor.callproc('sp_showCommonHobby', (_user_id_1, _user_id_2))
                    result = cursor.fetchall()

                    for hobby in result:
                        h_dict = {
                            'hobby_id': hobby[0],
                            'hobby_name': hobby[1]
                        }
                        common_hobby_dict.append(h_dict)

                    code_ch = 200

                    cursor.callproc('sp_isFriend', (_user_id_1, _user_id_2))
                    result = cursor.fetchall()

                    if result[0][0] == "FALSE":
                        cursor.callproc('sp_showRelatedHobby', (_user_id_1, _user_id_2))
                        result = cursor.fetchall()

                        for hobby in result:
                            h_dict = {
                                'related_hobby_id': hobby[0],
                                'hobby_name': hobby[1]
                            }
                            related_hobby_dict.append(h_dict)

                        code_rh = 200

                    else:
                        code_rh = 204

                except Exception as e:
                    return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

            else:
                code_ch = 403
                code_rh = 403

            final_list = []
            ij = {'info': user_info, 'code': code_i}
            fj = {'friends': friends_dict, 'code': code_f}
            hj = {'hobby': hobby_dict, 'code': code_h}
            chj = {'common_hobby': common_hobby_dict, 'code': code_ch}
            rhj = {'related_hobby': related_hobby_dict, 'code': code_rh}

            if code_rh == 204:
                rhj = {'related_hobby': "Friends. No need to show related hobbies.", 'code': code_rh}

            final_list.append(ij)
            final_list.append(fj)
            final_list.append(hj)
            final_list.append(chj)
            final_list.append(rhj)

            return json.dumps({'message': final_list, 'code': 200})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/edit/profile', methods=['POST'])
def edit_user_profile(user_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            _gender = request.args['gender']
            _age = request.args['age']
            _phone = request.args['phone']
            _location = request.args['location']
            _city = request.args['city']
            _hobby_list = request.json

            print _hobby_list

            if _gender and _age and _phone and _location and _city and _hobby_list:

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_updateProfile', (user_id, _gender, _age, _phone, _location, _city))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id_1>/add/friend/<int:user_id_2>')
def add_user_friend(user_id_1, user_id_2):
    if session.get('user'):
        cursor = None
        con = None
        try:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_addFriend', (user_id_1, user_id_2))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id_1>/delete/friend/<int:user_id_2>')
def delete_user_friend(user_id_1, user_id_2):
    if session.get('user'):
        cursor = None
        con = None
        try:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_deleteFriend', (user_id_1, user_id_2))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/all/hobby')
def get_all_hobbies():
    con = None
    cursor = None
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getAllHobbies')
        result = cursor.fetchall()

        hobby_dict = []

        for hobby in result:
            h_dict = {
                'hobby_id': hobby[0],
                'hobby_name': hobby[1]
            }
            hobby_dict.append(h_dict)

        return json.dumps({'message': {'hobby': hobby_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/all/event')
def get_all_events():
    con = None
    cursor = None
    now = datetime.datetime.now()
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_getAllEvents', (now.strftime("%Y-%m-%d"), ))
        result = cursor.fetchall()

        event_dict = []

        for event in result:
            e_dict = {
                'event_id': event[0],
                'event_name': event[1],
                'event_city': event[2],
                'event_date': event[3]
            }
            event_dict.append(e_dict)

        return json.dumps({'message': {'event': event_dict}, 'code': 200})

    except Exception as e:
        return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

    finally:
        cursor.close()
        con.close()


@app.route('/user/<int:user_id>/add/event/<int:hobby_id>')
def add_user_event(user_id, hobby_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_addEvent', (user_id, hobby_id))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/delete/friend/<int:hobby_id>')
def delete_user_event(user_id, hobby_id):
    if session.get('user'):
        cursor = None
        con = None
        try:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_deleteFriend', (user_id, hobby_id))
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

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


@app.route('/user/<int:user_id>/suggest/events')
def suggest_user_events(user_id):
    if session.get('user'):
        cursor = None
        con = None
        now = datetime.datetime.now()
        try:
            _req_user = user_id

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_suggestEvent', (_req_user, now.strftime("%Y-%m-%d")))
            result = cursor.fetchall()

            event_dict = []

            for event in result:
                e_dict = {
                    'event_id': event[0],
                    'event_name': event[1],
                    'event_city': event[2],
                    'event_date': event[3]
                }
                event_dict.append(e_dict)

            return json.dumps({'message': {'suggested_event': event_dict}, 'code': 200})

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
