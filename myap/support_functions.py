# aux functions that don't have a client call and response
from myap.models import Currency, Teams, PastGames


def get_currency_list():
    currency_list = list()
    import requests
    from bs4 import BeautifulSoup
    url = "https://thefactfile.org/countries-currencies-symbols/"
    response = requests.get(url)
    if not response.status_code == 200:
        return currency_list
    soup = BeautifulSoup(response.content)
    data_lines = soup.find_all('tr') #lines in the list
    for line in data_lines:
        try:
            detail = line.find_all('td')
            currency = detail[2].get_text().strip()
            iso = detail[3].get_text().strip()
            if (currency, iso) in currency_list:
                continue
            currency_list.append((currency, iso))
        except:
            continue
    return currency_list

def add_currencies(currency_list):
    for currency in currency_list:
        currency_name = currency[0]
        currency_symbol = currency[1]
        try:
            c= Currency.objects.get(iso=currency_symbol)
        except:
            c = Currency(long_name=currency_name, iso=currency_symbol)
            #c.save() #To test out the code, replace this by print(c)
            print(c)

def get_teams():
    import requests
    from bs4 import BeautifulSoup
    url = 'https://www.scoresandodds.com/nba/futures'
    short_out = list()
    long_out = list()
    all_out = list()
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    data_lines = soup.find_all('span', {'class': 'team-nameplate'})
    for i in data_lines:
        short_out = i.find_all('span', {'class': 'team-emblem'})[0].get_text().strip()
        long_out = i.find_all('a')[0].get_text().strip()
        if [short_out, long_out] not in all_out:
            all_out.append([short_out, long_out])

        # print(i.find_all('span',{'class': 'team-emblem'}))
    return(all_out)

def add_teams(team_list):
    for teams in team_list:
        short_names = teams[0]
        long_names = teams[1]
        try:
            t = Teams.objects.get(short_name=short_names)
        except:
            t = Teams(short_name=short_names, long_name=long_names)
            print(t)
            t.save()

def add_scores(season_scores):
    for games in season_scores:
        teamhome = games[3]
        mlhome = games[4]
        scorehome = games[5]
        teamaway = games[0]
        mlaway = games[1]
        scoreaway = games[2]
        date = games[6]
        try:
            s = PastGames.objects.get(home_team=teamhome,
                                      home_score=scorehome,
                                      home_money_line=mlhome,
                                      away_team=teamaway,
                                      away_score=scoreaway,
                                      away_money_line=mlaway,
                                      game_date=date)
        except:
            s = PastGames(home_team=teamhome,
                                      home_score=scorehome,
                                      home_money_line=mlhome,
                                      away_team=teamaway,
                                      away_score=scoreaway,
                                      away_money_line=mlaway,
                                      game_date=date)
            #print(s)
            s.save()

def get_currency_rates(iso_code):
    url = "http://www.xe.com/currencytables/?from=" + iso_code
    import requests
    from bs4 import BeautifulSoup
    x_rate_list = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content)
    except:
        return x_rate_list
    data = page_source.find('tbody')
    data_lines = data.find_all('tr')
    for line in data_lines:
        symbol = line.find('th').get_text()
        data=line.find_all('td')
        try:
            x_rate = float(data[2].get_text().strip())
            x_rate_list.append((symbol,x_rate))
        except:
            continue
    return x_rate_list

def get_results():
    import requests
    from bs4 import BeautifulSoup
    import re
    import datetime
    from datetime import date, timedelta
    yesterday=date.today()-timedelta(days=1)
    season_start=datetime.date(2022,10,18)
    #print(season_start+timedelta(days=1))
    counter = season_start
    list_of_dates=list()
    while counter <= yesterday:
        list_of_dates.append(str(counter))
        counter += timedelta(days=1)
    #list_of_dates
    team_away = list()
    team_home = list()
    ml_away = list()
    ml_home = list()
    away_score = list()
    home_score = list()
    final_game_list = list()
    print('dates in')
    for day_in in list_of_dates:
        url = 'https://www.scoresandodds.com/nba?date='+day_in
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.text)
        all_games = soup.find_all('table', {'class': 'event-card-table'})
        for game in all_games:

            #populate the home team and away team lists, change to class database population in pycharm
            #this needs work

            team_away = (game.find_all('span', {'class': 'team-emblem'})[0].get_text().strip())
            team_home = (game.find_all('span', {'class': 'team-emblem'})[1].get_text().strip())

            #populate MLs
            if game.find_all('td', {'data-field': 'live-moneyline'})[0].get_text().strip() == 'even':
                ml_away = (0)
            else:
                ml_away = (int(game.find_all('td', {'data-field': 'live-moneyline'})[0].get_text().strip()))
            if game.find_all('td', {'data-field': 'live-moneyline'})[1].get_text().strip() == 'even':
                ml_home = (0)
            else:
                ml_home = (int(game.find_all('td', {'data-field': 'live-moneyline'})[1].get_text().strip()))

            #populate final score
            away_score = (int(game.find_all('td', {'class': re.compile('event-card-score*')})[0].get_text().strip()))
            home_score = (int(game.find_all('td', {'class': re.compile('event-card-score*')})[1].get_text().strip()))
            final_game_list.append([team_away,ml_away,away_score,team_home,ml_home,home_score,day_in])
            #print(final_game_list)
    return(final_game_list)