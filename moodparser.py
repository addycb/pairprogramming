from lyricsgenius import Genius
import mysql.connector

token = "JVRbucZ0zodg1YRlSoURfzrCUOYc4jhh_d-sSM74UNzVY18crYOkW568cjzkfqA2"
genius = Genius(token)
genius.remove_section_headers = True
print("Welcome to Sentiment Finder.")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rooted!!lel4",
    database="sentimentstore"
)


def mainmenu():
    option = input('''Select an option. 
            [0]: Sentiment by song
            [1]: Sentiment by album\n''')
    if option == "0":
        artistname = input("Enter artist name: ")
        songname = input("Enter song name: ")
        result = songsentimentselect(artistname, songname)
        print(result)
        return mainmenu()
    elif option == "1":
        artistname = input("Enter artist name: ")
        albumname = input("Enter album name: ")
        result = albumsentimentselect(artistname, albumname)
        print(result)
        return mainmenu()
    else:
        print("Bad input.")
        #return mainmenu()


def songlyrics(songname, artistname):
    '''
    Gets song lyrics using lyricsgenius api, splits lyrics to list
    '''
    song = genius.search_song(songname, artistname)
    print(song.lyrics)
    return song.lyrics


def albumsentiment(artistname, albumname):
    '''
    Gets song names using lyricsgenius api
    '''
    #album=genius.search_albums(albumname+" "+artistname) Find album id
    id = getalbumid(artistname, albumname)
    album = genius.album_tracks(id)  # Using album id get song tracks
    #next get track ids
    scores = []
    for x in album["tracks"]:
        x = x["song"]
        songname = x["title"]
        artistname = x["artist_names"]
        query = "SELECT sentiment FROM songsentiment WHERE artistname='{0}' AND songname='{1}'".format(
            artistname, songname)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data != None:
            data = data[0]
            print("Song: "+str(songname)+" Score: "+str(data))
            scores.append(float(data))
        else:
            lyrics = songlyrics(songname, artistname)
            analysis = analyzesong(lyrics, songname, artistname)
            print("Song: "+str(songname)+" Score: "+str(analysis[2]))
            scores.append(float(analysis[2]))
    avgsentiment = sum(scores)/len(scores)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO albumsentiment(albumname, artistname, sentiment) VALUES (%s, %s, %s)",
                   (albumname, artistname, avgsentiment))
    conn.commit()
    return [albumname, artistname, avgsentiment]


def albumsentimentselect(artistname, albumname):
    query = "SELECT artistname, albumname, sentiment FROM albumsentiment WHERE artistname='{0}' AND albumname='{1}'".format(
        artistname, albumname)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    if data != None:
        print("Album Query successful")
        return data
    else:
        print("Album Query failed")
        return albumsentiment(artistname, albumname)


def songsentiment(artistname="", songname=""):
    lyrics = songlyrics(songname, artistname)
    return analyzesong(lyrics, songname, artistname)


def songsentimentselect(artistname, songname):
    query = "SELECT sentiment FROM songsentiment WHERE artistname='{0}' AND songname='{1}'".format(
        artistname, songname)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    if data != None:
        print("Song query successful")
        return data
    else:
        print("Song query failed")
        return songsentiment(artistname, songname)


def analyzesong(lyrics, songname, artistname):
    positive = open("positive-words.txt", "r")
    positivewords = positive.read()
    positive.close()
    negative = open("negative-words.txt", "r", encoding='ISO-8859-1')
    negativewords = negative.read()
    negative.close()
    numposwords = 0
    numnegwords = 0
    lyrics = lyrics.split()
    index = 0
    songnamels = songname.split()
    lyrics = lyrics[len(songnamels)+1:]
    print(lyrics)
    while(index < len(lyrics)-1):
        if lyrics[index][0] == "*":  # Ignore annotation blocks
            if lyrics[index][-1] == "*":
                print("Skipped "+lyrics[index])
            else:
                while(lyrics[index][-1] != "*" and index < len(lyrics)-1):
                    print("Skipped "+lyrics[index])
                    index += 1
                print("Skipped "+lyrics[index])
        else:
            if lyrics[index] in positivewords:
                numposwords += 1
                #print("Positive: "+lyrics[index])
            elif lyrics[index] in negativewords:
                numnegwords += 1
                #print("Negative: "+lyrics[index])
            else:
                pass
                #print("Neutral: "+lyrics[index])

        print(str(numnegwords)+" negative words, " +
              str(numposwords)+" postive words")
        index += 1
    print(str(numnegwords)+" negative words, " +
          str(numposwords)+" postive words total")
    sentiment = numposwords/(numposwords+numnegwords)
    print("sentiment="+str(sentiment)+" postive")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songsentiment(songname, artistname, sentiment) VALUES (%s, %s, %s)",
                   (songname, artistname, sentiment))
    conn.commit()
    return [songname, artistname, sentiment]


def getalbumid(artistname, albumname):
    album = genius.search_albums(albumname+" "+artistname)
    options = album["sections"][0]["hits"]
    i = 0
    for x in options:
        print(i)
        print(x["result"]["name_with_artist"])
        print("\n")
        i += 1
    option = input("Enter correct result by number: ")
    return (album["sections"][0]["hits"][int(option)]["result"]["id"])


if __name__ == '__main__':
    mainmenu()
