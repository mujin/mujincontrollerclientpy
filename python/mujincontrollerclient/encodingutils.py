# -*- coding: utf-8 -*-

import json
import tzlocal
import datetime

import logging
log = logging.getLogger(__name__)


class DatetimeEncoder(json.JSONEncoder):
    """Extends the default JSON encoder to support datetime.datetime and datetime.timedelta objects
    """
    def default(self, obj):
        # handle datetime objects
        if isinstance(obj, datetime.datetime):
            if obj.tzinfo is None:
                # attach the local timezone
                obj = obj.replace(tzinfo=tzlocal.get_localzone())
            return obj.isoformat()

        # encode timedelta objects into millisecond values
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()*1000

        return json.JSONEncoder.default(self, obj)


