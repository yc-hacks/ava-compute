#!/usr/bin/env python

# This script takes audio files and transcribes them using AWS.
from __future__ import print_function
import time
import boto3
transcribe = boto3.client('transcribe')
job_name = "test-job"
job_uri = "s3://ava-compute-storage/the_daily/e847d671-7d68-42ea-91ab-c2515a9f0a66_episode_0.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)
