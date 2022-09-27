from collections import namedtuple
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util

display_day = None
display_league = None

OTHER_LEAGUE = {'AL': 'NL', 'NL': 'AL'}
LEAGUE_NAME = {'AL': 'American League', 'NL': "National League"}


def index(request):
    global display_day, display_league
    if not display_day:
        display_day = util.start_of_season()
    if not display_league:
        display_league = 'AL'
    context = {"date": display_day,
               "league": display_league,
               "openingDay": util.start_of_season(),
               "closingDay": util.end_of_season()}
    return render(request, "baseball/index.html", context)


def standings(request):
    global display_day, display_league

    error, d, l = parse_parameters(request)
    if error:
        context = {"error": error}
        return render(request, "baseball/standings.html", context)

    display_day = d
    display_league = l
    standings = util.standings(d, l)
    estandings = [util.extend_record(s) for s in standings]
    context = {"standings": estandings,
               "date": d,
               "openingDay": util.start_of_season(),
               "closingDay": util.end_of_season(),
               "league": LEAGUE_NAME[l],
               "other": OTHER_LEAGUE[l],
               "final": d == util.end_of_season()}
    return render(request, "baseball/standings.html", context)


def parse_parameters(request):
    if "date" not in request.GET:
        return "Missing 'date' parameter", None, None
    try:
        date_str = request.GET["date"]
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return f"Invalid date: '{date_str}'", None, None
    if d > util.end_of_season():
        return f'Season ended on {util.end_of_season()}', None, None
    if d < util.start_of_season():
        return f'Season did not begin until {util.start_of_season()}', None, None

    if "league" not in request.GET:
        return "Missing 'league' parameter", None, None
    league = request.GET["league"]
    if league not in ['AL', 'NL']:
        return f"Invalid league: '{league}'", None, None

    return None, d, league


def advance_date(request):
    global display_day, display_league
    
    if request.GET["advance_date"] == "Previous Day":
        new_date = max(display_day-timedelta(days=1), util.start_of_season())
    elif request.GET["advance_date"] == "Next Day":
        new_date = min(display_day+timedelta(days=1), util.end_of_season())
    else:
        new_date = display_day
    print(f'new day: {new_date}')
    return HttpResponseRedirect(f'{reverse("baseball:standings")}?date={new_date}&league={display_league}')
