#!/usr/bin/env python

# This script takes audio files and transcribes them using AWS.
# You can find generated transcripts in their respective S3 buckets.

from __future__ import print_function
import time
import boto3
import argparse
import csv
import botocore
import wget
import json

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--podcast_src",
                    help="Home directory for podcasts to be transcribed, e.g. `the_daily`.")
parser.add_argument(
    "-n", "--num", help="How many podcasts in the home directory should be transcribed.", type=int)
parser.add_argument("-i", "--doc", help="Podcast Episode CSV File.")
args = parser.parse_args()

# Load podcast episode file.
episode_file = args.doc
# Podcast base directory e.g. "the_daily"
podSrc = args.podcast_src
# Path where podcasts are stored in S3.
basePath = f"s3://ava-compute-storage/{podSrc}"
# How many podcasts to transcribe.
podcastCount = args.num
# Resulting path.
resultingPath = f"podcasts/{podSrc}/transcripts/{podSrc}_episodes_transcribed.csv"

# Transcription Engine
transcribe = boto3.client('transcribe')
# S3 for file storage
S3 = boto3.client('s3')

SOURCE_FILENAME = resultingPath
BUCKET_NAME = 'ava-compute-storage'

# Open Podcast File.
with open(episode_file, "rt") as episodeFile, open(resultingPath, "w") as resultFile:
    episodeReader = csv.reader(episodeFile)
    resultWriter = csv.writer(resultFile)
    episodes = list(episodeReader)
    countEpisodes = 0
    for i, e in enumerate(episodes):
        if i >= podcastCount:
            break
        jobName = f"{podSrc}_episode_{i}"
        episode_id = e[0]
        countEpisodes += 1
        print(f"Transcribing {args.podcast_src} Episode {i} of {podcastCount}")
        jobName = f"{podSrc}_episode_{i}"
        jobUri = f"{basePath}/{episode_id}_episode_{i}.mp3"
        print(jobName)
        print(jobUri)
        # Save Translated Json

        transcribe.start_transcription_job(
            TranscriptionJobName=jobName,
            Media={'MediaFileUri': jobUri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=jobName)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                print(status)
                break
            print(f"Job {jobName} Not ready yet...")
            time.sleep(5)
        path_to_output = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        wget.download(path_to_output, f"{podSrc}/transcripts/{episode_id}_episode_{i}.json")
        with open(f"podcasts/{podSrc}/transcripts/{episode_id}_episode_{i}.json", "rt") as transcriptFile:
            d = json.load(transcriptFile)
        translated = d['results']['transcripts'][0]['transcript']
        transcriptFile.close()
        print(translated)
        e.append(translated)
        resultWriter.writerow(e)


S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)
episodeFile.close()
resultFile.close()
