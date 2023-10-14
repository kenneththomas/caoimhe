import requests
import json

storage = {}
previous_payloads = []

def scoreboard_request():
    # Define the API URL
    url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?limit=5"

    # Send an HTTP GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()
        
        #scoreboarddata = json.dumps(data, indent=4)

    else:
        # Print an error message if the request was not successful
        print("Error: Unable to fetch data from the ESPN API")

    return data

#information object that will be stored in storage
class GameInfo:
    def __init__(self, id, team1, team2, last_play, team1_score, team2_score):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.last_play = last_play
        self.team1_score = team1_score
        self.team2_score = team2_score

def sb_parser(scoreboard_data):

    #how many events in scoreboard data
    eventcount = len(scoreboard_data['events'])

    #loop through each event
    for evc in range(eventcount):

        #if the event is not live, skip it
        if scoreboard_data['events'][evc]['status']['type']['completed'] == True:
            continue

        id = scoreboard_data['events'][evc]['id']
        team1 = scoreboard_data['events'][evc]['competitions'][0]['competitors'][0]['team']['location']
        team2 = scoreboard_data['events'][evc]['competitions'][0]['competitors'][1]['team']['location']

        #make team names alphanumeric

        print(f'{team1} vs {team2}')
        sb_key = f'{id}_{team1}_{team2}'
        print(sb_key)

        #last play
        last_play = scoreboard_data['events'][evc]['competitions'][0]['situation']['lastPlay']['text']
        print(last_play)

        #get score
        team1_score = scoreboard_data['events'][evc]['competitions'][0]['competitors'][0]['score']
        team2_score = scoreboard_data['events'][evc]['competitions'][0]['competitors'][1]['score']
        print(f'{team1} {team1_score} - {team2} {team2_score}')

        #create GameInfo object
        game_info = GameInfo(id, team1, team2, last_play, team1_score, team2_score)



#real data
#sbd = scoreboard_request()

#test data
# parse scoreboard.json
sbd = json.loads(open('scoreboard.json').read())

sb_parser(sbd)