from app.database.database import Base
from sqlalchemy import column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
class Url_Short(Base):
    __tablename__="url_data"

    id : Mapped[int]=mapped_column(Integer,index=True,primary_key=True,unique=True)
    original_url:Mapped[str]=mapped_column(String,nullable=False)
    short_url:Mapped[str]= mapped_column(String,unique=True,nullable=False)
    click_count :Mapped[int]=mapped_column(Integer,default=0,nullable=False)
    created_at :Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,nullable=False)
