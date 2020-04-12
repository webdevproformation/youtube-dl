# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor


class PlayerGlobeWienIE(InfoExtractor):
    _VALID_URL = r'https?://player.(globe.wien|hader.at)/(globe-wien|hader)/(?P<id>.*)'
    _TESTS = [
        {
            'url': 'https://player.globe.wien/globe-wien/corona-podcast-teil-4',
            'info_dict': {
                'id': 'corona-podcast-teil-4',
                'ext': 'mp4',
                'title': 'Eckel & Niavarani & Sarsam - Im Endspurt versagt',
            },
            'params': {
                'format': 'bestvideo',
            }
        },
        {
            'url': 'https://player.globe.wien/globe-wien/corona-podcast-teil-4',
            'info_dict': {
                'id': 'corona-podcast-teil-4',
                'ext': 'm4a',
                'title': 'Eckel & Niavarani & Sarsam - Im Endspurt versagt',
            },
            'params': {
                'format': 'bestaudio',
                'skip_download': True,
            }
        },
        {
            'url': 'https://player.hader.at/hader/hader-indien-video',
            'info_dict': {
                'id': 'hader-indien-video',
                'ext': 'mp4',
                'title': 'Film der Woche - Indien',
            },
            'params': {
                'format': 'bestvideo',
            }
        },
        {
            'url': 'https://player.hader.at/hader/hader-indien-video',
            'info_dict': {
                'id': 'hader-indien-video',
                'ext': 'm4a',
                'title': 'Film der Woche - Indien',
            },
            'params': {
                'format': 'bestaudio',
                'skip_download': True,
            }
        },
        {
            'url': 'https://player.hader.at/hader/hader-indien',
            'info_dict': {
                'id': 'hader-indien',
                'ext': 'mp3',
                'title': 'Hader & Dorfer lesen Indien',
            }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        print(video_id)
        webpage = self._download_webpage(url, video_id)
        formats = []
        title = self._html_search_regex(r'<title>(.+?)</title>', webpage, 'title')
        title = re.sub(r'^(Globe Wien VOD -|Hader VOD -)\s*', '', title)

        streamurl = self._download_json("https://player.globe.wien/api/playout?vodId=" + video_id,
                                        video_id).get('streamUrl')

        if streamurl.get('hls'):
            formats.extend(self._extract_m3u8_formats(
                streamurl.get('hls'), video_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls'))

        if streamurl.get('dash'):
            formats.extend(self._extract_mpd_formats(
                streamurl.get('dash'), video_id, mpd_id='dash', fatal=False))

        if streamurl.get('audio'):
            return {
                'id': video_id,
                'title': title,
                'url': streamurl.get('audio'),
            }

        self._sort_formats(formats)
        return {
            'id': video_id,
            'title': title,
            'formats': formats,
        }
