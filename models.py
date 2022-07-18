from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text, LargeBinary, DateTime


class CarBrand(Base):
    __tablename__='brands'
    id=Column(String, primary_key=True)
    name=Column(String(255), nullable=False)
    description=Column(Text)
    is_active=Column(Boolean, default=False)
    logo=Column(Text, default=False)
    model_count=Column(Integer)
    last_update=Column(DateTime)

    def __repr__(self):
        return f"<CarBrand name={self.name} description={self.description}>"
