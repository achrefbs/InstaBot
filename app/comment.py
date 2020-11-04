from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import Comment_by_tag_Form, Comment_by_feed_Form
from app.models.account import Account
from instapy import InstaPy
from instapy import smart_run


@app.route('/comment_by_tag')
def display_commentbytag():
	form = Comment_by_tag_Form()
	form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
	return render_template('commentbytag.html', title='comment by tag', form=form)




@app.route('/comment_by_tag', methods=['POST'])
def commentbytag():
	form = Comment_by_tag_Form()
	accounts_id = request.form.getlist('accounts')
	tags = request.form.get('tags')
	amount = int(request.form.get('amount'))
	delay = int(request.form.get('delay'))
	comments = request.form.get('comments')
	percentage = int(request.form.get('percentage'))
	if request.form.get('randomize') is None:
		randomize = False
	else:
		randomize = True

	if len(accounts_id) != 1:
		flash('please select one account')
		return redirect(url_for('display_commentbytag'))

	with open('tags.txt', 'w') as f:
			f.write(tags)
	with open('comments.txt', 'w') as f:
			f.write(comments)
	with open('account.txt', 'w') as f:
		f.write(db.session.query(Account).get(accounts_id[0]).username)

	sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
					  password = db.session.query(Account).get(accounts_id[0]).password,
					  disable_image_load=False, headless_browser=True)
	with smart_run(sess, threaded=True):
		sess.set_action_delays(enabled=True, like=delay, randomize=True, random_range_from=70, random_range_to=140)
		hashtags = sess.target_list('tags.txt')
		comments = sess.target_list('comments.txt')
		sess.set_do_comment(enabled=True, percentage=percentage)
		sess.set_comments(comments)
		sess.like_by_tags(hashtags, amount=amount, randomize=randomize)


	return redirect(url_for('display_commentbytag'))




@app.route('/commment_by_feed')
def display_commentbyfeed():
	form = Comment_by_feed_Form()
	form.accounts.choices = [(acc.id, acc.username) for acc in db.session.query(Account)]
	return render_template('commentbyfeed.html', title='Comment by feed', form=form)


@app.route('/commment_by_feed', methods=['POST'])
def commentbyfeed():
	form = Comment_by_feed_Form()
	accounts_id = request.form.getlist('accounts')
	amount = int(request.form.get('amount'))
	delay = int(request.form.get('delay'))
	comments = request.form.get('comments')
	percentage = int(request.form.get('percentage'))

	if request.form.get('randomize') is None:
		randomize = False
	else:
		randomize = True

	if len(accounts_id) != 1:
		flash('please select one account')
		return redirect(url_for('display_commentbyfeed'))

	with open('comments.txt', 'w') as f:
			f.write(comments)
	with open('account.txt', 'w') as f:
		f.write(db.session.query(Account).get(accounts_id[0]).username)
	sess = InstaPy(username = db.session.query(Account).get(accounts_id[0]).username,
					  password = db.session.query(Account).get(accounts_id[0]).password,
					  disable_image_load=False, headless_browser=True)

	with smart_run(sess, threaded=True):
		comments = sess.target_list('comments.txt')
		sess.set_action_delays(enabled=True, like=delay, randomize=True, random_range_from=70, random_range_to=140)
		sess.set_do_comment(enabled=True, percentage=percentage)
		sess.set_comments(comments)
		sess.like_by_feed(amount=amount, randomize=randomize)

	return redirect(url_for('display_commentbyfeed'))
