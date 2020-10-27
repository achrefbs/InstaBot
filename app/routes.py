from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.models.account import Account
from app.forms import AccountForm

@app.route('/')
def dashboard():
	return render_template('dashboard.html')


@app.route('/accounts')
def accounts():
    """
    render accounts page
    displays form
    add account to db
    displays a list of all accounts
    """
    form = AccountForm() 
    all_accounts = db.session.query(Account)
    return render_template('accounts.html', title='Accounts', form=form, all_accounts=all_accounts)


@app.route('/accounts', methods=['POST'])
def add_account():
    """adds account to db"""
    form = AccountForm() 
    username = request.form.get('username')
    password = request.form.get('password')
    if form.submit():
        if username is None or username == "":
            flash('please make sure username is correct')
        elif password is None or password == "":
            flash('please make sure password is correct')
        else:
            account = Account(username=username, password=password)
            db.session.add(account)
            db.session.commit()
    return redirect(url_for('accounts'))



@app.route('/accounts/delete/<int:id>')
def delete_account(id):
    """deletes account from db"""
    db.session.delete(Account.query.get(id))
    db.session.commit()
    return redirect(url_for('accounts'))