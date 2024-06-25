from src.Blum import BlumBot
from time import sleep
from random import randint
import os

def clear():
    if os.name != "nt":
        os.system('clear')
    else:
        os.system('cls')

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
        
        timeToWait = randint(60*10, 60*15) 
        print(f"Waiting {timeToWait} seconds")
        sleep(timeToWait)
        
        bot.getNewTokens()
        sleep(2)
        clear()

    except:
        sleep(60)
        continue