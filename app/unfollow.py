from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import unfollow_by_list_Form, unfollow_non_followers, unfollow_all
from app.models.account import Account
from instapy import InstaPy
from instapy import smart_run



@app.route('/unfollow_by_list')
def display_unfollowbylist():
    form = unfollow_by_list_Form()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('unfollowbylist.html', title='Unfollow by list', form=form)



@app.route('/unfollow_by_list', methods=['POST'])
def unfollowbylist():
    form = unfollow_by_list_Form()
    accounts_id = request.form.getlist('accounts')
    users = request.form.get('users')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))
    unfollow_after = int(request.form.get('unfollow_after'))


    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_unfollowbylist'))

    with open('unfollowlist.txt', 'w') as f:
        f.write(users)
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, unfollow=delay, randomize=True, random_range_from=70, random_range_to=140)
        unfollowlist = sess.target_list('unfollowlist.txt')
        sess.unfollow_users(amount=amount ,custom_list_enabled=True, custom_list= unfollowlist, unfollow_after=unfollow_after)

    return redirect(url_for('display_unfollowbylist'))



@app.route('/unfollow_non_followers')
def display_unfollownonfollowers():
    form = unfollow_non_followers()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('unfollownonfollowers.html', title='Unfollow non followers', form=form)




@app.route('/unfollow_non_followers', methods=['POST'])
def unfollownonfollowers():
    form = unfollow_non_followers()
    accounts_id = request.form.getlist('accounts')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))
    unfollow_after = int(request.form.get('unfollow_after'))


    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_unfollownonfollowers'))
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, unfollow=delay, randomize=True, random_range_from=70, random_range_to=140)
        sess.unfollow_users(amount=amount, nonFollowers=True, unfollow_after=unfollow_after)

    return redirect(url_for('display_unfollownonfollowers'))




@app.route('/unfollow_all')
def display_unfollowall():
    form = unfollow_all()
    form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
    return render_template('unfollowall.html', title='Unfollow all', form=form)



@app.route('/unfollow_all', methods=['POST'])
def unfollowall():
    form = unfollow_all()
    accounts_id = request.form.getlist('accounts')
    amount = int(request.form.get('amount'))
    delay = int(request.form.get('delay'))
    unfollow_after = int(request.form.get('unfollow_after'))


    if len(accounts_id) != 1:
        flash('please select one account')
        return redirect(url_for('display_unfollowall'))
    with open('account.txt', 'w') as f:
        f.write(db.session.query(Account).get(accounts_id[0]).username)
    sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
                      password = db.session.query(Account).get(accounts_id[0]).password,
                      disable_image_load=False, headless_browser=False)

    with smart_run(sess, threaded=True):
        sess.set_action_delays(enabled=True, unfollow=delay, randomize=True, random_range_from=70, random_range_to=140)
        sess.unfollow_users(amount=amount, allFollowing=True, unfollow_after=unfollow_after)

    return redirect(url_for('display_unfollowall'))