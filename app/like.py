from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import Like_by_tag_Form, Like_by_feed_Form
from app.models.account import Account
from instapy import InstaPy
from instapy import smart_run




@app.route('/like_by_tag')
def display_likebytag():
    form = Like_by_tag_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('likebytag.html', title='Like by tag', form=form)




@app.route('/like_by_tag', methods=['POST'])
def likebytag():
    form = Like_by_tag_Form()
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
        return redirect(url_for('display_likebytag'))

    with open('tags.txt', 'w') as f:
        f.write(tags)

    session = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(session, threaded=True):
        session.set_action_delays(enabled=True, like=delay, randomize=True, random_range_from=70, random_range_to=140)
        hashtags = session.target_list('tags.txt')
        session.like_by_tags(hashtags, amount=amount, randomize=randomize)

    print('accounts_id: {}'.format(accounts_id))
    print('amount: {}'.format(amount))
    print('delay: {}'.format(delay))
    print('randomize: {}'.format(randomize))
    print('tags: {}'.format(tags))

    return redirect(url_for('display_likebytag'))

@app.route('/like_by_feed')
def display_likebyfeed():
    form = Like_by_feed_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('likebyfeed.html', title='Like by feed', form=form)




@app.route('/like_by_feed', methods=['POST'])
def likebyfeed():
    form = Like_by_feed_Form()
    accounts_id = request.form.getlist('accounts')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))

    if request.form.get('randomize') is None:
        randomize = False
    else:
        randomize = True

    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_likebyfeed'))

    session = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(session, threaded=True):
        session.set_action_delays(enabled=True, like=delay, randomize=True, random_range_from=70, random_range_to=140)
        session.like_by_feed(amount=amount, randomize=randomize)

    return redirect(url_for('display_likebyfeed'))