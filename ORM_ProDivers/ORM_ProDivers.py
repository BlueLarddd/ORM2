import pymysql

from sqlalchemy import Integer, String, Column, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from prettytable import PrettyTable

engine = create_engine(f'mysql+pymysql://student:Hn523cv-@95.154.68.63:3306/[Prodivers_LD_DB]')

session = Session(bind=engine)

Base = declarative_base()

products = Table('products', Base.metadata,
    Column('category_id', Integer(), ForeignKey("categories.id")),
    Column('storage_id', Integer(), ForeignKey("storage.id")),
)

class Prod(Base):
    tablename = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    storage_id = Column(Integer, ForeignKey('storage.id'))

    def add_type(self, type_name):
        t = Prod(name=type_name)
        session.add(t)
        session.commit()

    def get_type(self):
        query = text('SELECT * FROM products')
        result = session.execute(query)
        t = PrettyTable(['id', 'name', 'price', 'category_id', 'storage_id'])
        for row in result:
            t.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(f'\n{t}\n')

    def upd_type(self, old_type_name, new_type_name):
        t = session.query(Prod).filter(Prod.name == old_type_name).one()
        t = t.id
        ty = session.query(Prod).get(t)
        ty.name = new_type_name
        session.add(ty)
        session.commit()

    def del_type(self, type_name):
        t = session.query(Prod).filter(Prod.name == type_name).one()
        session.delete(t)
        session.commit()
