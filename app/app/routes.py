from flask import render_template, flash, redirect, url_for, request
from flask_mail import Message
from app.forms import ContactForm
# from app.main import bp
from app import app
from app import mail
from app.models import Post, Author

from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def parse_html_file(path):

    with open(path, 'r') as f:
        file_content = f.read()

    return file_content



@app.route('/')
@app.route('/index')
def index():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    header_pic_url = "/static/img/header_index.jpg"

    return render_template('blog.html', main_header="The News Inequality Project", title="The News Inequality Project", posts=post_items, next_url=next_url, prev_url=prev_url, header_pic_url=header_pic_url)


@app.route('/about')
def about():
    return render_template('about.html', main_header="About Us", title="About")


@app.route('/contact', methods=['GET', 'POST'])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        email_addr = form.email.data
        comment = form.comment.data
        name = form.name.data

        body_message = '''
        From: {} at {}, \n
        Comment: {}
        '''.format(name, email_addr, comment)

        msg = Message(subject="[NIP app] Contact Request",
                        body=body_message,
                        sender=app.config['ADMIN_EMAIL'],
                        recipients=app.config['ADMIN_RECIPIENTS'])


        thd = Thread(target=send_async_email, args=[app, msg])
        thd.start()

        flash("Thanks for your interest, {}!".format(name))

        return redirect('/contact')

    return render_template('contact.html', title="Contact Us", main_header="Contact Us", form=form)


@app.route('/blog')
def blog():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    header_pic_url = "/static/img/header_index.jpg"

    return render_template('blog.html', main_header="Blog", title="Blog", posts=post_items, next_url=next_url, prev_url=prev_url, header_pic_url=header_pic_url)


@app.route('/blog/<int:post_id>')
def blog_post(post_id):

    post_meta = Post.query.filter_by(id=post_id).first_or_404()

    if post_meta.header_pic:
        header_pic_url = "/static/img/header_{}.jpg".format(post_id)
    else:
        header_pic_url = None

    return render_template('blog/post_{}.html'.format(post_id), main_header=post_meta.title, title=post_meta.title, header_pic_url=header_pic_url, post=post_meta)


##########################
### App Error Handlers ###
##########################

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", title="404 Error", main_header="404"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html", title="500 Error", main_header="500"), 500
