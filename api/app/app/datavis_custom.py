import functools

from flask import request, make_response, abort, redirect, url_for
from sqlalchemy import func

from app.main import app as api, db, cache, SetEncoder, NetflixWatchMetadata, dateparser
from app.dataviz_api import get_api_root, query_args
import inspect
import sys
import json


def documented_route(*route_args, **route_kwargs):
    doc_name = route_kwargs["documentation_name"]
    description = route_kwargs.get("description", "")
    del route_kwargs["documentation_name"]

    def outer(action_function):
        @api.route(*route_args, **route_kwargs)
        @functools.wraps(action_function)
        def inner(*f_args, **f_kwargs):
            return action_function(f_args, f_kwargs)

        inner.endpoint = route_args[0]
        inner.documentation_name = doc_name
        inner.description = description
        return inner

    return outer


@api.route("/api/custom", methods=['GET'])
def get_custom_links():
    functions = [{"name": f.documentation_name, "href": get_api_root()[:-1] + f.endpoint} for name, f in
                 inspect.getmembers(sys.modules[__name__]) if
                 inspect.isfunction(f) and hasattr(f, "documentation_name")]

    return json.dumps(functions, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@documented_route("/api/custom/thumbnails/latest/weekly", methods=['GET'],
                  documentation_name="thumbnails-from-last-week")
def get_latest_logs_alias1(*args, **kwargs):
    return redirect(get_api_root() + "api/thumbnails/latest?since=last+week&limit=-1")


@documented_route("/api/custom/thumbnails/latest/monthly", methods=['GET'],
                  documentation_name="thumbnails-from-last-month")
def get_latest_logs_alias2(*args, **kwargs):
    return redirect(get_api_root() + "api/thumbnails/latest?since=last+month&limit=-1")


@documented_route("/api/custom/watches/latest/weekly", methods=['GET'], documentation_name="watches-from-last-week")
def get_latest_watches_alias1(*args, **kwargs):
    return redirect(get_api_root() + "api/watches/latest?since=last+week&limit=-1")


@documented_route("/api/custom/watches/latest/monthly", methods=['GET'], documentation_name="watches-from-last-month")
def get_latest_watches_alias2(*args, **kwargs):
    return redirect(get_api_root() + "api/watches/latest?date_from=last+month&limit=-1")


@documented_route("/api/custom/watches/tops/forever", methods=['GET'], documentation_name="watches-tops-forever")
def get_tops_forever(*args, **kwargs):
    return redirect(get_api_root() + "api/custom/watches/tops?date_from=1900")


@documented_route("/api/custom/watches/tops/last-week", methods=['GET'], documentation_name="watches-tops-last-week")
def get_tops_last_week(*args, **kwargs):
    return redirect(get_api_root() + "api/custom/watches/tops?date_from=last+week")


@documented_route("/api/custom/watches/tops/last-month", methods=['GET'], documentation_name="watches-tops-last-month")
def get_tops_last_month(*args, **kwargs):
    return redirect(get_api_root() + "api/custom/watches/tops?date_from=last+month")


@api.route("/api/custom/watches/tops", methods=['GET'])
@query_args(date_from="last week", date_to="now")
def get_tops(date_from, date_to):
    from_date = dateparser.parse(date_from)
    to_date = dateparser.parse(date_to)
    watches = db.session.query(NetflixWatchMetadata.video_id, func.count(NetflixWatchMetadata.id)) \
        .filter(NetflixWatchMetadata.timestamp >= from_date) \
        .filter(NetflixWatchMetadata.timestamp <= to_date) \
        .group_by(NetflixWatchMetadata.video_id) \
        .order_by(func.count(NetflixWatchMetadata.id).desc()).all()

    res = [{"video_id": video_id, "count": count, "links": {
        "rel": "content",
        "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{video_id}"
    }} for video_id, count in watches]

    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}
