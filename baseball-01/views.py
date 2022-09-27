from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from . import util

# Create your views here.


def index(request):
    return render(request, "baseball/index.html")


def standings(request):
    date_str = request.GET["date"]
    
    league_choice = request.GET["league"]

    # reloads page if user deletes preset date and submits form with mm/dd
    test_date = date_str.replace("-", "")
    if test_date.isnumeric():
        pass
    else:
        return render(request, "baseball/index.html")
    
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # reloads page if somehow user enters invalid date and no records exist
    standings = util.standings(d, league=league_choice)
    if standings == []:
        return render(request, "baseball/index.html") 

    for s in range(len(standings)):
        standings[s] = util.extend_record(standings[s])
    extended_standings = []
    for s in standings:
        code = s.code
        name = util.team_name(code)
        url = util.team_logo(code)
        wins = s.wins
        losses = s.losses
        pct = s.pct_str
        gb = s.gb
        extended_standings.append((code, name, url, wins, losses, pct, gb))

        context = {"extended_standings": extended_standings, "date": d, "league": league_choice, "test_date": test_date}
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
