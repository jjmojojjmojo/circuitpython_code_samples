# Scoreboard Modeled As A Dictionary
scoreboard = {
    "ball": 0,
    "out": 0,
    "strike": 0,
    "inning": 0,
    "home_score": 0,
    "guest_score": 0
}

while scoreboard["inning"] <= 9:
    
    # game stuff happens here
    # pitches, runs, etc
    
    if scoreboard["strike"] == 3:
        scoreboard["out"] += 1
        
    if scoreboard["out"] == 3:
        scoreboard["inning"] += 1
        scoreboard["out"] = 0
        scoreboard["strike"] = 0