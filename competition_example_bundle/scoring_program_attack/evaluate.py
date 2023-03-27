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


if not os.path.isdir(submission_dir):
    print("%s doesn't exist" % submission_dir)

if os.path.isdir(submission_dir) and os.path.isdir(orig_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'w')

    answer_files = sorted(glob.glob(os.path.join(orig_dir,"*.txt")))
    guess_files = sorted(glob.glob(os.path.join(submission_dir,"*.txt")))
 
    # OMIT: answer_file check

    score = [0] * len(answer_files)
    hit = [0] * len(answer_files)
    blow = [0] * len(answer_files)

    for i, (answer_file, guess_file) in enumerate(zip(answer_files, guess_files)):
        #print(i, guess_file, answer_file)
        with open(answer_file, "r") as f:
            answer = f.read()
        with open(guess_file, "r") as f:
            guess = f.read()

        hit[i], blow[i] = check_guess(answer, guess)
        score[i] = 1 - (hit[i] * 1 + blow[i] * 0.5) / 6 # Hit = 1pt, Blow = 0.5pt, All hits = 6pt
        print(guess, answer, score[i])

    output_filename = os.path.join(output_dir, 'scores.txt')
    with open(output_filename, mode="w") as f:
        f.writelines("attack_score:%.6f\n" % (1 - sum(score)/len(score)))
        for i in range(len(score)):
            f.writelines("privacy_score_%d:%.6f\n" % (i+1, score[i]))
            f.writelines("hit_%d:%d\n" % (i+1, hit[i]))
            f.writelines("blow_%d:%d\n" % (i+1, blow[i]))
