# # store the roots for our website-- where users can navigate to
# from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
# from flask_login import login_required, current_user, fresh_login_required
# from .models import User
# from . import db
# import json
# from flask_login import logout_user
#
# views = Blueprint('views', __name__)
#
#
# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     return render_template("home.html", user=current_user)
#     # we then need to register these blueprints in __init__.py
#     # current_user allows us to reference the user that is logged in
#
#
# @views.route('/update-content', methods=['GET', 'POST'])
# @fresh_login_required
# def update_content():
#     message = json.loads(request.data)
#     content_type = message['content_type']
#     current_user.action_type = content_type
#     db.session.commit()
#
#     return jsonify({})
#
#
# @views.route('/manage', methods=['GET'], defaults={'action': None, 'amount': None})
# @views.route('/manage/<action>', methods=['GET'], defaults={'amount': None})
# @views.route('/manage/<action>/<int:amount>', methods=['GET'])
# @fresh_login_required
# def manage(action, amount):
#     # handle balance and close
#     if not action and not amount:
#         print('we got nothin')
#         action = request.args.get('action')
#         amount = request.args.get('amount')
#         if not action and not amount:
#             print("request args didn't work either")
#         elif action and not amount:
#             print("args worked: action--" + action)
#         elif not action and not amount:
#             print("args worked: amount" + str(amount))
#         else:
#             print("args worked: action--" + action + " amount--" + str(amount))
#     if action and not amount:
#         print('action: ' + action)
#         if action == 'balance':
#             current_user.action_type = 'balance'
#             print('action = deposit')
#         elif action == 'close':
#             current_user.action_type = 'close'
#             close_account()
#             return redirect(url_for('auth.signup'))
#             # return render_template('sign_up.html', user=current_user)
#     # handle deposit and withdrawal
#     elif action and amount:
#         print('action: ' + action)
#         print('amount: ' + str(amount))
#         if action == 'deposit' and int(amount) > 0:
#             current_balance = current_user.balance
#             new_balance = current_balance + int(amount)
#             current_user.balance = new_balance
#             current_user.action_type = 'balance'
#             db.session.commit()
#             print('balance=' + str(new_balance))
#         elif action == 'withdraw' and int(amount) > 0:
#             current_balance = current_user.balance
#             if int(amount) > current_balance:
#                 flash('Your account does not have sufficient funds to complete this withdrawal', category='error')
#             else:
#                 new_balance = current_balance - int(amount)
#                 current_user.balance = new_balance
#                 current_user.action_type = 'balance'
#                 db.session.commit()
#         else:
#             flash('Please enter a value greater than zero', category='error')
#
#     return render_template('manage.html', user=current_user)
#
#
# @views.route('/close-account')
# @fresh_login_required
# def close_account():
#     user = current_user
#     User.query.filter_by(id=user.id).delete()
#     db.session.commit()
#     logout_user()
#     return redirect(url_for('auth.login'))
