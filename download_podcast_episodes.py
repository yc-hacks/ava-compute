#!/usr/bin/env python

# Download podcast episodes from URLs and save them to files.

import wget
import argparse
import csv
import urllib.parse

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-n", "--number_episodes", help="Number of episodes to download.", type=int)
# parser.add_argument("-s", "--start_index", help="Start downloading podcasts from the index.")
parser.add_argument("-i", "--input", help="File that contains podcast episode URLs.", required=True)
parser.add_argument("-d", "--destination", help="Where should this podcast go.Files will be called `destination`/id_episode_ix.mp3. Can be empty.")
args = parser.parse_args()

# Transforms title into a filename.
def namify(title):
    return title.lower().replace(" ", "_")

# Main
def main():
    # Get URL from filepath that contains .mp3
    inputPath = args.input
    with open(inputPath, "rt") as episodeList:
        episodeReader = csv.reader(episodeList)
        podcasts = list(episodeReader)
        countDownloads = 0
        for podcast in podcasts:
            if args.number_episodes:
                if countDownloads >= args.number_episodes:
                    break

            episode_name = podcast[1]
            print(f"Downloading episode {episode_name}.")
            episode_url = podcast[4]
            print(episode_url)
            podcast_id = podcast[0]
            pathToDownload = f"{args.destination}/{podcast_id}_episode_{countDownloads}.mp3"
            print(pathToDownload)
            countDownloads += 1
            # Download it into an S3 bucket.
            # Count number of podcasts downloaded. Try/catch.
            wget.download(episode_url, pathToDownload)
        episodeList.close()
        print(f"Downloaded {countDownloads} episodes.")
if __name__ == "__main__":

    # calling main function
    main()
