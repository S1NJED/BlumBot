import requests
import json
import os
from time import sleep
from random import randint

def clear():
    if os.name != "nt":
        os.system('clear')
    else:
        os.system('cls')

DIR_PATH = os.getcwd()
CONFIG_PATH = os.path.join(DIR_PATH, "config.json")

class BlumBot:
    
    def __init__(self):
        with open(os.path.join(os.getcwd(), "config.json"), 'r') as file:
            config = json.load(file)
        
        self.token = config['token']
        self.refresh_token = config['refresh']
        
        self.session = requests.Session()
        self.UA = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        self.session.headers = {
            "User-Agent": self.UA,
            "Authorization": f"Bearer {self.token}"
        }
        
        # Check if token is invalid
        self.getNewTokens()
                    
    # {"availableBalance":"2425.2","playPasses":2,"timestamp":1718671399363,"farming":{"startTime":1718666849114,"endTime":1718695649114,"earningsRate":"0.002","balance":"9.1"}}
    def getBalance(self):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        req = self.session.get(url)
        data = req.json()
        print(data)

    def getGame(self):
        url = "https://game-domain.blum.codes/api/v1/game/play"
        req = self.session.post(url)
        data = req.json() # gameId
        # success {'gameId': xxx}
        # failed {'message': 'cannot start game'}
        
        
        if data.get('gameId'):
            print(f"\n[GET GAME] Game available ID: {data.get('gameId')}\n\n")
            return data
        
        print("\n[GET GAME]Can't start game, no more tickets ...\n\n")
        return False
    
    def startFarming(self):
        url = "https://game-domain.blum.codes/api/v1/farming/start"
        req = self.session.post(url)
        data = req.json() # endTime
        print(f"\n[START FARMING] => {data}\n")
        # success {"startTime":1718749982381,"endTime":1718778782381,"earningsRate":"0.002","balance":"0"}
    
    def claimFarming(self):
        url = "https://game-domain.blum.codes/api/v1/farming/claim"
        req = self.session.post(url)
        data = req.json()
        print(f"\n[CLAIM FARMING] => {data}\n")
        # success : {"availableBalance":"3848.85","playPasses":0,"timestamp":1718749964061}
        
    # 280 points maximum
    def claimGame(self, gameId: str):
        url = "https://game-domain.blum.codes/api/v1/game/claim"
        body = {
            "gameId": gameId,
            "points": 280 # maximum
        }
        
        req = self.session.post(url, data=body)
        data = "abc"
        try:
            data = req.json()
        except:
            data = req.text
            
        print(f"\n[CLAIM GAME] Claiming maximum points (280) from game (ID: {gameId})\n")
        return data

    def claimFriends(self):
        url = "https://gateway.blum.codes/v1/friends/claim"
        req = self.session.post(url)
        data = req.json()
        # success: {'claimBalance': x}
        # failed: {'code': 9, 'message': "It's too early to claim", 'details': []}
        
        
        if data.get('claimBalance'):
            print(f"\nSucessfully claimed {data['claimBalance']} coins from friends !\n")
        else:
            print(f"\nFailed to claimed from friends, ({data})\n")
        

    # 
    def claimTask(self, id: str):
        url = f"https://game-domain.blum.codes/api/v1/tasks/{id}/claim"
        req = self.session.post(url)
        data = req.json()
        print(data)

    def getFriends(self):
        url = "https://gateway.blum.codes/v1/friends?pageSize=1000"
        req = self.session.get(url)
        data = req.json()
        
        if data.get('friends') == []:
            print("No friends for the moment.")
            return False

        return data
    
    # TODO
    def claimDaily(self):
        url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-120"
        req = self.session.post(url)
        data = req.json()
        print(f"\n[CLAIM DAILY] => {data}\n")
        
    
    def getNewTokens(self):
        url = "https://gateway.blum.codes/v1/auth/refresh"

        body = {
            "refresh": self.refresh_token or self.token
        }
        headers = {
            "user-agent": self.UA,
            "content-type": "application/json"
        }

        req = self.session.post(url, headers=headers, data=json.dumps(body))
        data = req.json()

        with open(CONFIG_PATH, 'r') as file:
            config = json.load(file)
            config['token'] = data['access']
            config['refresh'] = data['refresh']
            
        with open(CONFIG_PATH, "w") as file:
            json.dump(config, file, indent=4)        

        self.token = data['access']
        self.refresh_token = data['refresh']
        
        self.session.headers['Authorization'] = f"Bearer {self.token}"
        print(f"\nNew token: {self.token}\n")


if __name__ == '__main__':
    bot = BlumBot()

    
    while True:
        try:
            bot.claimDaily()
            sleep(2)
            bot.claimFarming()
            sleep(2)
            bot.startFarming()
            sleep(2)
            bot.claimFriends()
            sleep(2)

            game = bot.getGame()
            if game:
                sleep(40)
                bot.claimGame(gameId=game['gameId'])    
            
            sleep(randint(60*10, 60*15))
            
            bot.getNewTokens()
            sleep(2)
            clear()

        except:
            sleep(60)
            continue
        