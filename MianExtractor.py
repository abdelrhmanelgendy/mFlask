from pytube import YouTube,Playlist
class MainExtractor:
    mUrl=""
    def __init__(self,userUrl):
        self.mUrl=userUrl


    def createYoutube(self):
        return YouTube(self.mUrl)


    def createStreams(self):
        return self.createYoutube().streams


    def getVideoTittle(self):
        return self.createYoutube().title


    def getvideosUrls(self):
        streams=self.createStreams()
        itags=streams.itag_index
        for i in itags:
            return TagsVideos(streams.get_by_itag(i),streams.get_by_itag(i).url)



class TagsVideos:
    from pytube import Stream
    itag: Stream
    videoUrl: str
    def __init__(self,itag:Stream,videoUrl:str):
        self.itag=itag
        self.videoUrl=videoUrl



