import glob
import os
import re

import pandas as pd


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def create_df(fileName):
    return pd.read_csv(fileName, names=["uuid", "title", "author", "description", "category", "image"])

if __name__ == "__main__":
    os.chdir("./final-output/podcasts")

    OUTPUT_FILE = "../merged_podcasts.csv"

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([create_df(f) for f in all_filenames ])

    # export to csv
    combined_csv.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
