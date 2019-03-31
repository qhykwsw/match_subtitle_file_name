# 本脚本针对电影和美剧字幕批量修改
# 默认每一部电影和每一季的剧集与其字幕需要放在不同的单独文件夹下

import re
import os
import sys
import time

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, qApp)
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

	def __init__(self):
		self.pttn = re.compile(r'[s]\d+[e]\d+')
		self.match_num = 0
		self.no_match_num = 0
		self.has_match_num = 0
		super().__init__()
		
		self.initUI()
		
	def initUI(self):

		self.textEdit = QTextEdit()
		self.setCentralWidget(self.textEdit)
		self.statusBar()

		# 打开文件夹
		openFile = QAction(QIcon('icon/open.png'), 'Open dir', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Open dir')
		openFile.triggered.connect(self.showDialog)

		# 退出程序
		exitAction = QAction(QIcon('icon/exit.png'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit')
		exitAction.triggered.connect(qApp.quit)

		# 设置菜单栏
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openFile)
		fileMenu.addAction(exitAction)

		# 设置窗口大小、位置及名称
		self.resize(1000, 618)
		self.center()
		self.setWindowTitle('字幕匹配')
		self.show()
	
	def center(self):

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def showDialog(self):

		top = QFileDialog.getExistingDirectory(self, 'Open dir', 'C:\\Files')
		start = time.time()
		self.matchSubtitle(top)
		self.textEdit.append(f"原本有{self.has_match_num}个字幕已经匹配，本次有{self.match_num}个字幕完成匹配, 仍有{self.no_match_num}个字幕未匹配。")
		end = time.time()
		self.textEdit.append(f"共耗时{round(end-start, 5)}秒")
		self.match_num = 0
		self.no_match_num = 0
		self.has_match_num = 0

	def matchSubtitle(self, top):

		for path, dirlist, filelist in os.walk(top):
			videos = [name for name in filelist if name.endswith(('.mkv','.mp4','.avi','.rmvb','.rm','.flv','.3gp'))]
			subtitles = [name for name in filelist if name.endswith(('.ass','.srt','.sup','.ssa'))]
			# 如果只有一个字幕文件，则默认为电影，直接匹配同文件夹下的视频文件
			if len(subtitles) == len(videos) == 1:
				subtitle = subtitles[0]
				video = videos[0]
				if os.path.splitext(subtitle)[0] == os.path.splitext(video)[0]:
					self.has_match_num += 1
					continue
				else:
					subtitle_oldname = os.path.join(path, subtitle)
					subtitle_newname = os.path.join(path, os.path.splitext(video)[0] + os.path.splitext(subtitle)[1])
					os.rename(subtitle_oldname, subtitle_newname)
					self.textEdit.append(f"{subtitle_oldname}匹配成功。")
					self.match_num += 1
			else:
				for subtitle in subtitles:
					# 提取出包含季数与集数的字符串
					try:
						episode = re.search(self.pttn, subtitle.lower()).group()
					except AttributeError as e:
						self.textEdit.append(f"'{os.path.join(path, subtitle)}'中未找到匹配季数与集数的字符串。")
						break
					for video in videos:
						# print(subtitle,video)
						# 尝试匹配对应的video
						if episode in video.lower():
							if os.path.splitext(subtitle)[0] == os.path.splitext(video)[0]:
								self.has_match_num += 1
								break
							else:
								subtitle_oldname = os.path.join(path, subtitle)
								subtitle_newname = os.path.join(path, os.path.splitext(video)[0] + os.path.splitext(subtitle)[1])
								# 将字幕重命名
								os.rename(subtitle_oldname, subtitle_newname)
								self.textEdit.append(f"{subtitle_oldname}匹配成功。")
								self.match_num += 1
								break
					else:
						self.textEdit.append(f"'{os.path.join(path, subtitle)}'未找到与之匹配的视频文件。")
						self.no_match_num += 1

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
