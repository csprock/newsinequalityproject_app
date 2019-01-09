from app import app
from app.blog import bp
from app.models import Post

from flask import url_for, render_template, request

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

    return render_template('blog.html', main_header="Blog", title="Blog", posts=post_items, next_url=next_url, prev_url=prev_url)


@bp.route('/blog/<int:post_id>')
def blog_post(post_id):

    post_meta = Post.query.filter_by(id=post_id).first_or_404()

    return render_template('blog/post_{}.html'.format(post_id), main_header=post_meta.title, title=post_meta.title)


# @bp.route('/test')
# def test():
#
#     print("-----")
#     print(url_for('static', filename='blog/post0/post0.html'))
#     print("-----")
#
#     TEST = parse_html_file('app/static/blog/post0/post0.html')

#     TEST = '''
#     {% extends "post.html" %}
#
# {% block post %}
#
#     <!-- Post Content -->
#               <div class="text-center">
#                   <img class="img-fluid" src="{{ url_for('static', filename='blog/post0/post0img0.jpg') }}" alt="">
#               </div>
#               <p>In February 2017, the MIT Media Lab hosted <a href="https://misinfocon.com" target="_blank" rel="noopener">Misinfocon</a>, a creative studio aimed at combating misinformation and promoting trust in journalism. Our team had came to Cambridge from around the country &#8211; from New York, San Francisco, Portland, Maine, and Washington, DC &#8211; and we were united by our passion for the intersection of data, journalism, and storytelling.</p>
#               <p>During the opening pitch session, Hamdan Azhar discussed his experiences growing up in a little known part of Brooklyn called Marine Park. &#8220;Why is it that everyone has heard of Williamsburg but no one has heard of Marine Park?&#8221; he wondered. Could the media be playing a role in driving this attention inequality?</p>
#               <p>Luckily, among our team, we had a strong, complementary set of skills in data munging, analysis, design, and data visualization. Over the next 36 hours, we worked together to create a proof of concept for a quantitative analysis of news inequality based on data from New York and Maine. Check out some of our findings <a href="http://christianmilneil.com/newsinequalitycheckup/" target="_blank" rel="noopener">here</a>!</p>
#               <div class="text-center">
#                   <img class="img-fluid" src="{{ url_for('static', filename='blog/post0/post0img1.png') }}" alt="">
#               </div>
#
# {% endblock %}
#     '''



    # return render_template_string(TEST, main_header="New York Times' Coverage of Gentrification in NYC", title="NYC Gentrification")