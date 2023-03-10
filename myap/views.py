from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from myap import support_functions
from myap.models import Currency, AccountHolder, Teams, PastGames, TodayLines, Bets


#from django.http import HttpResponseRedirect
#from django.urls import reverse

# Create your views here.

def home(request):
    data = dict()
    import datetime
    time = datetime.datetime.now() #time sitting on the server
    data['time_of_day'] = time
    print(data) #print goes to line here, not browser. must be sent to template.
    return render(request,'home.html',context=data) #wtf is context??

def maintenance(request):
    data = dict()
    try:
        choice = request.GET['selection']
        if choice == "currencies":
            support_functions.add_currencies(support_functions.get_currency_list())
            c_list = Currency.objects.all()
            #print("Got c_list", len(c_list))
            data['currencies'] = c_list
            #return HttpResponseRedirect(reverse('currencies'))
        if choice == 'teams':
            support_functions.add_teams(support_functions.get_teams())
            t_list = Teams.objects.all()
            print('Got t list', len(t_list))
            data['teams'] = t_list
            #return HttpResponseRedirect(reverse('teams'))
        if choice == 'lines':
            for i in TodayLines.objects.all():
                i.delete()
            print('past lines delete')
            line_pull = support_functions.get_line_today()
            support_functions.add_lines(line_pull)
            today_line = TodayLines.objects.all()
            print('Got lines'), len(today_line)
            data['line'] = today_line
        if choice == 'clear':
            for i in Teams.objects.all():
                i.delete()
            print('teams delete')
            for i in TodayLines.objects.all():
                i.delete()
            print('lines delete')
            for i in PastGames.objects.all():
                i.delete()
            print('past delete')
            for i in Bets.objects.all():
                i.delete()
            print('bets delete')
        if choice == 'past':
            for i in PastGames.objects.all():
                i.delete()
            print('past games deleted')
            game_pull = support_functions.get_results()
            support_functions.add_scores(game_pull)
            past_list = PastGames.objects.all()
            print('Got t list', len(past_list))
            data['past'] = past_list
        if choice == "bets":
            for i in Bets.objects.all():
                i.delete()
            print('past bets deleted')
            support_functions.add_bet_rank(support_functions.get_bet_rank())
            b_list = Bets.objects.all()
            print('got b list', len(b_list))
            data['ranked_bets'] = b_list
    except:
        pass
    return render(request, "maintenance.html", context=data)

def view_currencies(request):
    data = dict()
    c_list = Currency.objects.all()
    data['currencies'] = c_list
    return render(request,'currencies.html',context=data)

def currency_selection(request):
    data = dict()
    currencies =Currency.objects.all()
    data['currencies'] = currencies
    return render(request,"currency_selector.html",data)

def view_teams(request):
    data = dict()
    t_list = Teams.objects.all()
    data['teams'] = t_list
    return render(request,'teams.html',context=data)

def view_past(request):
    data = dict()
    past_list = PastGames.objects.all()
    data['past'] = past_list
    return render(request,'past.html',context=data)

def view_lines(request):
    data = dict()
    today_line = TodayLines.objects.all()
    data['line'] = today_line
    return render(request,'lines.html',context=data)
def exch_rate(request):
    data=dict()
    try:
        currency1 = request.GET['currency_from']
        currency2 = request.GET['currency_to']
        c1 = Currency.objects.get(iso=currency1)
        c2 = Currency.objects.get(iso=currency2)

        data['currency1'] = c1
        data['currency2'] = c2
        try:
            rate = c1.rates_set.get(x_currency=c2.iso).rate #all rates associated w/ c1 -> get the rate w/ c2
            data['rate'] = rate
        except:
            data['rate'] = "Not Available"
    except:
        pass
    return render(request,"exchange_detail.html",data)

def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user,date_of_birth=dob)
        acct_holder.save()
        return render(request,"home.html",context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, "registration/register.html", context)

def bets(request):
    data = dict()
    rankings = Bets.objects.all()
    data['ranked_bets'] = rankings
    return render(request, "bets.html", context=data)