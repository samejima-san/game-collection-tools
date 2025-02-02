#INSERT INTO video_games (game_name, platform, year_played, rating, completed)
#VALUES

import json
import math

with open('steam_library.json', 'r') as f:
    data = json.load(f)

output = (f'INSERT INTO video_games (vg_name, hours_played) \n '
          f'VALUES ')
for game in data:
    game_name = game['name'].replace("'", "''")
    hours_played = math.floor(game['playtime_forever'] / 60)
    output += f"('{game_name}', {hours_played}), \n"
output += ';'

with open('query.txt', 'w') as f:
    f.write(output)
