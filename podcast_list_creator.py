#!/usr/bin/env python

# This script uses ListenNotes to generate a list of podcasts.

import csv
import requests
import argparse
import os
import json

# Command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("podcast_dest",
                    help="Destination path for podcast list.")
parser.add_argument("genre_list_dest",
                    help="Destination path for genre ids and names")
parser.add_argument("-n", "--max_count", help="Max number of podcasts per genre.", type=int)
# parser.add_argument('-l','--list_id', nargs='+', help='List of podcast ids.', type=int)
args = parser.parse_args()

# Main


def main():
    # Env variable for ListenNotes API.
    key = os.environ.get('X_ListenAPI_Key')
    headers = {
        'X-ListenAPI-Key': key,
    }
    # Get all podcast genres.
    # if args.list_id:
        # IDList = args.list_id
    url_genres = 'https://listen-api.listennotes.com/api/v2/genres'
    response_genre = requests.request('GET', url_genres, headers=headers)
    json_data_genre = json.loads(response_genre.text)
    # Open files for writing.
    podcastDest = args.podcast_dest
    genreDest = args.genre_list_dest
    # Set of ids that were seen (to avoid duplication).
    IDSet = set()
    genreSet = set()
    countGenres = 0
    countPodcasts = 0
    with open(podcastDest, 'w') as podcastFile, open(genreDest, 'w') as genreFile:
        podcastWriter = csv.writer(podcastFile)
        genreWriter = csv.writer(genreFile)
        for genre in json_data_genre['genres']:
            genre_id = genre['id']
            genre_name = genre['name']
            if genre_id not in genreSet:
                genreSet.add(genre_id)
                countGenres += 1
                genreWriter.writerow([genre_id, genre_name])
            # if args.list_id:
                # print(IDLisat)
            else:
                # Get best podcasts for each genre.
                url_podcasts = f'https://listen-api.listennotes.com/api/v2/best_podcasts?genre_id={genre_id}&page=1&region=us&safe_mode=0'
                response_podcasts = requests.request(
                    'GET', url_podcasts, headers=headers)
                json_data_podcasts = json.loads(response_podcasts.text)
            countCast = 0
            for podcast in json_data_podcasts['podcasts']:
                if args.max_count and args.max_count > countCast:
                    countCast += 1
                    newPodcast = podcast
                    try:
                        del newPodcast['extra']
                        del newPodcast['looking_for']
                    except KeyError:
                        print("Key 'testing' not found")
                    if newPodcast['id'] not in IDSet:
                        IDSet.add(newPodcast['id'])
                        countPodcasts += 1
                        podcastWriter.writerow([value for key, value in podcast.items()])
    podcastFile.close()
    genreFile.close()
    if args.verbose:
        print(f"File {podcastDest} contains {countPodcasts} podcasts.")
        print(f"File {genreDest} contains {countGenres} unique podcast genres.")

if __name__ == "__main__":

    # calling main function
    main()
