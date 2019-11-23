#!/usr/bin/env python

# This takes a podcast feed and parses it into a file.

# PODCAST
# UUID -> Number
# Title -> String
# Author -> String
# Description -> String
# Category -> String
# Image -> String

# EPISODE
# Title -> String
# Summary -> String
# Published Date -> Date
# Link -> String
# Audio Link -> String

import csv
import requests
import argparse
import feedparser
import uuid
import string

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-u", "--url", help="URL to Podcast RSS Feed. ")
parser.add_argument("-s", "--podcast_src", help="Podcast list generated with podcast_list_creator.py")
args = parser.parse_args()

# Transforms title into a filename.
def namify(title):
    return title.lower().replace(" ", "_")

# Take parsed podcast and return dict with uuid, title, author, description,
# category, and image.
def getPodcastAttributes(podcast, custom_uuid=None):
    # Get feed info.
    feed = podcast['feed']
    # Generate uuid
    if custom_uuid == None:
        id = uuid.uuid4()
    else:
        id = custom_uuid
    # Get podcast attributes.
    podcastAttributes = {}
    podcastAttributes['uuid'] = id
    podcastAttributes['title'] = feed['title']
    podcastAttributes['author'] = feed['author']
    podcastAttributes['description'] = feed['description']
    podcastAttributes['category'] = feed['category']
    podcastAttributes['image'] = feed['image']

    if args.verbose:
        for key, value in podcastAttributes.items():
            print(value)

    return podcastAttributes

# Get podcast episodes for the parsed podcast.
def getPodcastEpisodes(uuid, podcast):
    # Resulting list of podcast episodes.
    podcastEpisodes = []
    # Get episodes.
    entries = podcast['entries']
    # Parse episode by episode.
    for entry in entries:
        try:
            episode = {}
            episode['uuid'] = uuid
            episode['title'] = entry['title']
            episode['summary'] = entry['summary']
            episode['published'] = entry['published']
            episode_links = entry['links']
            # links = []
            for link in episode_links:
                link_href = link['href']
                if link_href.find("mp3") != -1:
                    # print("Found MP3")
                    episode['links'] = link_href
                # links.append(link_href)
            # episode['links'] = links
            podcastEpisodes.append(episode)
            if args.verbose:
                for key, value in episode.items():
                    print(value)
        except Exception:
            pass

    return podcastEpisodes

# Main
def main():
    print("Starting Podcast Feed Parser...")
    if args.url:
        # Generate one podcast.
        url = args.url
        print(f"Checking Podcast URL: {url}")
        # Get Podcasts
        podcast = feedparser.parse(url)
        podcastAttributes = getPodcastAttributes(podcast)
        podcastEpisodes = getPodcastEpisodes(podcastAttributes['uuid'], podcast)
        # Get Name
        name = podcastAttributes['title']
        podcastFilename = f'{namify(name)}_podcastMetdata.csv'
        episodesFilename = f'{namify(name)}_episodes.csv'
        with open(podcastFilename, 'w') as podcastFile, open(episodesFilename, 'w') as episodesFile:
            podcastWriter = csv.writer(podcastFile)
            episodeWriter = csv.writer(episodesFile)
            podcastWriter.writerow([value for key, value in podcastAttributes.items()])
            countEpisodes = 0
            for episode in podcastEpisodes:
                countEpisodes += 1
                episodeWriter.writerow([value for key, value in episode.items()])
            print(f"Saved info about {countEpisodes} podcast episodes.")
        podcastFile.close()
        episodesFile.close()
    elif args.podcast_src:
        print(f"Checking Podcast File {args.podcast_src}")
        episodesFilename = 'episodeList.csv'
        countPodcasts = 0
        countEpisodes = 0
        with open(args.podcast_src, 'rt') as podcastList, open(episodesFilename, 'w') as episodesFile:
            podcastListReader = csv.reader(podcastList)
            episodeWriter = csv.writer(episodesFile)
            podcasts = list(podcastListReader)
            for podcast in podcasts:
                print(f"Now parsing podcast: {podcast[1]}")
                url = podcast[10]
                id = podcast[0]
                # print(id)
                # print(url)
                try:
                    podcast = feedparser.parse(url)
                    countPodcasts += 1
                    podcastEpisodes = getPodcastEpisodes(id, podcast)
                    for episode in podcastEpisodes:
                        countEpisodes += 1
                        episodeWriter.writerow([value for key, value in episode.items()])
                except Exception:
                    print(f"Passed podcast: {podcast[1]}")
                    pass
        print(f"Saved info about {countPodcasts} podcasts.")
        print(f"Saved info about {countEpisodes} podcast episodes.")
        episodesFile.close()
        podcastList.close()
    else:
        print("ERROR: No URL or PODCAST_SRC specified.")


if __name__ == "__main__":

    # calling main function
    main()
