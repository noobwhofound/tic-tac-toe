# tik-tac-toe
tic tac toe game with 4 different levels of ai and 3 gamemodes

# ----------------------------

# how-to-use
it's easy.
with 3 lines of code you can run the game
```py
if __name__ == "__main__":
  game = Game(gamemode = 'pvsai', ai_difficulty = 'expert', ai_number = 2)
  while True:
    game.play()
```

# ai-levels
easy, medium, hard, expert
There's also 'random' you can use

# gamemodes
pvsp (player versus player)
pvsai (player versus ai)
aivsai (ai versus ai)

in aivsai you have to define a daley time between every ai move (in seconds)
```py
if __name__ == "__main__":
    game = Game('aivsai', 'medium', 1, 2)
    while True :
        game.play()
```
leave the delay arg empty to get delay of 0.5 seconds

# what-is-number
it's nothing special.
i'd recommend you using the number 2 for the ai but afterall it doesn't matter which number you define for the ai




