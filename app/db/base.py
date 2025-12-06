from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime


# Base class for all models
Base = declarative_base()


class BaseModel(Base):
    """
    Base model with common fields for all tables
    All models inherit from this class
    """
    __abstract__ = True  # This won't create a table
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """
        String representation of model
        """
        return f"<{self.__class__.__name__}(id={self.id})>"