# -*- encoding=UTF-8 -*-

from nowstagram import app, db
from flask_script import Manager
from nowstagram.models import  User,Image,Comment
import random
manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('newke' +str(i), 'a'+str(i)))
        for j in range(0, 3):   #每人发三张图
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('comment'+str(k), 1+3*i+j, i+1))
    db.session.commit()

    for i in range(60, 100, 10):
        # 通过update函数
        User.query.filter_by(id=i + 1).update({'username': '牛客新' + str(i)})
    db.session.commit()
    for m in range(5, 50, 2):
        # 通过设置属性
        newname = User.query.get(m)
        newname.username = '[new]' + newname.username
    db.session.commit()
    User.query.filter_by(id=11).update({'username': 'usr77'})
    db.session.commit()

    for i in range(51, 100, 2):
        comment = Comment.query.get(i + 1)
        db.session.delete(comment)
    db.session.commit()
if __name__=='__main__':
    manager.run()

