# -*- coding: utf-8 -*-

# local imports
from plexhints import constant_kit


MINUTE_SECONDS = 60
HOUR_SECONDS = MINUTE_SECONDS * 60
DAY_SECONDS = HOUR_SECONDS * 24
WEEK_SECONDS = DAY_SECONDS * 7
MONTH_SECONDS = DAY_SECONDS * 30


def test_cache_constants():
    assert constant_kit.CACHE_1MINUTE == MINUTE_SECONDS, "CACHE_1MINUTE should be {} seconds".format(MINUTE_SECONDS)
    assert constant_kit.CACHE_1HOUR == HOUR_SECONDS, "CACHE_1HOUR should be {} seconds".format(HOUR_SECONDS)
    assert constant_kit.CACHE_1DAY == DAY_SECONDS, "CACHE_1DAY should be {} seconds".format(DAY_SECONDS)
    assert constant_kit.CACHE_1WEEK == WEEK_SECONDS, "CACHE_1WEEK should be {} seconds".format(WEEK_SECONDS)
    assert constant_kit.CACHE_1MONTH == MONTH_SECONDS, "CACHE_1MONTH should be {} seconds".format(MONTH_SECONDS)


def test_client_platforms():
    client_platforms = constant_kit.ClientPlatforms()
    assert client_platforms.MacOSX == 'MacOSX', "ClientPlatforms.MacOSX should be 'MacOSX'"
    assert client_platforms.Linux == 'Linux', "ClientPlatforms.Linux should be 'Linux'"
    assert client_platforms.Windows == 'Windows', "ClientPlatforms.Windows should be 'Windows'"
    assert client_platforms.iOS == 'iOS', "ClientPlatforms.iOS should be 'iOS'"
    assert client_platforms.Android == 'Android', "ClientPlatforms.Android should be 'Android'"
    assert client_platforms.LGTV == 'LGTV', "ClientPlatforms.LGTV should be 'LGTV'"
    assert client_platforms.Roku == 'Roku', "ClientPlatforms.Roku should be 'Roku'"


def test_protocols():
    protocols = constant_kit.Protocols()
    assert protocols.DASH == 'dash', "Protocols.DASH should be 'dash'"
    assert protocols.HTTP == 'http', "Protocols.HTTP should be 'http'"
    assert protocols.HLS == 'hls', "Protocols.HLS should be 'hls'"
    assert protocols.RTMP == 'rtmp', "Protocols.RTMP should be 'rtmp'"


def test_old_protocols():
    old_protocols = constant_kit.OldProtocols()
    assert old_protocols.Shoutcast == 'shoutcast', "OldProtocols.Shoutcast should be 'shoutcast'"
    assert old_protocols.WebKit == 'webkit', "OldProtocols.WebKit should be 'webkit'"
    assert old_protocols.HTTPStreamingVideo == 'http-streaming-video', \
        "OldProtocols.HTTPStreamingVideo should be 'http-streaming-video'"
    assert old_protocols.HTTPStreamingVideo720p == 'http-streaming-video-720p', \
        "OldProtocols.HTTPStreamingVideo720p should be 'http-streaming-video-720p'"
    assert old_protocols.HTTPMP4Video == 'http-mp4-video', "OldProtocols.HTTPMP4Video should be 'http-mp4-video'"
    assert old_protocols.HTTPMP4Video720p == 'http-mp4-video-720p', \
        "OldProtocols.HTTPMP4Video720p should be 'http-mp4-video-720p'"
    assert old_protocols.HTTPVideo == 'http-video', "OldProtocols.HTTPVideo should be 'http-video'"
    assert old_protocols.RTMP == 'rtmp', "OldProtocols.RTMP should be 'rtmp'"
    assert old_protocols.HTTPLiveStreaming == 'http-live-streaming', \
        "OldProtocols.HTTPLiveStreaming should be 'http-live-streaming'"
    assert old_protocols.HTTPMP4Streaming == 'http-mp4-streaming', \
        "OldProtocols.HTTPMP4Streaming should be 'http-mp4-streaming'"


def test_view_types():
    view_types = constant_kit.ViewTypes()
    assert view_types.Grid == 'grid', "ViewTypes.Grid should be 'grid'"
    assert view_types.List == 'list', "ViewTypes.List should be 'list'"


