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

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    symb = Column(String)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    categoryId = Column(Integer, ForeignKey("categories.id"))
    scopeId = Column(Integer, ForeignKey("scopes.id"))
    isActive = Column(Boolean)

    category = relationship("Category", back_populates="items")
    scope = relationship("Scope", back_populates="items")

class Factor(Base):
    __tablename__ = "factors"

    id = Column(Integer, primary_key=True, index=True)
    valeur = Column(Integer)
    uniteId = Column(Integer, ForeignKey("units.id"))
    isActive = Column(Boolean)
    itemId = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="factors")
    unite = relationship("Unit")

# Create tables in the database
Base.metadata.create_all(bind=engine)