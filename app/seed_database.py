from datetime import datetime
from app import db
from app.models import Author, Post

db.create_all()

author1 = Author(firstname="Hamdan", lastname="Azhar", email="hamdan.azhar@gmail.com", handle="https://twitter.com/HamdanAzhar")
post1 = Post(title="Our Story", date=datetime(year=2019, month=1, day=1), author=author1, author_id=1)

db.session.add(author1)
db.session.commit()
db.session.add(post1)
db.session.commit()