#!/usr/bin/env python

# Download podcast episodes from URLs and save them to files.

import requests
import re
import pycurl
import argparse
import csv

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-n", "--number_episodes", help="Number of episodes to download.")
# parser.add_argument("-s", "--start_index", help="Start downloading podcasts from the index.")
parser.add_argument("-i", "--input", help="File that contains podcast episode URLs.", required=True)
args = parser.parse_args()


# Main
def main():
    # Get URL from filepath that contains .mp3
    inputPath = args.input
    with open(inputPath, "rt") as episodeList:
        episodeReader = csv.reader(episodeList)
        podcasts = list(episodeReader)
        for podcast in podcasts:
            print(podcast[0])
        # Download it into an S3 bucket.
        # Count number of podcasts downloaded. Try/catch.

if __name__ == "__main__":

    # calling main function
    main()
