import os

from flask import Flask, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
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
    return json.dumps({'message': 'Friend Match working.', 'code': 200}), 200


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
                return json.dumps({'message': 'User created successfully.', 'code':201}), 201
            else:
                return json.dumps({'message': str(data[0]), 'code': 400}), 400
        else:
            return json.dumps({'message': 'Invalid input', 'code': 400}), 400

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/validate_login', methods=['POST'])
def validate_login():
    cursor = None
    con = None
    try:
        _username = request.args['inputEmail']
        _password = request.args['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return json.dumps({'message': 'User validated.', 'code': 200}), 200
            else:
                return json.dumps({'message': 'Incorrect username or password.', 'code': 401}), 401
        else:
            return json.dumps({'message': 'Incorrect username or password.', 'code': 400}), 400

    except Exception as e:
        return json.dumps({'message': str(e), 'code': 400}), 400

    finally:
        cursor.close()
        con.close()


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/'), 200


@app.route('/user/info')
def get_my_info():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_info', user_id=user_id)), 302

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


@app.route('/user/friends')
def get_my_friends():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('get_user_friends', user_id=user_id)), 302

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


@app.route('/user/suggest/friends')
def suggest_my_friends():
    if session.get('user'):
        try:
            user_id = session.get('user')
            return redirect(url_for('suggest_user_friends', user_id=user_id)), 302

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


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
                    'age': result[0][2],
                    'gender': result[0][3],
                    'city': result[0][4],
                    'location': result[0][5],
                    'phone_number': result[0][6]
                }
            return json.dumps({'message': info, 'code': 200}), 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


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

            return json.dumps({'message': friends_dict, 'code': 200}), 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


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

            return json.dumps({'message': suggestion_dict, 'code': 200}), 200

        except Exception as e:
            return json.dumps({'message': 'Error: %s' % (str(e)), 'code': 400}), 400

        finally:
            cursor.close()
            con.close()

    else:
        return json.dumps({'message': 'Unauthorised access.', 'code': 401}), 401


if __name__ == '__main__':
    app.run()
