from src.config import db


class BaseModel(db.Model):
    __abstract__ = True  # This ensures that SQLAlchemy doesn't create a table for this class

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id)
