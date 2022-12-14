from django.shortcuts import render
from datetime import datetime
from . import util

# Create your views here.


def index(request):
    return render(request, "baseball/index.html")


def standings(request):
    league_play=request.GET["league"]
    date_str = request.GET["date"]
    # assumes date is valid
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
        if util.valid_date(d):
            standings = util.standings(d, league=league_play)
            context = {"standings": standings, "date": d, "league":league_play}
            return render(request, "baseball/standings.html", context)
        elif util.after_season(d): #if last season day or after
            standings = util.standings(util.end_of_season(), league=league_play)
            context = {"standings": standings, "date": util.end_of_season(), "end": "F ", "league":league_play}
            return render(request, "baseball/standings.html", context)
        else:
            return render(request,"baseball/index.html", {"errorMsg" :"Invalid date entered, please try again."})
    except (ValueError):
        return render(request, "baseball/index.html", {"errorMsg": "Invalid date entered, please try again."})



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

