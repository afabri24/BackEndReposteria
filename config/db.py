from sqlalchemy import create_engine, MetaData

# engine = create_engine('mysql+pymysql://sql5699343:TUBEuTZEl6@sql5.freesqldatabase.com:3306/sql5699343')
engine = create_engine('mysql+pymysql://adminReposteria:123456789@127.0.0.1:3306/reposteriarosario')
<<<<<<< Updated upstream

=======
#engine = create_engine('mysql+pymysql://root:Man159753@localhost/reposteriarosario')
>>>>>>> Stashed changes
meta_data = MetaData()