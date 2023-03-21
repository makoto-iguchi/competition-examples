#!/usr/bin/env python
import sys
import os
import os.path
import pandas as pd
import numpy as np
import umark

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submission_dir = os.path.join(input_dir, 'res')
orig_dir = os.path.join(input_dir, 'ref')

if not os.path.isdir(submission_dir):
    print("%s doesn't exist" % submission_dir)

if os.path.isdir(submission_dir) and os.path.isdir(orig_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'w')

    data_id_file = os.path.join(submission_dir, "data_id.txt")
    data_id = open(data_id_file).read()

    orig_file = os.path.join(orig_dir, str(data_id)+".csv")
    submission_file = os.path.join(submission_dir, "anonymized.csv")


    orig_df = pd.read_csv(orig_file, header=None)
    submission_df = pd.read_csv(submission_file, header=None)
    
    df = umark.umark(orig_df, submission_df)
    cnt, rate, coef, OR, pvalue, cor = df.loc["max"]

    #output_file.write("score:%.6f\n" % (1 - (rate + cor + OR + pvalue) / 4 ))
    output_file.write("utility_score:%.6f\n" % (1 - (rate + cor + OR + pvalue) / 4 ))
    output_file.write("rate:%.6f\n" % (1 - rate))
    output_file.write("cor:%.6f\n" % (1 - cor))
    output_file.write("OR:%.6f\n" % (1 - OR))
    output_file.write("pvalue:%.6f\n" % (1 - pvalue))
    output_file.close()
    