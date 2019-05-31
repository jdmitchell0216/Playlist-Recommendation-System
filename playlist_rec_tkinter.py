import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from scipy.sparse import csr_matrix
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import subprocess
import webbrowser
import sys

import matplotlib
matplotlib.use('TkAgg')

import math
from matplotlib import pyplot as plt

# Define the functions before calling them
def doNothing():
    print("nothing")

def create_window():
    window = tk.Tk() 

df = pd.read_json('pre_pivot.json')

def search_by_artist_and_track(df, artist, track):
    print(df[df.artist_and_track.str.contains(artist, regex=False, case=False) & df.artist_and_track.str.contains(track, regex=False, case=False)].artist_and_track.iloc[0])
    return df[df.artist_and_track.str.contains(artist, regex=False, case=False) & df.artist_and_track.str.contains(track, regex=False, case=False)]

def make_playlist(user_id, playlist_id, df, list_of_searches):
    new_df = pd.DataFrame()
    for artist,track in list_of_searches:
        curr = search_by_artist_and_track(df, artist, track).iloc[0]
        new_df = new_df.append(pd.DataFrame([[user_id, curr.album_id,curr.album_name,curr.artist_ids,
                   curr.artist_names,'NA',playlist_id,curr.track_id,
                   curr.track_name,user_id,1,curr.artists_join,curr.artist_and_track]], columns=df.columns))
    return new_df

def create_sim_dict(playlist_id, df):
    sparse_matrix, playlist_id_c = create_sparse(df)
    similarities_playlists = cosine_similarity(sparse_matrix)
    playlists = np.array(playlist_id_c.categories)
    playlists_indices = list(playlists)
    sim_zip = zip(playlists_indices, similarities_playlists[playlists_indices.index(playlist_id)])
    sim_dict = {p:sim for p,sim in sim_zip}
    return sim_dict

def create_sparse(df):
    playlist_id_c = CategoricalDtype(sorted(df.playlist_id.unique()), ordered=True)
    artist_and_track_c = CategoricalDtype(sorted(df.artist_and_track.unique()), ordered=True)

    row = df.playlist_id.astype(playlist_id_c).cat.codes
    col = df.artist_and_track.astype(artist_and_track_c).cat.codes
    sparse_matrix = csr_matrix((df['rating'], (row, col)), \
                               shape=(playlist_id_c.categories.size, artist_and_track_c.categories.size))
    return sparse_matrix, playlist_id_c

def create_rec_df(playlist_id, df):
    df_rec = df[df.playlist_id != playlist_id]
    sim_dict = create_sim_dict(playlist_id, df)
    df_sim = pd.DataFrame(zip(sim_dict.keys(), sim_dict.values()))
    df_sim.columns = ['playlist_id','sim']
    df_rec = df.merge(df_sim,how='left', on='playlist_id')
    grouped = df_rec.groupby(by = 'artist_and_track').sum()
    recommendations = grouped.sort_values(by = 'sim', ascending = False)
    return recommendations

def recommend_for_playlist(user_id, playlist_id, df, list_of_searches):
    my_playlist = make_playlist(user_id, playlist_id, df, list_of_searches)
    df = df.append(my_playlist)
    recommendations = create_rec_df(playlist_id, df)
    return recommendations

def simplify(messy_rec, number_tracks):
    combined = []
    for row in messy_rec.head(number_tracks).itertuples():
        combined.append(row.Index.split('|||||'))
    clean_df = pd.DataFrame(np.array(combined))
    clean_df.columns = ['artist','track']
    return clean_df

def get_input_and_give_recs():

    user_id = entry1.get()
    playlist_id = entry2.get()
    list_of_searches = [(entry3.get(), entry4.get()), (entry5.get(), entry6.get())]
    number_tracks = int(entry7.get())
    recs = recommend_for_playlist(user_id, playlist_id, df, list_of_searches)
    print(simplify(recs,number_tracks))
    return recs

root = tk.Tk()
root.configure(background='dark red')
root.geometry("1500x900")

tk.Button(root, text='Close',command=root.destroy).grid(row=2, column=2)


# tk.Button(root, text='Graph CA test', command=graph_1).grid(row=3, column=10) # Call the graph_1 function
tk.Button(root, text='Get Recommendations', command=get_input_and_give_recs, background = "dark red", font=("Helvetica", 16)).grid(row=20, column=20)
# tk.Button(root, text='Graph Temperature', command=create_temperature_graph).grid(row=5, column=10)
# tk.Button(root, text='All Graphs', command=create_all_graphs).grid(row=6, column=10)

label1 = Label(root,text = 'Username', background='dark red', font=("Helvetica", 16), fg = "white smoke")
label1.grid(column = 1, row=1)
label1.config(justify = CENTER)

entry1 = tk.Entry(root, width = 30)
entry1.grid(column = 1, row=2)

label2 = Label(root, text="Playlist Name", background='dark red', font=("Helvetica", 16), fg = "white smoke")
label2.grid(column = 1, row=3)
label2.config(justify = CENTER)

entry2 = Entry(root, width = 30, background='light grey')
entry2.grid(column = 1, row=4)

label3 = Label(root, text="Artist 1", background='dark red', font=("Helvetica", 16), fg = "white smoke")
label3.grid(column = 1, row=5)
label3.config(justify = CENTER)

entry3 = Entry(root, width = 30)
entry3.grid(column = 1, row=6)

label4 = Label(root,text = 'Track 1', background='dark red', font=("Helvetica", 16), fg = "white smoke")
label4.grid(column = 1, row=7)
label4.config(justify = CENTER)

entry4 = Entry(root, width = 30)
entry4.grid(column = 1, row=8)

label5 = Label(root, text="Artist 2", background='dark red', font=("Helvetica", 16), fg = "white smoke")
label5.grid(column = 1, row=9)
label5.config(justify = CENTER)

entry5 = Entry(root, width = 30)
entry5.grid(column = 1, row=10)

label6 = Label(root, text="Track 2", background='dark red', font=("Helvetica", 16), fg = "white smoke")
label6.grid(column = 1, row=11)
label6.config(justify = CENTER)

entry6 = Entry(root, width = 30)
entry6.grid(column = 1, row=12)

label7 = Label(root,text = 'Number of Tracks', background='dark red', font=("Helvetica", 16), fg = "white smoke")
label7.grid(column = 1, row=13)
label7.config(justify = CENTER)

entry7 = Entry(root, width = 30)
entry7.grid(column = 1, row=14)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(15, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

menu =  Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="New", command=create_window)
subMenu.add_command(label="Open", command=doNothing)
subMenu.add_command(label="Restart", command=doNothing)
subMenu.add_command(label="Exit", command=doNothing)
editMenu = Menu(menu)
menu.add_cascade(label = "Help", menu=editMenu)
editMenu.add_command(label="Help", command=doNothing)

root.mainloop()