from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import Follow_by_tag_Form, Follow_user_followers_Form, Follow_by_list_Form
from app.models.account import Account
from instapy import InstaPy
from instapy import smart_run

@app.route('/follow_by_tag')
def display_followbytag():
    form = Follow_by_tag_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('followbytag.html', title='Follow by tag', form=form)


@app.route('/follow_by_tag', methods=['POST'])
def followbytag():
    form = Follow_by_tag_Form()
    accounts_id = request.form.getlist('accounts')
    tags = request.form.get('tags')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))

    if request.form.get('randomize') is None:
        randomize = False
    else:
        randomize = True

    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_followbytag'))

    with open('tags.txt', 'w') as f:
        f.write(tags)
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=True)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, follow=delay, randomize=True, random_range_from=70, random_range_to=140)
        hashtags = sess.target_list('tags.txt')
        sess.follow_by_tags(hashtags, amount=amount, randomize=randomize)

    return redirect(url_for('display_followbytag'))



@app.route('/follow_user_followers')
def display_followuserfollowers():
    form = Follow_user_followers_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('followuserfollowers.html', title='Follow user followers', form=form)




@app.route('/follow_user_followers', methods=['POST'])
def followuserfollowers():
    form = Follow_user_followers_Form()
    accounts_id = request.form.getlist('accounts')
    users = request.form.get('users')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))

    if request.form.get('randomize') is None:
        randomize = False
    else:
        randomize = True

    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_followuserfollowers'))

    with open('users.txt', 'w') as f:
        f.write(users)
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=True)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, follow=delay, randomize=True, random_range_from=70, random_range_to=140)
        usersfoll = sess.target_list('users.txt')
        sess.follow_user_followers(usersfoll, amount=amount, randomize=randomize)

    return redirect(url_for('display_followuserfollowers'))




@app.route('/follow_by_list')
def display_followbylist():
    form = Follow_by_list_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('followbylist.html', title='Follow by list', form=form)


@app.route('/follow_by_list', methods=['POST'])
def followbylist():
    form = Follow_by_list_Form()
    accounts_id = request.form.getlist('accounts')
    users = request.form.get('users')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))

    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_followbylist'))

    with open('users.txt', 'w') as f:
        f.write(users)
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=True)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, follow=delay, randomize=True, random_range_from=70, random_range_to=140)
        users = sess.target_list('users.txt')
        sess.follow_by_list(users, amount=amount)

    return redirect(url_for('display_followbylist'))
