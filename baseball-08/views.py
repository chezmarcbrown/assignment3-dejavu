from django.shortcuts import render
from datetime import datetime
from . import util

# Create your views here.


def index(request):
    return render(request, "baseball/index.html")


def standings(request):
    date_str = request.GET["date"]
    league = request.GET["league"]
    # assumes date is valid
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return render(request, "baseball/index.html", {"errormsg":"Please enter a valid date"})
    if date_str < "1967-04-01" or date_str > "1967-10-31":
        return render(request, "baseball/index.html", {"errormsg":"Please enter a valid date"})
    standings = util.standings(d, league)
    team_names = []
    for s in standings:
        code = s.code
        name = util.team_name(code)
        team_names.append((code, name))
    context = {"standings": standings, "date": d, "league": league, "team_names":team_names}
    return render(request, "baseball/standings.html", context)
   

   


def logos(request):
    d = datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    standings = []
    for l in ['AL', 'NL']:
        standings.extend(util.standings(d, league=l))
    logos = []
    for s in standings:
        code = s.code
        name = util.team_name(code)
        url = util.team_logo(code)
        logos.append((code, name, url))
    return render(request, "baseball/logos.html", {"logos": logos})


def redsox(request):
    return oneteam("BOS")


def oneteam(request, code):
    code = code.upper()
    name = util.team_name(code)
    url = util.team_logo(code)
    return render(request, "baseball/oneteam.html",
                  {"code": code, 
                  "team_name": name, 
                  "team_logo_url": url,
                  "opening_day": util.start_of_season(),
                  "last_day": util.end_of_season() })
