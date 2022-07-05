from lyricsgenius import Genius
from matplotlib import artist


token="JVRbucZ0zodg1YRlSoURfzrCUOYc4jhh_d-sSM74UNzVY18crYOkW568cjzkfqA2"
genius = Genius(token)
print("Welcome to Mood Finder.")

def mainmenu():
    option=input('''Select an option. 
            [0]: Mood by song
            [1]: Mood by album
            [2]: Mood by artist\n''')
    if option=="0":
        return songmood()
    elif option=="1":
        return albummood()
    elif option=="2":
        return artistmood()
    else:
        print("Bad input.")
        return mainmenu()

def songlyrics(songtitle,artistname):
    '''
    Gets song lyrics using api, splits lyrics to list
    '''
    song = genius.search_song(songtitle, artistname)  
    return song.lyrics

def albummood():
    return 0

def artistmood():
    return 0

def analyzesong(lyrics):
    return 0


def songmood():
    positive = open("positive-words.txt", "r")
    positivewords=positive.read()
    positive.close()
    negative = open("negative-words.txt", "r", encoding='ISO-8859-1')
    negativewords=negative.read()
    negative.close()
    numposwords=0
    numnegwords=0
    artistname=input("Enter artist name: ")
    songtitle=input("Enter song title: ")
    lyrics=songlyrics(songtitle,artistname)
    lyrics=lyrics.split() 
    lyrics=lyrics[len(songtitle):]  #Ignore songtitle
    index=0
    while(index<len(lyrics)-1):
        if "[" in lyrics[index] and "]" not in lyrics[index]:
            index+=1
            while lyrics[index][-1]!="]":
                index+=1
        elif lyrics[index][0]=="*":  #Ignore adlibs
            pass
        else:
            if lyrics[index] in positivewords:
                numposwords+=1
            elif lyrics[index] in negativewords:
                numnegwords+=1
            print(lyrics[index])  #Replace with adjust score according to word
        index+=1
        print(str(numnegwords)+" negative words, "+str(numposwords)+" postive words")
    return analyzesong(lyrics)


mainmenu()
