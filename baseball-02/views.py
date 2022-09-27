from django.shortcuts import render
from datetime import date, datetime
from . import util

# Create your views here.


def index(request):
    return render(request, "baseball/index.html")


def standings(request):
    date_str = request.GET["date"]
    league_in = request.GET["region"]
    # date parsing and checking
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    if(year > 1967 or year < 1967
       or month > 12 or month < 1
       or day > 31 or day < 1):
        # invalid date redirects to homepage (in this case, /index.html)
        return render(request, "baseball/index.html", {"datemsg":"ERROR: Invalid date"})
    # otherwise, date is good
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # if the region/league option is empty, display an error message
    # else, make list of rankings based on the league that was selected
    if(league_in=="null"):
        return render(request, "baseball/standings.html", {"datestr": date_str, "errormsg":"ERROR: Choose a league to view."})
    else:
        stnd = util.standings(d, league_in)
    standings =[]
    
    # make an exteded record
    for s in stnd:
        standings.append(util.extend_record(s))
    context = {"standings": standings, "date": d, "datestr":date_str, "leaguein":league_in}
    
    #if the date is greater than or = to the end of season, print "Final Standings" on page
    if(d >= util.end_of_season()):
        return render(request, "baseball/standings.html",
                      {"standings": standings, "date": d, "datestr":date_str, "leaguein":league_in, "post_szn":"Final Standings of 1967 Season"})
    else:
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
