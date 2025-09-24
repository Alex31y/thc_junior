import os
from . import schemas
from sqlalchemy import create_engine, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Query, Session, declarative_base, sessionmaker, relationship

database_url = os.getenv("DATABASE_URL", "postgresql://dnl@localhost/dnl")
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)

    categories = relationship("Category", back_populates="manufacturer")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer_id = Column(
        Integer,
        ForeignKey("manufacturers.id", onupdate="RESTRICT", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    name = Column(Text)

    manufacturer = relationship("Manufacturer", back_populates="categories")
    models = relationship("Model", back_populates="category")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", onupdate="RESTRICT", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    name = Column(Text)

    category = relationship("Category", back_populates="models")
    parts = relationship("Part", back_populates="model")


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(
        Integer,
        ForeignKey("models.id", onupdate="RESTRICT", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    number = Column(Text)
    name = Column(Text)

    model = relationship("Model", back_populates="parts")


def paginate(query: Query, page: int = 1, per_page: int = 10) -> Query:
    return query.offset((page - 1) * per_page).limit(per_page)


def select_manufacturers(session: Session, *, q: str | None) -> Query[Manufacturer]:
    query = session.query(Manufacturer)
    if q is not None:
        query = query.where(Manufacturer.name.ilike(f"%{q}%"))
    return query.order_by(Manufacturer.id)


def insert_manufacturer(session: Session, **kwargs) -> schemas.Manufacturer:
    manufacturer = Manufacturer(**kwargs)
    session.add(manufacturer)
    session.commit()
    return manufacturer


def select_categories(session: Session, *, manufacturer_id: int, q: str | None) -> Query[Category]:
    query = session.query(Category).where(Category.manufacturer_id == manufacturer_id)
    if q is not None:
        query = query.where(Category.name.ilike(f"%{q}%"))
    return query.order_by(Category.id)


def insert_category(session: Session, **kwargs) -> schemas.Category:
    category = Category(**kwargs)
    session.add(category)
    session.commit()
    return category


def select_models(session: Session, *, category_id: int, q: str | None) -> Query[Model]:
    query = session.query(Model).where(Model.category_id == category_id)
    if q is not None:
        query = query.where(Model.name.ilike(f"%{q}%"))
    return query.order_by(Model.id)


def insert_model(session: Session, **kwargs) -> schemas.Model:
    model = Model(**kwargs)
    session.add(model)
    session.commit()
    return model


def select_parts(session: Session, *, model_id: int, q: str | None) -> Query[Part]:
    query = session.query(Part).filter(Part.model_id == model_id)
    if q is not None:
        query = query.filter(Part.name.ilike(f"%{q}%") or Part.number.ilike(f"%{q}%"))
    return query.order_by(Part.id)


def insert_part(session: Session, **kwargs) -> schemas.Part:
    part = Part(**kwargs)
    session.add(part)
    session.commit()
    return part
