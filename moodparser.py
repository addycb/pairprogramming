from lyricsgenius import Genius
from matplotlib import artist


token="JVRbucZ0zodg1YRlSoURfzrCUOYc4jhh_d-sSM74UNzVY18crYOkW568cjzkfqA2"
genius = Genius(token)
genius.remove_section_headers = True
print("Welcome to Mood Finder.")

def mainmenu():
    option=input('''Select an option. 
            [0]: Mood by song
            [1]: Mood by album
            [2]: Mood by artist\n''')
    if option=="0":
        artistname=input("Enter artist name: ")
        songtitle=input("Enter song title: ")
        songmood(artistname,songtitle)
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


def songmood(artistname="",songtitle=""):
    positive = open("positive-words.txt", "r")
    positivewords=positive.read()
    positive.close()
    negative = open("negative-words.txt", "r", encoding='ISO-8859-1')
    negativewords=negative.read()
    negative.close()
    numposwords=0
    numnegwords=0
    lyrics=songlyrics(songtitle,artistname)
    lyrics=lyrics.split() 
    index=0
    songtitle=songtitle.split()
    lyrics=lyrics[len(songtitle)+1:]
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
    print(str(numnegwords)+" negative words, "+str(numposwords)+" postive words")
    return [int(numnegwords),int(numposwords)]

"""
def optselect(songtitle,artistname):
if lyrics[index][0]=="*" and lyrics[index][-1]=="*":  #Ignore adlibs
            lyrics[index]=lyrics[index][1:-1]
            print("Fixed *"+lyrics[index]+"* to "+lyrics[index])
"""