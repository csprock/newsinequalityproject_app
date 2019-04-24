import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = 'this-is-my-key'

    # TODO: remove hardcoded parameters and move into environment
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{dbname}'.format(
    #     host=os.environ['POSTGRES_HOST'],
    #     user=os.environ['POSTGRES_USER'],
    #     password=os.environ['POSTGRES_PASSWORD'],
    #     dbname=os.environ['POSTGRES_DB'])

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_PER_PAGE = 3

    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']


    #AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    #AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    #FLASKS3_BUCKET_NAME = os.environ['FLASKS3_BUCKET_NAME']
    #FLASKS3_REGION = os.environ['FLASKS3_REGION']
    #FLASKS3_USE_HTTPS = False
    #FLASKS3_ACTIVE = False
    #FLASKS3_DEBUG = False

