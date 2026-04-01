from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import datetime
from db.database import Base

class RecordType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    record_type = Column(Enum(RecordType), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    notes = Column(String, nullable=True)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User")
