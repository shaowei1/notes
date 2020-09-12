import os
import datetime
from datetime import date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, cast, and_
from sqlalchemy.sql.sqltypes import DATETIME
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.sql.schema import Column
from sqlalchemy import func, String

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:yangxinyue@127.0.0.1:3306/merchant?charset=utf8mb4'
db = SQLAlchemy(app)


class User(db.Model):
    id = Column(INTEGER(10), primary_key=True)
    account_id = Column(INTEGER(10))
    name = Column(String(200))
    updated_at = Column(DATETIME,
                        default=datetime.datetime.utcnow,
                        )
    created_at = Column(DATETIME,
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow, )


saved_days = os.getenv('SAVED_DAYS', 10)

db.session.bulk_save_objects([User(account_id=1, name='yue')])
db.session.commit()

ten_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=saved_days)

now_update = db.session.query(User).filter(func.DATE(User.updated_at) == date.today()).all()
print(now_update)

now_update_two = (db.session.query(User)
                  .filter(cast(User.updated_at, Date) == date.today())
                  .all())
print(now_update_two)

# or , just like sql

register_after_2012 = db.session.query(User).filter(User.created_at >= '2012-10-26').all()
print(register_after_2012)
register_between_a_and_b = (db.session.query(User)
                            .filter(
    and_(User.created_at >= '2012-10-25', User.created_at <= '2021-10-26')).all())
print(register_between_a_and_b)
register_between_a_and_b_two = (db.session.query(User)
                                .filter(User.created_at.between('2012-10-25', '2039-10-26')).all())
print(register_between_a_and_b_two)
