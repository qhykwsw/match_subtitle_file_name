# 本脚本仅针对美剧字幕批量修改
# 默认每一季的剧集需要放在不同的单独文件夹下
import re
import os
		
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, qApp)
from PyQt5.QtGui import QIcon
import sys

class Example(QMainWindow):
	
	def __init__(self):
		self.pttn = re.compile(r'[s]\d+[e]\d+')
		self.match_num = 0
		self.no_match_num = 0
		super().__init__()
		
		self.initUI()
		
	def initUI(self):      

		self.textEdit = QTextEdit()
		self.setCentralWidget(self.textEdit)
		self.statusBar()

		# 打开文件夹
		openFile = QAction(QIcon('open.png'), 'Open dir', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Open dir')
		openFile.triggered.connect(self.showDialog)

		# 退出程序
		exitAction = QAction(QIcon('exit.png'), 'Exit', self)      
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit')
		exitAction.triggered.connect(qApp.quit)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openFile)
		fileMenu.addAction(exitAction)

		self.resize(1000, 400)
		self.center()
		self.setWindowTitle('Dir dialog')
		self.show()
	
	def center(self):

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def showDialog(self):

		top = QFileDialog.getExistingDirectory(self, 'Open dir', '/home')
		self.matchSubtitle(top)
		self.textEdit.append(f"共有{self.match_num}个字幕完成匹配, 仍有{self.no_match_num}个字幕未匹配")
	
	def matchSubtitle(self, top):

		for path, dirlist, filelist in os.walk(top):
			videos = [name for name in filelist if name.endswith(('mkv','mp4','avi'))]
			subtitles = [name for name in filelist if name.endswith(('ass','srt','sup','ssa'))]
			for subtitle in subtitles:
				# 提取出包含季数与集数的字符串
				try:
					episode = re.search(self.pttn, subtitle.lower()).group()
				except AttributeError as e:
					self.textEdit.append(f"'{os.path.join(path, subtitle)}'中未找到匹配季数与集数的字符串")
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
							self.match_num += 1
							break
				else:
					self.textEdit.append(f"'{os.path.join(path, subtitle)}'未找到与之匹配的视频文件")
					self.no_match_num += 1

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())