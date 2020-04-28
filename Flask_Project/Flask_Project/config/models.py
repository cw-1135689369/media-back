#encoding:utf-8


from datetime import datetime

# # 定义用户模型
# class User(db.Model):
#     __tablename__='user'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     telephone=db.Column(db.String(11),nullable=False)
#     username=db.Column(db.String(50),nullable=False)
#     password=db.Column(db.String(100),nullable=False)
#
#
# # 定义问题模型
# class Question(db.Model):
#     __tablename__='question'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     title=db.Column(db.String(100),nullable=False)
#     content=db.Column(db.Text,nullable=False)
#     # now()获取的是服务器第一次运行的时间
#     # now就是每次创建一个模型的时候 都获取当前时间
#     create_time=db.Column(db.DateTime,default=datetime.now)
#     author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
#     author=db.relationship('User',backref=db.backref('questions'))


# # 定义评论模型
# class Answer(db.Model):
#     __tablename__='answer'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     content=db.Column(db.Text,nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
#     author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
#     question=db.relationship('Question',backref=db.backref('answers'))
#     author=db.relationship('User',backref=db.backref('answers'))
