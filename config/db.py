from sqlalchemy import create_engine, MetaData

#engine = create_engine('mysql+pymysql://adminReposteria:@db-mysql-nyc3-66165-do-user-14328275-0.c.db.ondigitalocean.com:25060/reposteriarosario?ssl-mode=REQUIRED')
#engine = create_engine('mysql+pymysql://adminReposteria:123456789@127.0.0.1:3306/reposteriarosario')
engine = create_engine('mysql+pymysql://root:Man159753@localhost/reposteriarosario')
meta_data = MetaData()