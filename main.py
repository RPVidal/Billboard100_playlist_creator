from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


SPOTIFY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIFY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SCOPE = ["playlist-modify-private", "playlist-modify-public"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
PLAYLIST_URL_CREATE = f"https://api.spotify.com/v1/users/{SPOTIFY_CLIENT_ID}/playlists"
BASE_URL = "https://www.billboard.com/charts/hot-100/"


def create_billboard(billboard_date: str) -> list:
	"""This function takes a str date in a YY-MM-DD format and returns the billboard hot 100 for that week as a list."""

	global BASE_URL
	dated_url = BASE_URL + billboard_date + "/"
	response = requests.get(dated_url)
	soup = BeautifulSoup(response.text, "html.parser")
	h3_tags = soup.find_all(
		class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
	span_tags = soup.find_all(
		class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
	first_song = soup.find_all(
		class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
	first_song = first_song[0].get_text(strip="True")
	first_author = soup.find_all(
		class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet")
	first_author = first_author[0].get_text(strip="True")
	music_titles = [item.get_text(strip=True) for item in h3_tags]
	authors = [item.get_text(strip=True) for item in span_tags]

	billboard = []
	for num in range(0, len(music_titles)):
		if num == 0:
			billboard.append({"music": first_song, "artist": first_author})
			billboard.append({"music": music_titles[num], "artist": authors[num]})
		else:
			billboard.append({"music": music_titles[num], "artist": authors[num]})

	# print(first_author, first_song)
	# print(billboard, len(billboard))
	return billboard


def spotify_client():
	"""Setups the client with appropriate user and client authentication, al"""
	auth_manager = SpotifyOAuth(
		scope="playlist-modify-private",
		redirect_uri=REDIRECT_URI,
		client_id=SPOTIFY_CLIENT_ID,
		client_secret=SPOTIFY_CLIENT_SECRET,
		cache_path=os.environ["cache_path"],
		show_dialog=True
								)
	sp = spotipy.Spotify(auth_manager=auth_manager)
	return sp


def create_playlist(name: str) -> list:
	return spotify.user_playlist_create(user=spotify.current_user()["id"], name=name, public=False, collaborative=False, description="Test playlist")


def get_song_uri(playlist: list):
	"""GETS ALL URI FOR THE MUSICS IN THE BILLBOARD VARIABLE"""
	music_data = []
	for item in range(0, len(bill_board)):
		data = spotify.search(q=f"{playlist[item]['music']}", type=["track"], limit=1)
		if len(data["tracks"]["items"]) == 1:
			music_data.append(data["tracks"]["items"][0]["uri"])

		if len(data["tracks"]["items"]) != 1:
			print(f"The music {playlist[item]['music']} from {playlist[item]['artist']} could not be found")
	return music_data


def add_to_playlist(uris: list, music_list):
	global spotify
	spotify.playlist_add_items(playlist_id=music_list["id"], items=uris)


date = str(input("Input a date with the following format: YY-MM-DD: \n"))
playlist_name = str(input("How do you want to call the playlist? \n"))
bill_board = create_billboard(date)
spotify = spotify_client()
song_uri = get_song_uri(bill_board)
playlist = create_playlist(playlist_name)
songs_uris = get_song_uri(bill_board)
add_to_playlist(songs_uris, playlist)





