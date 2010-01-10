from __future__ import division
import os
from random import randint, choice

MAX_INCREASE = 32
INITIAL_SCORE = 1500

class Player:
    
    def __init__(self, id, score, skill, variation):
        self.id = id
        self.score = score
        self.skill = skill
        self.variation = variation
        self.wins = 0
        self.matches = 0
       
    def get_score(self):
        return self.skill + randint(-self.variation, self.variation)

    def __str__(self):

        if self.matches:
            win_perc = self.wins / self.matches * 100
        else:
            win_perc = 0
        return 'Player %3i %5i skill: %3i/%3i W:%3i %3.1f %%' % (self.id, self.score,
                self.skill, self.variation, self.wins, win_perc)

    def __eq__(self, other):
        return self.id == other.id

class Elo:

    def __init__(self, players):
        self.players = [Player(a, INITIAL_SCORE, randint(0, 99), randint(0, 99)) for a in xrange(players)]
#        self.players.append(Player(-1, INITIAL_SCORE, -500, 0))
        self.players.append(Player(-2, INITIAL_SCORE, -50, 0))
        self.players.append(Player(-3, INITIAL_SCORE, 0, 0))
#        self.players.append(Player(-10, INITIAL_SCORE, 1500, 0))
        self.players.append(Player(-11, INITIAL_SCORE, 500, 0))
        self.players.append(Player(-12, INITIAL_SCORE, 100, 0))
        self.output_match = True

    def random_match(self):
        p1 = choice(self.players)
        p2 = p1
        while p1 == p2:
            p2 = choice(self.players)
        self.match(p1, p2)

    def match(self, p1, p2):
        if self.output_match: print
        e1 = MAX_INCREASE * 1 / (1 + 10 ** ((p2.score - p1.score) / 400))
        e2 = MAX_INCREASE * 1 / (1 + 10 ** ((p1.score - p2.score) / 400))
        s1 = p1.get_score()
        s2 = p2.get_score()
        if self.output_match: print p1, e1
        if self.output_match: print ' vs'
        if self.output_match: print p2, e2
        p1.matches += 1
        p2.matches += 1
        if s1 > s2:
            p1.wins += 1
            p1.score += e2
            p2.score -= e2
            if self.output_match: print p1, 'won. Gained', e2
            if self.output_match: print p2, 'loss. Lost ', e2
        else:
            p2.wins += 1
            p1.score -= e1
            p2.score += e1
            if self.output_match: print p2, 'won. Gained', e1
            if self.output_match: print p1, 'loss. Lost ', e1

    
    def print_ranks(self):
        print
        s = sorted(self.players, key=lambda a: a.score)
        last = 0
        for player in s:
            print player, int(player.score - last)
            last = player.score


def main():
    e = Elo(30)
    fast = True
    e.output_match = not fast
    matches = 0
    while 1:
        matches += 1
        if matches % 100000 == 0:
            e.players.append(Player(99, INITIAL_SCORE, randint(0, 99),
                        randint(0, 99)))
        e.random_match()
        if fast and (matches % 100000):
            continue
        if fast:
            os.system('clear')
        e.print_ranks()
        if not fast:
            raw_input()

if __name__ == '__main__':
    main()

