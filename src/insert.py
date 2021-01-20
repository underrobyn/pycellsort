from models import engine, Sector, Node
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


#session.add()
session.commit()