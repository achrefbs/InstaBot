from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import Follow_by_tag_Form, Follow_user_followers_Form
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

    session = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(session, threaded=True):
        session.set_action_delays(enabled=True, follow=delay, randomize=True, random_range_from=70, random_range_to=140)
        hashtags = session.target_list('tags.txt')
        session.follow_by_tags(hashtags, amount=amount, randomize=randomize)

    print('accounts_id: {}'.format(accounts_id))
    print('amount: {}'.format(amount))
    print('delay: {}'.format(delay))
    print('randomize: {}'.format(randomize))
    print('tags: {}'.format(tags))

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
        return redirect(url_for('display_followbytag'))

    with open('users.txt', 'w') as f:
        f.write(users)

    session = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(session, threaded=True):
        session.set_action_delays(enabled=True, follow=delay, randomize=True, random_range_from=70, random_range_to=140)
        usersfoll = session.target_list('users.txt')
        session.follow_user_followers(usersfoll, amount=amount, randomize=randomize)

    print('accounts_id: {}'.format(accounts_id))
    print('amount: {}'.format(amount))
    print('delay: {}'.format(delay))
    print('randomize: {}'.format(randomize))
    print('users: {}'.format(users))

    return redirect(url_for('display_followuserfollowers'))