from pytube import YouTube, Playlist, Stream
import json, dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class MainExtractor:
    videoAndAudiosItags = [5, 6, 17, 18, 22, 34, 35, 36, 37, 38, 43, 44, 45, 46, 82, 83, 84, 85, 92, 93, 94, 95, 96,
                           100, 101, 102, 132, 151, 395]
    audiosOnlyItags = [139, 140, 141, 171, 249, 250, 251]

    mUrl = ""
    videoStream: Stream
    youTubeVideo: YouTube

    def __init__(self, userUrl):
        self.mUrl = userUrl
        self._createYoutube()

    def createStream(self):
        self.videoStream = self.youTubeVideo.streams

    def _createYoutube(self):
        self.youTubeVideo = YouTube(self.mUrl)

    def getVideoDescription(self):
        return self.youTubeVideo.description

    def getVideoData(self):

        result = "{'title':'" + self.youTubeVideo.title + "','views':'" + str(
            self.youTubeVideo.views) + "','publishDate':'" + str(
            self.youTubeVideo.publish_date) + "', 'rating' :'" + str(self.youTubeVideo.rating) + "','author':'" + str(
            self.youTubeVideo.author) + "','length':'" + str(
            self.youTubeVideo.length) + "','thimbnail':'" + str(self.youTubeVideo.thumbnail_url) + "'}"

        return result

    def getvideosUrls(self):
        streams = self.videoStream.filter(progressive=True)
        itags = streams.itag_index
        listOfUrlTags = []
        for i in itags:
            stream = streams.get_by_itag(i)
            rsult = ResultData(stream.mime_type,
                               stream.itag,
                               stream.resolution,
                               stream.type,
                               stream.abr,
                               stream.url)
            listOfUrlTags.append(rsult)
        return json.dumps(listOfUrlTags, cls=EnhancedJSONEncoder)

    def getVideoOnly(self):
        streams = self.videoStream.filter(progressive=True).filter(type='video')
        itags = streams.itag_index
        listOfUrlTags = []
        for i in itags:
            stream = streams.get_by_itag(i)
            rsult = ResultData(stream.mime_type,
                               stream.itag,
                               stream.resolution,
                               stream.type,
                               stream.abr,
                               stream.url)
            listOfUrlTags.append(rsult)
        return json.dumps(listOfUrlTags, cls=EnhancedJSONEncoder)

    def getAudioOnly(self):
        streams = self.videoStream.filter(type='audio')
        itags = streams.itag_index
        listOfUrlTags = []
        for i in itags:
            stream = streams.get_by_itag(i)
            rsult = ResultData(stream.mime_type,
                               stream.itag,
                               stream.resolution,
                               stream.type,
                               stream.abr,
                               stream.url)
            listOfUrlTags.append(rsult)
        return json.dumps(listOfUrlTags, cls=EnhancedJSONEncoder)


from dataclasses import dataclass


@dataclass
class ResultData:
    mime_type: str
    itag: str
    res: str
    type: str
    abr: str
    url: str

    def __init__(self, mime_type: str,
                 itag: str,
                 res: str,
                 type: str,
                 abr: str,
                 url: str):
        self.url = url
        self.mime_type = mime_type
        self.itag = itag
        self.res = res
        self.type = type
        self.abr = abr


class PlayListsExtractor:
    mPlayListUrl = ""
    mPlayListFromUrl = Playlist

    def __init__(self, playLitsUrl):
        self.mPlayListUrl = playLitsUrl
        self.mPlayListFromUrl = Playlist(playLitsUrl)

    def getPlayListData(self):
        owner = self.mPlayListFromUrl.owner
        title = self.mPlayListFromUrl.title
        views = self.mPlayListFromUrl.views
        return "{'owner':'" + str(owner) + "', 'title':'" + str(title) + "','views':'" + str(views) + "'}"

    def getVideosInsidePlayList(self):
        return self.mPlayListFromUrl.video_urls

    def getAllVideoData(self):
        urls = self.getVideosInsidePlayList()
        listsOfData = []
        for url in urls:
            mainExc = MainExtractor(url)
            videoData = mainExc.getVideoData()
            listsOfData.append(videoData)
        return listsOfData




ex=MainExtractor("https://youtu.be/e-ORhEE9VVg")
ex.createStream()
print(ex.getAudioOnly())

from flask import Flask
from flask import request

app = Flask(__name__)
#
#
#
@app.route('/predict',methods=["POST"])
def hello_predict():
    val=str(request.form['v1'])
    ex=MainExtractor(val)
    ex.createStream()
    return ex.getAudioOnly()

    # str(v1+v2+v3+v4)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# ply=PlayListsExtractor("https://youtube.com/playlist?list=PLQkwcJG4YTCT-lTlkOmE-PpRkuyNXq6sW")
# print(ply.getAllVideoData())
# print(ply.getVideosInsidePlayList())
# print(ply.getPlayListData())