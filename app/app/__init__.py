from flask import Flask, render_template
#from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_mail import Mail
import click
from flask.cli import AppGroup
from datetime import datetime

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter(fmt="%(asctime)s [%(level)s] %(message)s %(module)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



app = Flask(__name__)
app.config.from_object(Config)

#s3 = FlaskS3(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app.main import bp as main_bp
from app.blog import bp as blog_bp
app.register_blueprint(main_bp)
app.register_blueprint(blog_bp)

from app import models

#### Define CLI for DB management ####
metadata_cli = AppGroup('metadata')

@metadata_cli.command('create_author')
@click.option('--firstname', type=str, required=True)
@click.option('--lastname', type=str, required=True)
@click.option('--email', type=str, required=True)
@click.option('--handle', type=str, required=True)
def create_author(firstname, lastname, email, handle):
    
    author = models.Author(firstname=firstname,
                           lastname=lastname, 
                           email=email,
                           handle=handle)

    db.session.add(author)
    db.session.commit()

    new_author = models.Author.query.order_by(models.Author.id.desc()).first()

    logger.info(f"Inserted new author with ID {new_author.id}")

@metadata_cli.command('create_post')
@click.option('--title', type=str, required=True)
@click.option('--author_id', type=int, required=True)
@click.option('--header_pic', type=int, required=True)
@click.option('--year', type=int, required=True)
@click.option('--month', type=int, required=True)
@click.option('--day', type=int, required=True)
@click.option('--url', type=str, required=False, default=None)
def create_post(title, author_id, header_pic, year, month, day, url):
    
    author = models.Author.query.filter_by(id=author_id)

    post = models.Post(title=title, 
                       date=datetime(year=year, month=month, day=day), 
                       author=author, 
                       author_id=author_id,
                       external_url=url,
                       header_pic=header_pic)

    db.session.add(post)
    db.session.commit()

    logger.info(f"Added post {post.id}")

@metadata_cli.command('delete_author')
@click.option('--author_id', type=int, required=True)
def delete_author(author_id):
    
    author = models.Author.query.filter_by(id=author_id).first()

    posts = models.Post.query.filter_by(author_id=author.id).all()

    for post in posts:
        db.session.delete(post)

    db.session.commit()

    db.session.delete(author)
    db.session.commit()

    logger.info(f"Author {author.firstname} {author.lastname} deleted.")

@metadata_cli.command('delete_post')
@click.option('--post_id', type=int, required=True)
def delete_post(post_id):
    
    post = models.post.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()

    logger.info(f"Post {post.id} {author.title} deleted.")

app.cli.add_command(metadata_cli)