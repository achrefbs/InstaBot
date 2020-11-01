from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.models.account import Account
from app.forms import AccountForm, accept_requests_Form
from instapy import InstaPy
from instapy import smart_run

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



@app.route('/accept_requests')
def display_acceptrequests():
    form = accept_requests_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('acceptrequests.html', title='Accept pending requests', form=form)


@app.route('/accept_requests', methods=['POST'])
def acceptrequests():
    form = accept_requests_Form()
    accounts_id = request.form.getlist('accounts')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))

    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_acceptrequests'))

    session = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(session, threaded=True):
        session.accept_follow_requests(amount=amount, sleep_delay=delay)

    return redirect(url_for('display_acceptrequests'))