from models import Post, User, db
from app import app 

db.drop_all()
db.create_all()

u1 = User(first_name = 'Nate', last_name = 'Test', image_url = 'https://play-lh.googleusercontent.com/HnzbI7urJlB6V26dtKiawYoBrH4iR5DAAk4KqNZzIa0NRWQukskR6aX7IrV55AULKIgA=w240-h480-rw')

u2 = User(first_name = 'Karla', last_name = 'Lozano-Smith', image_url = 'https://cdn.prod.website-files.com/6005be2ff5173b2244717570/62151df2fbd936dd4d843ba3_82qWt8IK5oVuM3R2ZnhQdpnfal1DgQt1Lz4ECc2fZjDJtrp5QJhaPKMQJLL12CnrKASRA-7x4x9CDjzicW5x_oWSjQAF9YYSrzz2Sz2TuOnUjIkRKhKd0E5CuP7P93Y1MCCn4KCP.jpeg')

dumb_post = Post(title='Dumb Post', content='This is a dumb post.', user_id=1)
post3 = Post(title='Chicken Parmigiana', content='<insert recipe>', user_id=1)
smart_post = Post(title='Smart Post', content='E=MC^2', user_id=2)
post4 = Post(title='Coffee', content='My favorite coffee is from Daily Dose', user_id=2)

db.session.add_all([u1,u2])
db.session.commit()

db.session.add_all([dumb_post, smart_post, post3, post4])
db.session.commit()


