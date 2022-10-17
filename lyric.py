import re


class Lyric():
    def __init__(self):
        self.artist = None
        self.title = None
        self.album = None
        self.by = None
        self.offset = 0
        self.data = []

    def parse_lrc(self, lyric: str):
        lyric = lyric.replace('\r\n', '\n')

        offset_tag = re.search('\[offset:\s*(-?\d+)\]', lyric)
        artist_tag = re.search('\[ar:\s*(.*?)\]', lyric)
        title_tag = re.search('\[ti:\s*(.*?)\]', lyric)
        album_tag = re.search('\[al:\s*(.*?)\]', lyric)
        by_tag = re.search('\[by:\s*(.*?)\]', lyric)
        if offset_tag:
            self.offset = int(offset_tag.group(1))
        if artist_tag:
            self.artist = artist_tag.group(1).strip()
        if title_tag:
            self.title = title_tag.group(1).strip()
        if album_tag:
            self.album = album_tag.group(1).strip()
        if by_tag:
            self.by = by_tag.group(1).strip()

        lines = lyric.split('\n')
        data = []
        pattern = re.compile('\[(\d+):(\d+)(\.?\d+)?\]')
        for line in lines:
            match = pattern.match(line)
            if match:
                times = []
                while(match):
                    t = int(match.group(1)) * 60000 + \
                        int(match.group(2)) * 1000
                    length = 3 + len(match.group(1)) + len(match.group(2))
                    if match.group(3):
                        t += int(match.group(3)[1:])
                        length += len(match.group(3))
                    t -= self.offset
                    times.append(t)
                    line = line[length:]
                    match = pattern.match(line)
                for time in times:
                    data.append((time, line.strip()))
        data = sorted(data, key=lambda x: x[0])
        self.data = data
        return self

    def to_lrc(self, remove_tag=False):
        lrc = ''
        if not remove_tag:
            if self.artist:
                lrc += '[ar:{}]\n'.format(self.artist)
            if self.title:
                lrc += '[ti:{}]\n'.format(self.title)
            if self.album:
                lrc += '[al:{}]\n'.format(self.album)
            if self.by:
                lrc += '[by:{}]\n'.format(self.by)
        for d in self.data:
            time = d[0]
            m = time // 60000
            time %= 60000
            s = time // 1000
            ms = time % 1000
            lrc += '[{:02d}:{:02d}.{:03d}]{}\n'.format(m, s, ms, d[1])
        return lrc

    def to_srt(self):
        srt = ''
        if not self.data:
            return srt
        self.data.append((self.data[-1][0] + 10000, ''))
        h_list = []
        m_list = []
        s_list = []
        ms_list = []

        for d in self.data:
            time = d[0]
            h_list.append(time // 3600000)
            time %= 3600000
            m_list.append(time // 60000)
            time %= 60000
            s_list.append(time // 1000)
            ms_list.append(time % 1000)
        self.data.pop()
        h_list.append(h_list[-1])
        m_list.append(m_list[-1])
        s_list.append(s_list[-1])
        ms_list.append(ms_list[-1])
        for i in range(len(self.data)):
            srt += '{}\n{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}\n{}\n'.format(
                i+1, h_list[i], m_list[i], s_list[i], ms_list[i], h_list[i+1], m_list[i+1], s_list[i+1], ms_list[i+1], self.data[i][1])
        return srt

    def to_txt(self):
        txt = ''
        for d in self.data:
            txt += d[1] + '\n'
        return txt
