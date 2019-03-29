import flask


@app.route('/<int:goal_num>/<string:start_date>/<string:end_date>/<int:start_hour>/<int:end_hour>/<string:days_of_week>')
def get_data():
    return 'Hello, World!'