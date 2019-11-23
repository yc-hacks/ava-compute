#!/usr/bin/env python

# This script takes audio files and transcribes them using AWS.
# You can find generated transcripts in their respective S3 buckets.

from __future__ import print_function
import time
import boto3
import argparse

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-u", "--url", help="URL to Podcast RSS Feed. ")
parser.add_argument("-s", "--podcast_src", help="Home directory for podcasts to be transcribed.")
parser.add_argument("-n", "--num", help="How many podcasts in the home directory should be transcribed.")
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

# Transcription Engine
transcribe = boto3.client('transcribe')
# S3 for file storage
S3 = boto3.client('s3')

# Open Podcast File.
with open(episode_file, "rt") as episodeFile:
    episodeReader = csv.reader(episodeFile)
    episodes = list(episodeReader)
    countEpisodes = 0
    for e in episodes:
        print(e)
#         jobName = f"{podSrc}_episode_{i}"
#         countEpisodes += 1
# for i in range(0, podcastCount):
#     print(f"Transcribing {args.podcast_src} Episode {i} of {podcastCount}")
#     jobName = f"{podSrc}_episode_{i}"
#     job_uri = f"{basePath}/"
#
#     transcribe.start_transcription_job(
#         TranscriptionJobName=job_name,
#         Media={'MediaFileUri': job_uri},
#         MediaFormat='mp3',
#         LanguageCode='en-US'
#     )
#     while True:
#         status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
#         if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
#             print(status)
#             with open('data.txt', 'w') as outfile:
#                 json.dump(data, outfile)
#             S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)
#             break
#         print(f"Job {jobName} Not ready yet...")
#         time.sleep(5)
#     print(status)
