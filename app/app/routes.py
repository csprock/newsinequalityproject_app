import os
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask_mail import Message
from threading import Thread

from app.forms import ContactForm
from app import app
from app import mail
from app.models import Post, Author

from app.utils import send_async_email
from app.utils import check_file_in_dir

@app.route('/')
@app.route('/index')
def index():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    header_pic_url = url_for('static', filename=app.config['STATIC_HEADER_PICTURE_INDEX'])

    return render_template('blog.html', 
                            main_header="The News Inequality Project", 
                            title="The News Inequality Project", 
                            posts=post_items, 
                            next_url=next_url, 
                            prev_url=prev_url, 
                            header_pic_url=header_pic_url)


@app.route('/about')
def about():

    header_pic_url = url_for('static', filename=app.config['STATIC_HEADER_PICTURE_INDEX'])

    return render_template('about.html', 
                            main_header="About Us", 
                            title="About",
                            header_pic_url=header_pic_url)


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


        thd = Thread(target=send_async_email, args=[app, msg, mail])
        thd.start()

        flash("Thanks for your interest, {}!".format(name))

        return redirect(url_for('contact'))

    return render_template('contact.html', 
                            title="Contact Us", 
                            main_header="Contact Us", 
                            form=form)


@app.route('/blog')
def blog():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    header_pic_url = url_for('static', filename=app.config['STATIC_HEADER_PICTURE_INDEX'])

    return render_template('blog.html', 
                            main_header="Blog", 
                            title="Blog", 
                            posts=post_items, 
                            next_url=next_url, 
                            prev_url=prev_url, 
                            header_pic_url=header_pic_url)


@app.route('/blog/<int:post_id>')
def blog_post(post_id):

    post_meta = Post.query.filter_by(id=post_id).first_or_404()

    _file = check_file_in_dir(os.path.join(app.root_path, f'static/blog/post_{post_id}'), app.config['DEFAULT_HEADER_PICTURE_NAME'])
    app.logger.debug("Header file {}".format(_file))

    if _file:
        header_pic_url = url_for('static', filename=f"/blog/post_{post_id}/{_file}")
        app.logger.debug(f"header_pic_url: {header_pic_url}")
    else:
        header_pic_url = None
        app.logger.debug("header_pic_url is None")

    # if post_meta.header_pic:
    #     header_pic_url = url_for('static', filename=f"/blog/post_{post_id}/header.jpg")
    # else:
    #     header_pic_url = None

    return render_template(f'blog/post_{post_id}.html', 
                            main_header=post_meta.title, 
                            title=post_meta.title, 
                            header_pic_url=header_pic_url, 
                            post=post_meta)


##########################
### App Error Handlers ###
##########################

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", title="404 Error", main_header="404"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html", title="500 Error", main_header="500"), 500
