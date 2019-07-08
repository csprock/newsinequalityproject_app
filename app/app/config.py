import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = 'this-is-my-key'

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{dbname}'.format(
        host=os.environ['POSTGRES_HOST'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        dbname=os.environ['POSTGRES_DB'])

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_PER_PAGE = int(os.environ.get('MAX_PER_PAGE', 10))

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_RECIPIENTS = os.environ.get('ADMIN_RECIPIENTS')


    #### URLs to static files #####
    STATIC_HEADER_PICTURE_INDEX = 'blog/other/index_header.jpg'
    DEFAULT_HEADER_PICTURE_NAME = re.compile("^header.(jpg|jpeg|png)$")


    #AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    #AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    #FLASKS3_BUCKET_NAME = os.environ['FLASKS3_BUCKET_NAME']
    #FLASKS3_REGION = os.environ['FLASKS3_REGION']
    #FLASKS3_USE_HTTPS = False
    #FLASKS3_ACTIVE = False
    #FLASKS3_DEBUG = False

