import os
from flask import current_app as app
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

import json

def toJSON(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)