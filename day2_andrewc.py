import os
# os.chdir('/home/jovyan/ds-risk-team-adventofcode/')

# import numpy as np
import pandas as pd

# Day 2 data
data_path = 'andrewc_2022/data/day2_input.txt'

# Read data
df = pd.read_csv(data_path, sep=' ')

# Re-order columns
df = df[['strategy', 'opponent']]


################################################################
# Define some dictionaries for mapping values used in the games
################################################################

# Coding: Opponent/Me (R=Rock, P=Paper, S=Scissors)
opponent = dict(A='R', B='P', C='S')
me = dict(X='R', Y='P', Z='S')

# Part 2: How I need to end the game
me_end = dict(X='lose', Y='draw', Z='win')

# Part 2: Return shape based on whether we need to win/lose
win = dict(R='P', S='R', P='S')
lose = {v:k for k, v in win.items()}

# What game can result in (me->opponent)
game_result = dict(RR='draw', PP='draw', SS='draw'
                    , RP='lose', PS='lose', SR='lose'
                    , RS='win', PR='win', SP='win')

# Win/lose/draw scores
scores_num = dict(win=6, lose=0, draw=3)

# What you score simply for making a choice
selection_score = dict(P=2, R=1, S=3)


# What should I play?
def work_out_play(opponent, strategy):

    """Part 2 strategy: Return shape based on how the game should end"""
    
    if strategy == 'draw':
        return opponent
    elif strategy == 'win':
        return win[opponent]
    else:
        return lose[opponent]

if __name__ == "__main__":

    # Score
    # RR, PP, SS = Draw (3)
    # RP, PS, SR = Loss (0)
    # RS, PR, SP = Win (6)


    # Unencrypt the strategy
    df['strategy_u'] = df['strategy'].map(me)
    df['opponent_u'] = df['opponent'].map(opponent)

    # Work out the whole game (me -> opponent)
    df['game'] =  df['strategy_u'] + df['opponent_u']
    
    # Get Scores
    df['game_scores_'] = df['game'].map(game_result)
    df['game_scores'] = df['game_scores_'].map(scores_num)

    # Extra points for selecting
    df['select_score'] = df['strategy_u'].map(selection_score)

    # Final score for round
    df['score'] = df['game_scores'] + df['select_score']

    ########################################
    # Part 1: Total score
    ########################################

    # Total score following part 1 guide
    print(f"Part 1: {df.score.sum():,}")

    ########################################
    # Part 2: Chose shape for game
    ########################################

    # What is the planned end result?
    df['end_result'] = df['strategy'].map(me_end)

    # Work out how game goes now
    df['strategy_u2'] = df.apply(lambda row: work_out_play(row.opponent_u, row.end_result), axis=1)

    # Part 2 version of game
    df['game2'] = df['strategy_u2'] + df['opponent_u']

    # part 2 scores

    # Win/lose/draw
    df['game_scores2_'] = df['game2'].map(game_result)

    # Change win, etc. to numeric
    df['game_scores2'] = df['game_scores2_'].map(scores_num)

    # Get score for selecting
    df['select_score2'] = df['strategy_u2'].map(selection_score)

    # Final score for round
    df['score2'] = df['game_scores2'] + df['select_score2']

    # Score using part 2 strategy
    print(f"Part 2: {df.score2.sum():,}")
