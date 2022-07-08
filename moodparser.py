from lyricsgenius import Genius
import mysql.connector
from mysql.connector import Error

token="JVRbucZ0zodg1YRlSoURfzrCUOYc4jhh_d-sSM74UNzVY18crYOkW568cjzkfqA2"
genius = Genius(token)
genius.remove_section_headers = True
print("Welcome to Mood Finder.")




conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rooted!!lel4",
    database="sentimentstore"
    )





def mainmenu():
    option=input('''Select an option. 
            [0]: Mood by song
            [1]: Mood by album
            [2]: Mood by artist\n''')
    if option=="0":
        artistname=input("Enter artist name: ")
        songname=input("Enter song name: ")
        songmood(artistname,songname)
        return mainmenu()
    elif option=="1":
        pass
        #return mainmenu()
    elif option=="2":
        pass
        #return mainmenu()  
    else:
        print("Bad input.")
        #return mainmenu()
    
def songlyrics(songname,artistname):
    '''
    Gets song lyrics using lyricsgenius api, splits lyrics to list
    '''
    song = genius.search_song(songname, artistname)  
    print(song.lyrics)
    return song.lyrics  


def albumsongs(albumname,artistname):
    '''
    Gets song names using lyricsgenius api
    '''
    #album=genius.search_albums(albumname+" "+artistname) Find album id
    album=genius.album_tracks(12411) #Using album id get song tracks
    #next get track ids
    scores=[]
    for x in album["tracks"]:
        print(x)
        x=x["song"]
        songname=x["title"]
        artistname=x["artist_names"]
        x=x["id"]
        lyrics=songlyrics(str(songname,artistname))
        #print("songname")
        #print(songname)
        #print("artistname")
        #print(artistname)
        #print("lyrics")
        #print(lyrics)
        #print(analyzesong(lyrics,songname,artistname))
        analysis=analyzesong(lyrics,songname,artistname)
        scores.append(analysis[3])
    avgsentiment=sum(scores)/len(scores)
    return [albumname,artistname,avgsentiment]
            


def albummood():
    return 0

def artistmood():
    return 0

def analyzesong(lyrics,songname,artistname):
    positive = open("positive-words.txt", "r")
    positivewords=positive.read()
    positive.close()
    negative = open("negative-words.txt", "r", encoding='ISO-8859-1')
    negativewords=negative.read()
    negative.close()
    numposwords=0
    numnegwords=0
    lyrics=lyrics.split() 
    index=0
    songname=songname.split()
    lyrics=lyrics[len(songname)+1:]
    print(lyrics)
    while(index<len(lyrics)-1):
        if lyrics[index][0]=="*" :  #Ignore annotation blocks
            if lyrics[index][-1]=="*":
                print("Skipped "+lyrics[index])
            else:
                while(lyrics[index][-1]!="*" and index<len(lyrics)-1):
                    print("Skipped "+lyrics[index])
                    index+=1
                print("Skipped "+lyrics[index])
        else:
            if lyrics[index] in positivewords:
                numposwords+=1
                print("Positive: "+lyrics[index])
            elif lyrics[index] in negativewords:
                numnegwords+=1
                print("Negative: "+lyrics[index])
            else:
                print("Neutral: "+lyrics[index])

        print(str(numnegwords)+" negative words, "+str(numposwords)+" postive words")
        index+=1
    print(str(numnegwords)+" negative words, "+str(numposwords)+" postive words total")
    sentiment=numposwords/(numposwords+numnegwords)
    print("sentiment="+str(sentiment)+" postive")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO songsentiment(songname, artistname, sentiment) VALUES (%s, %s, %s)", (songname,artistname,sentiment))
    conn.commit()
    return [songname,artistname,sentiment]



def songmoodselect(artistname,songname):
    try:
        query= "SELECT sentiment FROM songsentiment WHERE artistname='{0}' AND songname='{1}'".format(artistname,songname)
        cursor=conn.cursor()
        cursor.execute(query)
        data=cursor.fetchone()
        print("Query successful")
        return data
    except:
        print("Query failed")
        return songmood(artistname,songname)

def songmood(artistname="",songname=""):
    lyrics=songlyrics(songname,artistname)
    return analyzesong(lyrics,songname,artistname)
   

"""
def optselect(songtitle,artistname):
if lyrics[index][0]=="*" and lyrics[index][-1]=="*":  #Ignore adlibs
            lyrics[index]=lyrics[index][1:-1]
            print("Fixed *"+lyrics[index]+"* to "+lyrics[index])
"""
print(albumsongs("Abbey Road","The Beatles"))