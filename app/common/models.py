from app.common.extensions import db
from flask import url_for
from sqlalchemy.sql import func
from typing import Union

class BaseMixin:
    id = db.Column(db.Integer, primary_key=True)

    def commit(self) -> Union[object, None]:
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as Error:
            db.session.rollback()
            raise Error

class TimestampMixin:
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class PaginatedAPIMixin:
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data