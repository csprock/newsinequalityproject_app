from datetime import datetime
from app import db
from app.models import Post, Author
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--title', required=True, type=str)
parser.add_argument('--author_id', required=True, type=int)
parser.add_argument('--year', required=True, type=int)
parser.add_argument('--month', required=True, type=int)
parser.add_argument('--day', required=True, type=int)


args = parser.parse_args()

author = Author.query.filter_by(id=args.author_id)

post = Post(title=args.title, 
            date=datetime(year=args.year, month=args.month, day=args.day), 
            author=author, 
            author_id=args.author_id)

db.session.add(post)
db.session.commit()