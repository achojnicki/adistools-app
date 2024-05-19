from Login import Login
from API_Conn import API_Conn

from .pages.logs_page import logs_page
from .pages.url_shortener_page import url_shortener_page
from .pages.pixel_tracker_page import pixel_tracker_page


from threading import Thread
from sys import exit
from time import sleep
from AppKit import NSWorkspace, NSApplicationActivateAllWindows

import wx
import rumps


class adistools_wx(wx.Frame):
	def __init__(self, root):
		self._on_load=[]
		self._root=root
		wx.Frame.__init__(self, None, title="adis.tools", size=(1500,890), style=wx.DEFAULT_FRAME_STYLE)

		self._notebook=wx.Notebook(self)

		self._logs_page=logs_page(self._root, self._notebook, self)
		self._url_shortener_page=url_shortener_page(self._root, self._notebook, self)
		self._pixel_tracker_page=pixel_tracker_page(self._root, self._notebook, self)

		self._notebook.AddPage(self._logs_page, "Logs")
		self._notebook.AddPage(self._url_shortener_page, "Short Links")
		self._notebook.AddPage(self._pixel_tracker_page, "Pixel Trackers")

		#self.Bind(wx.EVT_CLOSE, self._on_close)

		self.Bind(wx.EVT_SHOW, self._do_on_load)

	def _do_on_load(self, event):
		for a in self._on_load:
			a()

	def _on_close(self, event):
		exit(0)

class adistools_rumps(rumps.App):
	def __init__(self, root):
		self._root=root

		super(adistools_rumps, self).__init__("AT")
		self.menu=['Show']

	@rumps.clicked('Show')
	def show(self, event):
		if self._root._logged_in:
			self._root._adistools_wx.Show()
			self._switch_to_app()

		else:
			rumps.notification('adistools',subtitle=None, message='You need to login first.')
			self._root._login.Show()

	def _switch_to_app(self):
		for item in NSWorkspace.sharedWorkspace().runningApplications():
			if item.localizedName()=='adistools':
				item.activateWithOptions_(NSApplicationActivateAllWindows)

class adistools:
	def __init__(self):
		self._active=True
		self._logged_in=False

		self._app=wx.App()
		self._api_conn=API_Conn(self)
		
		self._adistools_wx=adistools_wx(self)
		self._adistools_rumps=adistools_rumps(self)
		self._login=Login(self)

		self._wx_thread=Thread(
			target=self._app.MainLoop,
			args=()
			)



	def start(self):
		#self._wx_thread.start()
		self._login.Show()

		self._adistools_rumps.run()


		#self._login.Show()
		#self._app.MainLoop()
