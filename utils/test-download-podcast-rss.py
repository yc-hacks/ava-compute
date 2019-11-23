#!/usr/bin/env python

# This tests the ListenNotes API.
# Theodor Marcu

import requests
import os

key = os.environ.get('X_ListenAPI_Key')

url = 'https://listen-api.listennotes.com/api/v2/search?q=News&sort_by_date=0&type=episode&offset=0&len_min=10&len_max=30&genre_ids=68%2C82&published_before=1390190241000&published_after=0&only_in=title%2Cdescription&language=English&safe_mode=1'
headers = {
  'X-ListenAPI-Key': key,
}
response = requests.request('GET', url, headers=headers)
print(response.json())
