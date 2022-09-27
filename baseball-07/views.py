from django.shortcuts import render
from datetime import datetime
from . import util

# Create your views here.


def index(request):
    return render(request, "baseball/index.html")

def standings(request):
    date_str = request.GET["date"]
    # assumes date is valid
    league_name = request.GET["league"]
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    standings = util.standings(d, league=league_name)
    if standings == []:
        return render(request, "baseball/index.html")

    for s in range(len(standings)):
        standings[s] = util.extend_record(standings[s])
    ext_standings = []
    for s in standings:
        code = s.code
        name = util.team_name(code)
        url = util.team_logo(code)
        wins = s.wins
        losses = s.losses
        pct = s.pct_str
        gb = s.gb
        ext_standings.append((code, name, url, wins, losses, pct, gb))
    context = {"ext_standings": ext_standings, "date": d, "league": league_name}
    return render(request, "baseball/standings.html", context)


def logos(request):
    d = datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    standings = []
    for l in ['AL', 'NL']:
        standings.extend(util.standings(d, league=l))
    logos = []
    for i in range(len(standings)):
        standings[i] = util.extend_record(standings[i])
    for s in standings:
        code = s.code
        name = util.team_name(code)
        url = util.team_logo(code)
        wins = s.wins
        losses = s.losses
        pct = s.pct_str
        gb = s.gb
        logos.append((code, name, url, wins, losses, pct, gb))
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
