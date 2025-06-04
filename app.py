import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
from dotenv import load_dotenv
import time

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value 
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _insert(node, key, value):
            if not node:
                return Node(key, [value])
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value.append(value)
            return node
        self.root = _insert(self.root, key, value)

    def in_order(self):
        result = []
        def _in_order(node):
            if node:
                _in_order(node.left)
                result.append((node.key, node.value))
                _in_order(node.right)
        _in_order(self.root)
        return result[::-1]  


    def in_order_desc(self):
        result = []
        def _in_order_desc(node):
            if node:
                _in_order_desc(node.right)
                result.append((node.key, node.value))
                _in_order_desc(node.left)
        _in_order_desc(self.root)
        return result

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private playlist-read-collaborative"
))

def extrair_playlist_id(link_ou_id):
    if "playlist/" in link_ou_id:
        return link_ou_id.split("playlist/")[1].split("?")[0]
    return link_ou_id.strip()

def get_tracks_from_playlist(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend([item['track'] for item in results['items'] if item['track']])
        results = sp.next(results) if results['next'] else None
    return tracks

def analyze_playlist(playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
    except Exception as e:
        print(f"Não foi possível acessar a playlist: {e}")
        return

    print(f"\nAnalisando playlist: {playlist['name']}")
    tracks = get_tracks_from_playlist(playlist_id)
    print(f"\nTotal de músicas encontradas: {len(tracks)}")

    track_counter = Counter()
    genre_counter = Counter()
    track_info_map = dict()
    artist_genre_cache = dict()

    for track in tracks:
        if not track or not track.get('id'):
            continue
        track_key = (track['name'], ', '.join([a['name'] for a in track['artists']]))
        track_counter[track_key] += 1
        if track_key not in track_info_map:
            track_info_map[track_key] = {
                'Nome': track['name'],
                'Artistas': ', '.join([a['name'] for a in track['artists']]),
                'Popularidade': track.get('popularity', 0),
                'Duração (min)': round(track['duration_ms']/60000, 2)
            }

    print("Calculando gêneros (pode demorar um pouco)...")

    for (name, artists), _ in track_counter.most_common(50):
        artist_names = [a.strip() for a in artists.split(',')]
        for artist_name in artist_names:
            if artist_name not in artist_genre_cache:
                try:
                    result = sp.search(q='artist:' + artist_name, type='artist', limit=1)
                    if result['artists']['items']:
                        artist = result['artists']['items'][0]
                        artist_genre_cache[artist_name] = artist.get('genres', [])
                    else:
                        artist_genre_cache[artist_name] = []
                    time.sleep(0.05)
                except Exception as e:
                    print(f"Erro ao buscar gênero para artista {artist_name}: {e}")
                    artist_genre_cache[artist_name] = []
            for genre in artist_genre_cache[artist_name]:
                genre_counter[genre] += 1

    top_10 = track_counter.most_common(10)
    tracks_data = []
    bt_freq = BinaryTree()
    bt_pop = BinaryTree()

    for (name, artists), freq in top_10:
        item = track_info_map[(name, artists)].copy()
        item['Quantidade'] = freq
        tracks_data.append(item)
        bt_freq.insert(freq, f"{name} - {artists}")
        bt_pop.insert(item['Popularidade'], f"{name} - {artists}")

    bt_genres = BinaryTree()
    for genre, count in genre_counter.items():
        bt_genres.insert(count, genre)



    print("\n=== TOP 10 MÚSICAS (usando árvore de popularidade) ===")
    print(f"{'Música'.ljust(70)}{'Popularidade'.rjust(15)}")
    print("-" * 85)
    for pop, nomes in bt_pop.in_order_desc():
        for nome in nomes:
            print(f"{nome.ljust(70)}{str(pop).rjust(15)}")

    print("\n=== RANKING DE MÚSICAS POR FREQUÊNCIA (usando árvore binária) ===")
    print(f"{'Música'.ljust(70)}{'Repetições'.rjust(12)}")
    print("-" * 82)
    for freq, nomes in bt_freq.in_order_desc():
        for nome in nomes:
            print(f"{nome.ljust(70)}{str(freq).rjust(12)}")

    print("\n=== RANKING DE GÊNEROS (usando árvore binária) ===")
    print(f"{'Gênero'.ljust(25)}{'Quantidade'.rjust(10)}")
    print("-" * 35)
    cont = 0
    for count, genres in bt_genres.in_order_desc():
        for genre in genres:
            print(f"{genre.ljust(25)}{str(count).rjust(10)}")
            cont += 1
            if cont >= 10:
                break
        if cont >= 10:
            break


    top_popularities = []
    top_names = []
    for pop, nomes in bt_pop.in_order_desc():
        for nome in nomes:
            top_popularities.append(pop)
            top_names.append(nome)
            if len(top_popularities) >= 10:
                break
        if len(top_popularities) >= 10:
            break
    if top_popularities and top_names:
        plt.figure(figsize=(10, 5))
        ax = pd.DataFrame({'Nome': top_names, 'Popularidade': top_popularities}).sort_values('Popularidade', ascending=True).plot.barh(
            x='Nome', y='Popularidade', color='#1DB954', legend=False, ax=plt.gca()
        )
        plt.xlabel('Popularidade')
        plt.title('Top 10 músicas da playlist (por popularidade)', pad=20)
        ax.tick_params(axis='y', labelsize=12)
        plt.subplots_adjust(left=0.33, right=0.98, top=0.9, bottom=0.1)
        plt.show()

    top_genres = []
    top_counts = []
    cont = 0
    for count, genres in bt_genres.in_order_desc():
        for genre in genres:
            top_genres.append(genre)
            top_counts.append(count)
            cont += 1
            if cont >= 10:
                break
        if cont >= 10:
            break
    if top_genres and top_counts:
        pd.DataFrame({'Gênero': top_genres, 'Quantidade': top_counts}).set_index('Gênero').plot.pie(
            y='Quantidade', autopct='%1.1f%%',
            legend=False,
            colors=plt.cm.Paired.colors
        )
        plt.title('Top gêneros na playlist')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    print("=== ANALISADOR DE PLAYLIST SPOTIFY ===")
    playlist_input = input("Cole o link da playlist ou o ID da playlist: ").strip()
    playlist_id = extrair_playlist_id(playlist_input)
    analyze_playlist(playlist_id)