```


from sqlalchemy import Date, cast
from datetime import date

from sqlalchemy import func

saved_days = os.getenv('SAVED_DAYS', 10)

ten_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=saved_days)

session.query(db.Transaction).filter(func.DATE(db.Transaction.datetime) == date.today())

my_date = (session.query(MyObject)
      .filter(cast(MyObject.date_time, Date) == date.today())
      .all())


#or , just like sql

query = session.query(MyObject).filter(MyObject.create_time >= '2012-10-26')

query = (session.query(MyObject)
         .filter(and_(MyObject.create_time >='2012-10-25', MyObject.create_time <= '2012-10-26')))

query = (session.query(MyObject)
        .filter(MyObject.create_time.between('2012-10-25', '2012-10-26')))

        
```
