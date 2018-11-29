# Scoreboard Modeled As A List
scoreboard = [
    0,   # ball        - 0
    0,   # out         - 1
    0,   # strike      - 2
    0,   # inning      - 3
    0,   # home score  - 4
    0    # guest score - 5
]

while scoreboard[0] <= 9:
    
    # game stuff happens here
    # pitches, runs, etc
    
    if scoreboard[2] == 3:
        scoreboard[1] += 1
        
    if scoreboard[1] == 3:
        scoreboard[0] += 1
        scoreboard[1] = 0
        scoreboard[2] = 0