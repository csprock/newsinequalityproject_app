import os
from flask import Flask, render_template
#from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_mail import Mail
import click
from flask.cli import AppGroup
from datetime import datetime

from app.utils import create_content_folder

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app import routes
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

    app.logger.info(f"Inserted new author with ID {new_author.id}")

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

    app.logger.info(f"Added post {post.id}")

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

    app.logger.info(f"Author {author.firstname} {author.lastname} deleted.")

@metadata_cli.command('delete_post')
@click.option('--post_id', type=int, required=True)
def delete_post(post_id):
    
    post = models.Post.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()

    app.logger.info(f"Post {post.id} {post.title} deleted.")



@metadata_cli.command("init_directories")
def init_directories():


    paths = [
        os.path.join(app.root_path, app.config['DEFAULT_BLOG_CONTENT_FOLDER']),
        os.path.join(app.root_path, app.config['DEFAULT_BLOG_TEMPLATE_FOLDER']),
        os.path.join(os.path.join(app.root_path, app.config['DEFAULT_BLOG_CONTENT_FOLDER']), 'other')
    ]

    for path in paths:
        try:
            os.mkdir(path)
            os.chown(path, app.config['UID'], app.config['UID'])
            app.logger.info(f"{path} created.")
        except FileExistsError:
            app.logger.warning(f"{path} already exists")

    # try:
    #     path = os.path.join(app.root_path, app.config['DEFAULT_BLOG_CONTENT_FOLDER'])
    #     os.mkdir(path)
    #     os.chown(path, app.config['UID'], app.config['UID'])
    # except FileExistsError:
    #     app.logger.info("static/blogs folder already exists")

    # try:
    #     path = os.path.join(app.root_path, app.config['DEFAULT_BLOG_TEMPLATE_FOLDER'])
    #     os.mkdir(path)
    #     os.chown(path, app.config['UID'], app.config['UID'])
    # except FileExistsError:
    #     app.logger.info("templates/blogs folder already exists")

    # try:
    #     path = os.path.join(os.path.join(app.root_path, app.config['DEFAULT_BLOG_CONTENT_FOLDER']), 'other')
    #     os.mkdir(path)
    #     os.chown(path, app.config['UID'], app.config['UID'])
    # except FileExistsError:
    #     app.logger.info("static/blog/other already exists")


app.cli.add_command(metadata_cli)
