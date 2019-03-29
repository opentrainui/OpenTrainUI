from typing import Iterable, Tuple

from functools import lru_cache

from opencityui.otrain_adapter.methods import path_info
from opencityui.origins import origins

origins = lru_cache(1)(origins)


def time_filter_coff(start_date: str, end_date: str,
                     start_hour: int = 0, end_hour: int = 24,
                     day_of_week_filter: Iterable[int] = ()):
    # for now, start and end date is not checked, since the query handles it
    day_of_week_filter = [(i + 1) in day_of_week_filter for i in range(7)]

    def ret(dow: int, hours: Tuple[int, int]):
        if not day_of_week_filter[dow - 1]:
            return 0
        min_h, max_h = hours
        max_lim = min(max_h, end_hour)
        min_lim = max(min_h, start_hour)
        if min_lim < max_lim:
            return 0
        return (max_lim - min_lim) / (end_hour - start_hour)

    return ret


def stat_path(origin_station, goal_station, start_date: str, end_date: str, filter_coff_func):
    routes = path_info(start_date, end_date, origin_station, goal_station)
    pop_sum = 0
    late_chance_sum = 0
    for route in routes:
        dow = route['info']['week day']
        hours = routes['info']['hours']
        filter_coff = filter_coff_func(dow, hours)
        if filter_coff == 0:
            continue
        pop = route['info']['num_trips'] * filter_coff
        late_chance = route['stops'][-1]['arrival_late_pct']
        pop_sum += pop
        late_chance_sum += late_chance
    if pop_sum == 0:
        return None
    return late_chance_sum / pop_sum


def stat_station(goal_num, start_date: str, end_date: str, **filter_kwargs):
    filter_coff_func = time_filter_coff(start_date, end_date, **filter_kwargs)
    ret = {}
    for o_name, o_num, line_name, line_num in origins():
        if o_num in ret:
            continue
        value = stat_path(o_name, goal_num, start_date, end_date, filter_coff_func)
        if value is None:
            continue
        ret[o_name] = value
    return ret
