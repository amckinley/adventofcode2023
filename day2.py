# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# result = { 'id': 1, 'trials': [{'b': 3}, {}, {}]
def find_max(game):
    max_r = max_g = max_b = -1
    for t in game['trials']:
        max_r = max(max_r, t['r'])
        max_g = max(max_g, t['g'])
        max_b = max(max_b, t['b'])
    return max_r, max_g, max_b

def parse_game(line):
    game_s, trial_s = line.split(": ")
    game_id = int(game_s[5:])
    
    trials_res = []
    all_trials = trial_s.split(";")
    for trial_s in all_trials:
        # print('trial_s "{}"'.format(trial_s))
        trial_s = trial_s.strip()
        t = {'r': 0, 'g': 0, 'b': 0}

        color_count_s = trial_s.split(",")
        for count_s in color_count_s:
            count_s = count_s.strip()
            cnt_s, color_s = count_s.split(" ")
            # print('[{}] [{}]'.format(cnt_s, color_s))
            cnt = int(cnt_s)
            color = color_s[0]
            t[color] = cnt
        trials_res.append(t)
    
    return {'id': game_id, 'trials': trials_res}


def parse_games(lines):
    games = []
    for l in lines:
        games.append(parse_game(l))
    return games

            
def solve(games, red, green, blue):
    results = []
    for g in games:
        possible = True
        for t in g['trials']:
            if t['r'] > red or t['g'] > green or t['b'] > blue:
                print("found impossible game: {}".format(g))
                possible = False

        results.append({'id': g['id'], 'possible': possible})
    return results 

if __name__ == "__main__":
    file1 = open('input_day2.txt', 'r')
    lines = file1.readlines()
    games = parse_games(lines)

    acc = 0
    for g in games:
        r, g, b = find_max(g)
        acc += r * g * b
    print(acc)
    # results = solve(games, 12, 13, 14)
    
    # acc = 0
    # for r in results:
    #     if r['possible']:
    #         acc += r['id']
    # print(acc)

    # g_s = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    # print(parse_game(g_s))