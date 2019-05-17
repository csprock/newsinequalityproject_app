from app import db
from app.models import Author
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--firstname', required=True, type=str)
parser.add_argument('--lastname', required=True, type=str)
parser.add_argument('--email', required=True, type=str)
parser.add_argument('--handle', required=True, type=str)

args = parser.parse_args()



author = Author(firstname=args.firstname,
                 lastname=args.lastname, 
                 email=args.email,
                 handle=args.handle)

db.session.add(author)
db.session.commit()