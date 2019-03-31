# 本脚本针对电影和美剧字幕批量修改
# 默认每一部电影和每一季的剧集与其字幕需要放在不同的单独文件夹下

import re
import os

top = "C:\\Files\\Videos"
# top =  "E:\\视频"

pttn = re.compile(r'[s]\d+[e]\d+')

match_num = 0
no_match_num = 0

for path, dirlist, filelist in os.walk(top):
	videos = [name for name in filelist if name.endswith(('mkv','mp4','avi','rmvb','rm','flv','3gp'))]
	subtitles = [name for name in filelist if name.endswith(('ass','srt','sup','ssa'))]
	# 如果只有一个字幕文件，则默认为电影，直接匹配同文件夹下的视频文件
	if len(subtitles) == len(videos) == 1:
		subtitle = subtitles[0]
		video = videos[0]
		if os.path.splitext(subtitle)[0] == os.path.splitext(video)[0]:
			continue
		else:
			subtitle_oldname = os.path.join(path, subtitle)
			subtitle_newname = os.path.join(path, os.path.splitext(video)[0] + os.path.splitext(subtitle)[1])
			os.rename(subtitle_oldname, subtitle_newname)
			match_num += 1
	else:
		for subtitle in subtitles:
			# 提取出包含季数与集数的字符串
			try:
				episode = re.search(pttn, subtitle.lower()).group()
			except AttributeError as e:
				print(f"'{os.path.join(path, subtitle)}'中未找到匹配季数与集数的字符串")
				break
			for video in videos:
				# print(subtitle,video)
				# 尝试匹配对应的video
				if episode in video.lower():
					if os.path.splitext(subtitle)[0] == os.path.splitext(video)[0]:
						break
					else:
						subtitle_oldname = os.path.join(path, subtitle)
						subtitle_newname = os.path.join(path, os.path.splitext(video)[0] + os.path.splitext(subtitle)[1])
						# 将字幕重命名
						os.rename(subtitle_oldname, subtitle_newname)
						match_num += 1
						break
			else:
				print(f"'{os.path.join(path, subtitle)}'未找到与之匹配的视频文件")
				no_match_num += 1

print(f"共有{match_num}个字幕完成匹配, 仍有{no_match_num}个字幕未匹配")