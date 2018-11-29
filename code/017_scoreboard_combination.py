# Scoreboard Modeled With Multiple Variable Types
scoreboard = {
    "markers": [
        0,  # ball   - 0
        0,  # out    - 1
        0   # strike - 2
    ],
    "inning": 0,
    "scores": {
        "home": 0,
        "guest": 0
    }
}

while scoreboard["inning"] <= 9:
    
    # game stuff happens here
    # pitches, runs, etc
    
    if scoreboard["markers"][2] == 3:
        scoreboard["markers"][1] += 1
        
    if scoreboard["markers"][1] == 3:
        scoreboard["inning"] += 1
        scoreboard["markers"][1] = 0
        scoreboard["markers"][2] = 0