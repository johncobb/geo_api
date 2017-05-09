



from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from geoalchemy2 import Geometry



from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

class MyGeom(UserDefinedType):
    def get_col_spec(self):
        return 'GEOMETRY'

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)





metadata = MetaData()

engine = create_engine('mysql+pymysql://root:Password1@localhost/geodesity', echo=True)

lake_table = Table('lake', metadata, Column('id', Integer, primary_key=True), Column('name', String(255)), Column('geom', Geometry('POLYGON')))

#lake_table.create(engine)
metadata.create_all(engine)







