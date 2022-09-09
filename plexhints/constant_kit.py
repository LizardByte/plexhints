# cache time constants
CACHE_1MINUTE = 60  # type: int
CACHE_1HOUR = 3600  # type: int
CACHE_1DAY = 86400  # type: int
CACHE_1WEEK = 604800  # type: int
CACHE_1MONTH = 2592000  # type: int


class ClientPlatforms(object):
    MacOSX = 'MacOSX'
    Linux = 'Linux'
    Windows = 'Windows'
    iOS = 'iOS'
    Android = 'Android'
    LGTV = 'LGTV'
    Roku = 'Roku'


class Protocols(object):
    DASH = 'dash'
    HTTP = 'http'
    HLS = 'hls'
    RTMP = 'rtmp'


class OldProtocols(Protocols):
    Shoutcast = 'shoutcast'
    WebKit = 'webkit'
    HTTPStreamingVideo = 'http-streaming-video'
    HTTPStreamingVideo720p = 'http-streaming-video-720p'
    HTTPMP4Video = 'http-mp4-video'
    HTTPMP4Video720p = 'http-mp4-video-720p'
    HTTPVideo = 'http-video'
    RTMP = 'rtmp'
    HTTPLiveStreaming = 'http-live-streaming'
    HTTPMP4Streaming = 'http-mp4-streaming'


class ServerPlatforms(object):
    MacOSX_i386 = 'MacOSX-i386'
    Linux_i386 = 'Linux-i386'
    Linux_x86_64 = 'Linux-x86_64'
    Linux_MIPS = 'Linux-MIPS'
    Linux_ARM = 'Linux-ARM'


class ViewTypes(object):
    Grid = 'grid'
    List = 'list'


class SummaryTextTypes(object):
    NoSummary = 0
    Short = 1
    Long = 2


class AudioCodecs(object):
    AAC = 'aac'
    DCA = 'dca'
    MP3 = 'mp3'
    WMA = 'wma'
    WMAP = 'wmap'
    VORBIS = 'vorbis'
    FLAC = 'flac'


class VideoCodecs(object):
    H263 = 'h263'
    H264 = 'h264'
    VP6 = 'vp6'
    WVC1 = 'wvc1'
    DIVX = 'divx'
    DIV4 = 'div4'
    XVID = 'xvid'
    THEORA = 'theora'


class Containers(object):
    MKV = 'mkv'
    MP4 = 'mp4'
    MPEGTS = 'mpegts'
    MOV = 'mov'
    AVI = 'avi'
    MP3 = 'mp3'
    OGG = 'ogg'
    FLAC = 'flac'
    FLV = 'flv'


class ContainerContents(object):
    Secondary = 'secondary'
    Mixed = 'mixed'
    Genres = 'genre'
    Playlists = 'playlist'
    Albums = 'album'
    Tracks = 'track'
    GenericVideos = 'video'
    Episodes = 'episode'
    Movies = 'movie'
    Seasons = 'season'
    Shows = 'show'
    Artists = 'artist'


class StreamTypes(object):
    Video = 1
    Audio = 2
    Subtitle = 3