def test_summary_text_types():
    summary_text_types = constant_kit.SummaryTextTypes()
    assert summary_text_types.NoSummary == 0, "SummaryTextTypes.NoSummary should be 0"
    assert summary_text_types.Short == 1, "SummaryTextTypes.Short should be 1"
    assert summary_text_types.Long == 2, "SummaryTextTypes.Long should be 2"


def test_audio_codecs():
    audio_codecs = constant_kit.AudioCodecs()
    assert audio_codecs.AAC == 'aac', "AudioCodecs.AAC should be 'aac'"
    assert audio_codecs.DCA == 'dca', "AudioCodecs.DCA should be 'dca'"
    assert audio_codecs.MP3 == 'mp3', "AudioCodecs.MP3 should be 'mp3'"
    assert audio_codecs.WMA == 'wma', "AudioCodecs.WMA should be 'wma'"
    assert audio_codecs.WMAP == 'wmap', "AudioCodecs.WMAP should be 'wmap'"
    assert audio_codecs.VORBIS == 'vorbis', "AudioCodecs.VORBIS should be 'vorbis'"
    assert audio_codecs.FLAC == 'flac', "AudioCodecs.FLAC should be 'flac'"


def test_video_codecs():
    video_codecs = constant_kit.VideoCodecs()
    assert video_codecs.H263 == 'h263', "VideoCodecs.H263 should be 'h263'"
    assert video_codecs.H264 == 'h264', "VideoCodecs.H264 should be 'h264'"
    assert video_codecs.VP6 == 'vp6', "VideoCodecs.VP6 should be 'vp6'"
    assert video_codecs.WVC1 == 'wvc1', "VideoCodecs.WVC1 should be 'wvc1'"
    assert video_codecs.DIVX == 'divx', "VideoCodecs.DIVX should be 'divx'"
    assert video_codecs.DIV4 == 'div4', "VideoCodecs.DIV4 should be 'div4'"
    assert video_codecs.XVID == 'xvid', "VideoCodecs.XVID should be 'xvid'"
    assert video_codecs.THEORA == 'theora', "VideoCodecs.THEORA should be 'theora'"


def test_containers():
    containers = constant_kit.Containers()
    assert containers.MP4 == 'mp4', "Containers.MP4 should be 'mp4'"
    assert containers.MP4 == 'mp4', "Containers.MP4 should be 'mp4'"
    assert containers.MPEGTS == 'mpegts', "Containers.MPEGTS should be 'mpegts'"
    assert containers.MOV == 'mov', "Containers.MOV should be 'mov'"
    assert containers.AVI == 'avi', "Containers.AVI should be 'avi'"
    assert containers.MP3 == 'mp3', "Containers.MP3 should be 'mp3'"
    assert containers.OGG == 'ogg', "Containers.OGG should be 'ogg'"
    assert containers.FLAC == 'flac', "Containers.FLAC should be 'flac'"
    assert containers.FLV == 'flv', "Containers.FLV should be 'flv'"


def test_container_contents():
    container_contents = constant_kit.ContainerContents()
    assert container_contents.Secondary == 'secondary', "ContainerContents.Secondary should be 'secondary'"
    assert container_contents.Mixed == 'mixed', "ContainerContents.Mixed should be 'mixed'"
    assert container_contents.Genres == 'genre', "ContainerContents.Genres should be 'genre'"
    assert container_contents.Playlists == 'playlist', "ContainerContents.Playlists should be 'playlist'"
    assert container_contents.Albums == 'album', "ContainerContents.Albums should be 'album'"
    assert container_contents.Tracks == 'track', "ContainerContents.Tracks should be 'track'"
    assert container_contents.GenericVideos == 'video', "ContainerContents.GenericVideos should be 'video'"
    assert container_contents.Episodes == 'episode', "ContainerContents.Episodes should be 'episode'"
    assert container_contents.Movies == 'movie', "ContainerContents.Movies should be 'movie'"
    assert container_contents.Seasons == 'season', "ContainerContents.Seasons should be 'season'"
    assert container_contents.Shows == 'show', "ContainerContents.Shows should be 'show'"
    assert container_contents.Artists == 'artist', "ContainerContents.Artists should be 'artist'"


def test_stream_types():
    stream_types = constant_kit.StreamTypes()
    assert stream_types.Video == 1, "StreamTypes.Video should be 1"
    assert stream_types.Audio == 2, "StreamTypes.Audio should be 2"
    assert stream_types.Subtitle == 3, "StreamTypes.Subtitle should be 3"
