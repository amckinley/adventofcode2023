import math

class RaceRun(object):
    def __init__(self, race_time, button_time, record_distance):
        self.r_time = race_time
        self.b_time = button_time
        self.r_distance = record_distance
        
        rem_time = self.r_time - self.b_time
        speed = self.b_time
        self.distance = rem_time * speed
    
    def is_winner(self):
        return self.distance > self.r_distance

if __name__ == "__main__":
    file1 = open('input_day6_final.txt', 'r')
    lines = file1.readlines()

    winner_margin = []
    for l in lines:
        race_time, record_distance = l.split(" ")
        race_time = int(race_time)
        record_distance = int(record_distance)
        winner_count = 0
        for i in range(1, race_time):
            rr = RaceRun(race_time, i, record_distance)
            # print("{} {} {} {}".format(race_time, i, record_distance, rr.is_winner()))
            if rr.is_winner():
                winner_count += 1
                # print(winner_margin)

        print(winner_count)
    
    