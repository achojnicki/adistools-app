from Login import Login
from API_Conn import API_Conn
from .Pages.Logs_Page import Logs_Page

from sys import exit

import wx
import rumps



class Adistools_Gui(wx.Frame):
	def __init__(self, root):
		self._root=root
		wx.Frame.__init__(self, None, title="adistools", size=(1500,810), style=wx.DEFAULT_FRAME_STYLE)

		self._notebook=wx.Notebook(self)

		self._logs_page=Logs_Page(self._root, self._notebook, self)

		self._notebook.AddPage(self._logs_page, "Logs")

		self.Bind(wx.EVT_CLOSE, self._on_close)

	def _on_close(self, event):
		exit(0)

class adistools:
	def __init__(self):
		self._app=wx.App()
		
		self._api_conn=API_Conn(self)
		self._adistools_gui=Adistools_Gui(self)
		self._login=Login(self)


	def start(self):
		self._login.Show()


		self._app.MainLoop()
		

class AT(rumps.App):
    def __init__(self):
        super(AT, self).__init__("AT")
        self.menu = ["Show adistools", None]


    @rumps.clicked("Show adistools")
    def sayhi(self, _):
        rumps.notification("", None, "hi!!1")
