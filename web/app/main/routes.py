from flask import render_template, flash, redirect, url_for, request
from app.main.forms import ContactForm
from app.main import bp
from app import app

from app.models import Post, Author


@bp.route('/')
@bp.route('/index')
def index():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    return render_template('blog.html', main_header="News Inequality Project", title="News Inequality Project", posts=post_items, next_url=next_url, prev_url=prev_url)


@bp.route('/about')
def about():
    return render_template('about.html', main_header="About Us", title="About")


@bp.route('/contact', methods=['GET', 'POST'])
def contact():

    form = ContactForm()

    if form.validate_on_submit():
        # TODO: logic to send email
        flash("Thank you for your interest!")
        return redirect(url_for('main.contact'))

    return render_template('contact.html', title="Contact Us", main_header="Contact Us", form=form)


##########################
### App Error Handlers ###
##########################

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", title="404 Error", main_header="404"), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html", title="500 Error", main_header="500"), 500
