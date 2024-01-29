from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Scope(Base):
    __tablename__ = "scopes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    
    items = relationship("Item", back_populates="scope")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    
    items = relationship("Item", back_populates="category")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    symb = Column(String)
    
    factors = relationship("Factor", back_populates="unit")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    categoryId = Column(Integer, ForeignKey("categories.id"))
    scopeId = Column(Integer, ForeignKey("scopes.id"))
    isActive = Column(Boolean)

    category = relationship("Category", back_populates="items")
    scope = relationship("Scope", back_populates="items")
    
    factors = relationship("Factor", back_populates="item")

class Factor(Base):
    __tablename__ = "factors"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)
    unitId = Column(Integer, ForeignKey("units.id"))
    isActive = Column(Boolean)
    itemId = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="factors")
    unit = relationship("Unit", back_populates="factors")

# Create tables in the database
Base.metadata.create_all(bind=engine)