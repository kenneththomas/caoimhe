import requests
import json
import time
import termcolor
import datetime

storage = {}
previous_payloads = []

class GameInfo:
    def __init__(self, id, team1, team2, last_play, team1_score, team2_score, downDistanceText, time_qtr):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.last_play = last_play
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.downDistanceText = downDistanceText
        self.time_qtr = time_qtr

def scoreboard_request():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        scoreboarddata = json.dumps(data, indent=4)

    else:
        print("Error: Unable to fetch data from the ESPN API")

    return data



def sb_parser(scoreboard_data):

    eventcount = len(scoreboard_data['events'])
    for evc in range(eventcount):

        #if the event is not live, skip it
        if scoreboard_data['events'][evc]['status']['type']['completed'] == True:
            continue

        id = scoreboard_data['events'][evc]['id']
        team1 = scoreboard_data['events'][evc]['competitions'][0]['competitors'][0]['team']['location']
        team2 = scoreboard_data['events'][evc]['competitions'][0]['competitors'][1]['team']['location']

        #print(f'{team1} vs {team2}')
        sb_key = f'{id}_{team1}_{team2}'
        #print(sb_key)
        try:
            last_play = scoreboard_data['events'][evc]['competitions'][0]['situation']['lastPlay']['text']
        except:
            last_play = 'No last play available'
        #print(last_play)
        team1_score = scoreboard_data['events'][evc]['competitions'][0]['competitors'][0]['score']
        team2_score = scoreboard_data['events'][evc]['competitions'][0]['competitors'][1]['score']
        #print(f'{team1} {team1_score} - {team2} {team2_score}')

        try:
            downDistanceText = scoreboard_data['events'][evc]['competitions'][0]['situation']['downDistanceText']
        except:
            downDistanceText = 'No down and distance available'

        #status type detail is time and quarter
        time_qtr = scoreboard_data['events'][evc]['status']['type']['detail']

        game_info = GameInfo(id, team1, team2, last_play, team1_score, team2_score, downDistanceText, time_qtr)
        storage[sb_key] = game_info

def info_printer(gio):
    info = f'{(gio.team1)} {gio.team1_score} - {(gio.team2)} {gio.team2_score} | {gio.last_play}'

    #check if info is in previous_payloads
    if info in previous_payloads:
        return info
    
    print(f'''
    {(gio.team1)} {gio.team1_score} - {(gio.team2)} {gio.team2_score}
    {gio.downDistanceText} , {gio.time_qtr}
    {gio.last_play}
    ''')

    previous_payloads.append(info)
    return info

update_interval = 90

#test data
# parse scoreboard.json
sbd = json.loads(open('scoreboard.json').read())

print('-----------------------------------')
while True:

    print(f'current time: {datetime.datetime.now()} - next update in {update_interval} seconds')

    #real data
    sbd = scoreboard_request()
    sb_parser(sbd)

    for key in storage:
        info_printer(storage[key])

    print('-----------------------------------')

    time.sleep(update_interval)