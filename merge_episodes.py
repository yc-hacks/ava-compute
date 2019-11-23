import glob
import os
import re

import pandas as pd

from chunk_transcripts import transcript_to_chunks


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def create_df(fileName, maxChunkSize):
    df = pd.read_csv(fileName, names=["UUID", "title", "summary", "published", "link", "transcription"])
    df['paragraphs'] = df['transcription'].apply(lambda x: transcript_to_chunks(x, maxChunkSize))

    # Test: drop columns
    # df = df.drop("UUID", axis=1)
    # df = df.drop("summary", axis=1)
    # df = df.drop("published", axis=1)
    # df = df.drop("link", axis=1)
    # df = df.drop("transcription", axis=1)

    expodedDF = []
    for i, row in df.iterrows():
        for paragraph in row['paragraphs']:
            clean_paragraph = cleanhtml(paragraph)
            expodedDF.append((row['title'], clean_paragraph, row['UUID'], cleanhtml(row['summary']), row['link']))
    
    return pd.DataFrame(expodedDF, columns = ['title', 'paragraphs', 'uuid', 'summary', 'link']) 



if __name__ == "__main__":
    os.chdir("./final-output/episodes")

    OUTPUT_FILE = "../merged_episodes.csv"
    MAX_CHUNK = 50

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([create_df(f, MAX_CHUNK) for f in all_filenames ])

    # export to csv
    combined_csv.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
