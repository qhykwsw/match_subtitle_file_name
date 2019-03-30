# 本脚本仅针对美剧字幕批量修改
import re
import os

# top = "C:\\Files\\Videos"
top =  "E:\\视频"

pttn = re.compile(r'[s]\d+[e]\d+')

for path, dirlist, filelist in os.walk(top):
	videos = [name for name in filelist if name.endswith(('mkv','mp4','avi'))]
	subtitles = [name for name in filelist if name.endswith(('ass','srt','sup','ssa'))]
	for subtitle in subtitles:
		# 提取出包含季数与集数的字符串
		try:
			episode = re.search(pttn, subtitle.lower()).group()
		except AttributeError as e:
			print(subtitle)
			break
		for video in videos:
			# 尝试匹配对应的video
			if episode in video.lower():
				subtitle_oldname = os.path.join(path, subtitle)
				subtitle_newname = os.path.join(path, video[:-3]+subtitle[-3:])
				# 将字幕重命名
				os.rename(subtitle_oldname, subtitle_newname)
				break

