#!/usr/bin/env python
import sys
import os
import os.path
import glob

input_dir = sys.argv[1]
output_dir = sys.argv[2]

def check_guess(answer, guess):
    hit = 0
    blow = 0
    for i in range(len(answer)):
        if answer[i] == guess[i]:
            hit += 1
        elif guess[i] in answer:
            blow += 1
    return hit, blow

submission_dir = os.path.join(input_dir, 'res')
orig_dir = os.path.join(input_dir, 'ref')

num_of_team = 15

if not os.path.isdir(submission_dir):
    print("%s doesn't exist" % submission_dir)

if os.path.isdir(submission_dir) and os.path.isdir(orig_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # OMIT: answer_file check
    # - Score 1.0 for all non-existing data
    # - Calculate the score roughly (assume that one of the teams is the attacker)

    # We want to start the filenames from 001, so...
    score = [0] * (num_of_team + 1)
    hit = [0] * (num_of_team + 1)
    blow = [0] * (num_of_team + 1)

    for i in range(1, num_of_team + 1):
        filename = "%03d.txt" % i
        answer_file = os.path.join(orig_dir, "%03d.txt" % i)
        guess_file = os.path.join(submission_dir, "%03d.txt" % i)

        with open(answer_file, "r") as f:
            answer = f.read()

        if os.path.exists(guess_file):
            with open(guess_file, "r") as f:
                guess = f.read()

            hit[i], blow[i] = check_guess(answer, guess)
            score[i] = 1 - (hit[i] * 1 + blow[i] * 0.5) / 6 # Hit = 1pt, Blow = 0.5pt, All hits = 6pt
        else:
            guess = 00000
            hit[i] = blow[i] = 0
            score[i] = 1.0

        #print(i, guess, answer, score[i])            

    output_filename = os.path.join(output_dir, 'scores.txt')
    with open(output_filename, mode="w") as f:
        f.writelines("attack_score:%.6f\n" % (1 - (sum(score) - 1) / (num_of_team - 1))) # Exclude the own data
        for i in range(1, num_of_team + 1):
            f.writelines("privacy_score_%d:%.6f\n" % (i, score[i]))
            f.writelines("hit_%d:%d\n" % (i, hit[i]))
            f.writelines("blow_%d:%d\n" % (i, blow[i]))
