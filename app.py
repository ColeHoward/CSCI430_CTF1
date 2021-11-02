from website import create_app
import random
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website.databases import db
from flask import render_template, request, flash, jsonify, redirect, url_for, g, request, make_response
# from flask_login import login_required, current_user, fresh_login_required, logout_user
import json
from functools import wraps

app = create_app()
app.secret_key = 'dxJO>BQ,7FXsw^s[t*8mC`<&]o|d@F'

blacklist = []
MAX_ATTEMPTS = 10


# @app.before_request
# def before_request():
#     print('before_request')
#     if 'user_id' in session:
#         print('session active')
#         user = User.query.filter_by(id=session['user_id']).first()
#         g.user = user
#     else:
#         print('session inactive')
#         redirect(url_for('login'))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in request.cookies:
            return func(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        # session.pop('user_id', None)
        username = request.args.get('user')
        password = request.args.get('pass')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # session['user_id'] = user.id
                # session.permanent = True
                user.is_authenticated = True
                db.session.commit()
                resp = make_response(redirect(url_for('manage')))
                print('cookie id: ' + str(user.id))
                resp.set_cookie('user_id', value=str(user.id), max_age=1500, samesite='Lax')
                # may neede to set g.user = user here and then say user is authenticated
                # g.user = user
                print(F'user_id: {str(user.id)}')
                # login_user(user, remember=True)  # stays until webserver is restarted
                return resp
        elif username is not None:
            flash("Incorrect username or password. Try again.", category="error")
            return render_template('fail.html')

    return render_template('login.html')


@app.route('/logout')
# @login_required  # ensures we can't access this route unless the user is logged in
def logout():
    # current_user.alternative_id = random(0, 100000)
    # logout_user()
    # if 'user_id' in session:
    #     g.user.is_authenticated = False
    # session.permanent = True
    # db.session.commit()
    # session.pop('user_id', None)
    cookie = request.cookies.get('user_id')
    user = User.query.filter_by(id=cookie).first()
    user.is_authenticated = False
    db.session.commit()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('user_id', value='', max_age=1)

    # resp.delete_cookie('user_id')
    return resp
    # return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def signup():
    # make sure to encrypt usernames
    if request.method == "GET":
        username = request.args.get('user')
        password = request.args.get('pass')

        user = User.query.filter_by(username=username).first()
        if user:
            flash("This username already exists. Try again.", category="error")
        elif password is not None:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'), balance=0,
                            action_type='deposit')
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            # login_user(g.user, remember=True)  # stays until webserver is restarted
            return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    # if 'user_id' in session:
    #     print('session active home create g.user')
    #     user = User.query.filter_by(id=session['user_id']).first()
    #     g.user = user
    # if 'user_id' not in session:
    #     print('has user id in home')
    #     redirect(url_for('login'))
    # print('no user id in home')
    cookie = request.cookies.get('user_id')
    if not cookie or cookie == '':
        return redirect(url_for('login'))
    resp = make_response(render_template('home.html'))
    resp.set_cookie('user_id', value=cookie, max_age=1500, samesite='Lax')
    return resp
    # we then need to register these blueprints in __init__.py
    # current_user allows us to reference the user that is logged in


@app.route('/update-content', methods=['GET', 'POST'])
# @login_required
def update_content():
    # if 'user_id' in session:
    #     print('session active update content')
    #     user = User.query.filter_by(id=session['user_id']).first()
    #     g.user = user
    cookie = request.cookies.get('user_id')
    user = User.query.filter_by(id=int(cookie)).first()
    print('update content')
    message = json.loads(request.data)
    content_type = message['content_type']
    user.action_type = content_type
    db.session.commit()
    return jsonify({})


@app.route('/manage', methods=['GET'])
# @login_required
def manage():
    # if 'user_id' in session:
    #     print('session active manage')
    #     user = User.query.filter_by(id=session['user_id']).first()
    #     g.user = user

    cookie = request.cookies.get('user_id')
    print(str(cookie) + "B")

    if not cookie or cookie == '':
        return redirect(url_for('login'))
    else:
        print("A" + cookie + "A")
        user = User.query.filter_by(id=int(cookie)).first()
        resp = make_response(render_template('manage.html', user=user))
        resp.set_cookie('user_id', value=str(user.id), max_age=1500, samesite='Lax')

    if request.method == "GET" and cookie:
        action = request.args.get('action')
        amount = request.args.get('amount')
        # handle balance and close
        if action and not amount:
            if action == 'balance':
                user.action_type = 'balance'
                print("balance=" + str(user.balance))
            elif action == 'close':
                user.action_type = 'close'
                return close_account()
                # resp = make_response(close_account())
                # resp.set_cookie('user_id', value=str(user.id), max_age=1500)
                # return resp
                # return render_template('sign_up.html')
        # handle deposit and withdrawal
        elif action and amount:
            if action == 'deposit' and int(amount) > 0:
                current_balance = user.balance
                new_balance = current_balance + int(amount)
                user.balance = new_balance
                user.action_type = 'balance'
                db.session.commit()
                print('balance=' + str(new_balance))
                resp = make_response(render_template('manage.html', user=user))
                resp.set_cookie('user_id', value=str(user.id), max_age=1500, samesite='Lax')
            elif action == 'withdraw' and int(amount) > 0:
                current_balance = user.balance
                if int(amount) > current_balance:
                    flash('Your account does not have sufficient funds to complete this withdrawal', category='error')
                else:
                    new_balance = current_balance - int(amount)
                    user.balance = new_balance
                    print('balance=' + str(new_balance))
                    user.action_type = 'balance'
                    db.session.commit()
                    resp = make_response(render_template('manage.html', user=user))
                    resp.set_cookie('user_id', value=str(user.id), max_age=1500, samesite='Lax')
            else:
                flash('Please enter a value greater than zero', category='error')

    # return render_template('manage.html', user=g.user)
    return resp


@app.route('/close-account')
# @login_required
def close_account():
    cookie = request.cookies.get('user_id')
    user = User.query.filter_by(id=cookie).delete()
    db.session.commit()

    resp = make_response(redirect(url_for('login')))
    # resp.set_cookie('user_id', value='', max_age=1)
    resp.delete_cookie('user_id')
    # user = g.user
    # session.pop('user_id', None)

    return resp


# only if we execute this file, and did not import it, should the app be run
if __name__ == '__main__':
    app.run()

    #  ssl_context='adhoc'
