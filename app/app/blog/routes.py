from app import app
from app.blog import bp
from app.models import Post

from flask import url_for, render_template, request

import logging

def parse_html_file(path):

    with open(path, 'r') as f:
        file_content = f.read()

    return file_content


@bp.route('/blog')
def blog():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['MAX_PER_PAGE'], error_out=True)

    post_items = posts.items

    next_url = url_for('blog.html', page=posts.prev_num) if posts.has_prev else None
    prev_url = url_for('blog.html', page=posts.next_num) if posts.has_next else None

    header_pic_url = "/static/img/header_index.jpg"

    return render_template('blog.html', main_header="Blog", title="Blog", posts=post_items, next_url=next_url, prev_url=prev_url, header_pic_url=header_pic_url)


@bp.route('/blog/<int:post_id>')
def blog_post(post_id):

    post_meta = Post.query.filter_by(id=post_id).first_or_404()

    if post_meta.header_pic:
        header_pic_url = "/static/img/header_{}.jpg".format(post_id)
    else:
        header_pic_url = None

    return render_template('blog/post_{}.html'.format(post_id), main_header=post_meta.title, title=post_meta.title, header_pic_url=header_pic_url, post=post_meta)