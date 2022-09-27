from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from datetime import datetime
from . import util

# Create your views here.
def index(request):    
    if request.method == "GET" and "date" in request.GET:  
        date_str = request.GET["date"]
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
        league = request.GET["league"]
        if d < util.start_of_season():
            return render (request, "baseball/index.html", {"errormsg":"Please select a valid date"})
        else:            
            if d >= util.end_of_season():
                message = util.league_name(league) + " final standings"
                final = True
            else:
                message = util.league_name(league) + " standings on " 
                final = False
            standings = util.standings(d, league)
            context = {"standings": standings, "date": d, "datestr": date_str, "message": message, "final_standings":final}
            return render(request, "baseball/index.html", context)
    else:  
        context = {"datestr": "1967-04-10"}
        return render(request, "baseball/index.html", context)

