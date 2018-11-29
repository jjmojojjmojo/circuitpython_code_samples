# Scoreboard Modeled As Simple Variables
ball = 0
out = 0
strike = 0
inning = 0
home_score = 0
guest_score = 0

while inning <= 9:
    
    # game stuff happens here
    # pitches, runs, etc
    
    if strike == 3:
        out += 1
        
    if out == 3:
        inning += 1
        out = 0
        strike = 0