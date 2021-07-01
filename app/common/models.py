from app.common.extensions import db
from flask import url_for
from typing import Union
from datetime import datetime
from datetime import timedelta


class TimestampMixin():
    meta = {
        'indexes': [
            {
                'name': 'Transaction_index',
                'fields': ['time_expires'],
                'expireAfterSeconds': 0
            }
        ]
    }
    time_created = db.DateTimeField(default=datetime.utcnow())
    time_updated = db.DateTimeField()
    time_expires = db.DateTimeField()


    def update_activity(self):
        self.time_updated = datetime.utcnow()
    
    def set_expire_at(self, seconds):
        self.update_activity()
        self.time_expires = self.time_updated + timedelta(seconds=seconds)

    def save(self, *args, **kwargs):
        self.update_activity()
        return super(db.Document, self).save(*args, **kwargs)