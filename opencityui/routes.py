from flask import abort
from opencityui.station_statistics import stat_station
from opencityui.app import app
import json


@app.route(
    '/<int:goal_num>/<string:start_date>/<string:end_date>/<int:start_hour>/<int:end_hour>/<string:days_of_week>')
def get_data(goal_num, start_date, end_date, start_hour, end_hour, days_of_week):
    try:
        split_days = [int(i) for i in days_of_week.split(",")]
        start_hour = int(start_hour)
        end_hour = int(end_hour)
    except ValueError:
        return abort(400)
    ret = stat_station(goal_num, start_date, end_date, start_hour=start_hour, end_hour=end_hour,
                       days_of_week=split_days)
    return json.dumps(ret)
