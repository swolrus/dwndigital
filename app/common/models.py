from app.common.extensions import db
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