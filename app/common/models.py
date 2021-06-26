from app.common.extensions import db
from flask import url_for
from typing import Union
from datetime import datetime


class TimestampMixin():
    creation_date = db.DateTimeField(default=datetime.utcnow)
    modified_date = db.DateTimeField()

    def update_activity(self):
        self.modified_date = datetime.utcnow

    def save(self, *args, **kwargs):
        self.update_activity()
        return super(db.Document, self).save(*args, **kwargs)