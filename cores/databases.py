from datetime import datetime
import uuid

from cores.extensions import db  # sqlalchemy

# from flask-cookiecutter
"""Database module, including the SQLAlchemy database object and DB-related utilities."""

# Alias common SQLAlchemy names
basestring = (str, bytes)
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            db.session.commit()
        return "success"


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):  # pragma: no cover
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


class PkModelWithManageAttr(PkModel):
    """
    Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``.
    and Manage Attr : is_deleted, created_at & updated_at
    """

    __abstract__ = True

    is_deleted = Column(db.Boolean, default=False)

    created_at = Column(db.DateTime, default=datetime.now())
    updated_at = Column(db.DateTime, default=datetime.now())

    def save(self, commit=True):
        """override method save"""
        self.updated_at = datetime.now()

        super().save(commit)

    def update(self, commit=True, **kwargs):
        """override method update"""
        if not commit:
            self.updated_at = datetime.now()

        super().update(commit, **kwargs)


def reference_col(tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )


def generate_id():
    """auto generate id"""
    return str(uuid.uuid4().hex)
