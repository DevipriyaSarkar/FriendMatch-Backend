import os

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
                return json.dumps({'message': 'User validated.', 'code': 200})
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
        return redirect('/'), 200

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
                        'user_name': info[1]
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
                hobby_dict.append(hobby[0])

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
                common_hobby_dict.append(hobby[0])

            return json.dumps({'message': {'common_hobby': common_hobby_dict}, 'code': 200})

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

        user_info = None
        friends_dict = []
        suggestion_dict = []
        hobby_dict = []
        common_hobby_dict = []

        code_i = code_f = code_s = code_h =  code_ch = 400
        con1 = con2 = con3 = con4 = con5 = None
        cursor1 = cursor2 = cursor3 = cursor4 = cursor5 = None

        # fetch user info
        try:
            con1 = mysql.connect()
            cursor1 = con1.cursor()

            cursor1.callproc('sp_getUserInfo', (_req_user,))
            result = cursor1.fetchall()

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

        finally:
            cursor1.close()
            con1.close()

        # fetch user friends
        try:
            con2 = mysql.connect()
            cursor2 = con2.cursor()

            cursor2.callproc('sp_getUserFriends', (_req_user, ))
            result = cursor2.fetchall()

            for info in result:
                info_dict = {
                        'friend_id': info[0],
                        'user_name': info[1]
                    }
                friends_dict.append(info_dict)

            code_f = 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor2.close()
            con2.close()

        # fetch user friend suggestion
        try:
            con3 = mysql.connect()
            cursor3 = con3.cursor()

            cursor3.callproc('sp_suggestFriend', (_req_user,))
            result = cursor3.fetchall()

            for friend in result:
                suggestion = {
                    'id': friend[0],
                    'user_name': friend[1],
                    'age': friend[2],
                    'gender': friend[3]
                }
                suggestion_dict.append(suggestion)

            code_s = 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor3.close()
            con3.close()

        # fetch user hobby
        try:
            con4 = mysql.connect()
            cursor4 = con4.cursor()

            cursor4.callproc('sp_getUserHobby', (_req_user,))
            result = cursor4.fetchall()

            for hobby in result:
                hobby_dict.append(hobby[0])

            code_h = 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

        finally:
            cursor4.close()
            con4.close()

        # show common hobby if not checking own profile
        if session.get('user') != _req_user:
            try:
                con5 = mysql.connect()
                cursor5 = con5.cursor()

                _user_id_1 = session.get('user')
                _user_id_2 = _req_user

                cursor5.callproc('sp_showCommonHobby', (_user_id_1, _user_id_2))
                result = cursor5.fetchall()

                for hobby in result:
                    common_hobby_dict.append(hobby[0])

                code_ch = 200

            except Exception as e:
                return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400})

            finally:
                cursor5.close()
                con5.close()

        else:
            code_ch = 403

        final_list = []
        ij = {'info': user_info, 'code': code_i}
        fj = {'friends': friends_dict, 'code': code_f}
        sj = {'suggestions': suggestion_dict, 'code': code_s}
        hj = {'hobby': hobby_dict, 'code': code_h}
        chj = {'common_hobby': common_hobby_dict, 'code': code_ch}

        final_list.append(ij)
        final_list.append(fj)
        final_list.append(sj)
        final_list.append(hj)
        final_list.append(chj)

        return json.dumps({'message': final_list, 'code': 200})

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
