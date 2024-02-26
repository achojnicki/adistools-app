import wx
import wx.grid

from exceptions import APIConnException
from constants import SHORT_URL_DOMAIN

import rumps

class new_short_url(wx.Frame):
	def __init__(self, root, parent):
		self._root=root
		self._parent=parent

		wx.Frame.__init__(self, self._parent, title="New Short URL", size=(400,100), style=wx.DEFAULT_FRAME_STYLE)

		self._query_label=wx.StaticText(self, wx.ID_ANY, label="Query")
		self._long_url_label=wx.StaticText(self, wx.ID_ANY, label="Long URL")

		self._query_field=wx.TextCtrl(self, wx.ID_ANY)
		self._long_url_field=wx.TextCtrl(self, wx.ID_ANY)

		self._create_button=wx.Button(self, wx.ID_ANY, label="Create")


		self._sizer=wx.FlexGridSizer(2,2,0)
		self._sizer.Add(self._query_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		self._sizer.Add(self._query_field, 5, wx.EXPAND)
		self._sizer.Add(self._long_url_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		self._sizer.Add(self._long_url_field, 5, wx.EXPAND)
		self._sizer.AddSpacer(1)
		self._sizer.Add(self._create_button, 0, wx.ALIGN_RIGHT)


		self._sizer.AddGrowableCol(1)
		self.SetSizer(self._sizer)

		self.Bind(wx.EVT_CLOSE, self._on_close)
		self.Bind(wx.EVT_BUTTON, self._do_create_url_shortener, self._create_button)
		

		self.SetMinSize((400,100))
		self.SetMaxSize((400,100))

	def _on_close(self, event=None):
		self._query_field.SetValue('')
		self._long_url_field.SetValue('')

		self.Destroy()
		self._parent.Show()


	def _do_create_url_shortener(self, event):
		try:
			result=self._root._api_conn.create_short_url(self.query)
		
			data=result['data']
			indexes=list(data.keys())

			if result['status']=='Success':
				url=SHORT_URL_DOMAIN+data[indexes[0]]['redirection_query']
				rumps.notification('adistools',subtitle=result['message'], message=url, sound=True)
				self._on_close()
				self._parent.Show()

		except APIConnException as e:
			rumps.notification('adistools','Error', message=e.message, sound=True)

		
	@property
	def query(self):
		q={
			"redirection_query":self._query_field.GetValue(),
			"redirection_url":self._long_url_field.GetValue(),
		}
		return q

class url_shortener_page(wx.Panel):
	def __init__(self, root, parent, frame):
		self._root=root
		self._frame=frame

		self._urls_page=1
		self._metrics_page=1

		self._new_short_url_frame=new_short_url(
			root=self._root,
			parent=self._frame
		)

		self._short_urls={}
		self._short_urls_indexes=[]

		wx.Panel.__init__(self, parent)

		self._toolbar=wx.ToolBar(self, id=wx.ID_ANY, style=wx.TB_HORIZONTAL)
		new_icon=wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, (16, 16))
		delete_icon=wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16, 16))
		self._toolbar.AddTool(1, "New", new_icon, wx.NullBitmap, wx.ITEM_NORMAL, 'New', "New short URL", None)
		self._toolbar.AddTool(2, "delete", delete_icon, wx.NullBitmap, wx.ITEM_NORMAL, "Delete", "Delete short URL", None)
		self._toolbar.Realize()

		self._urls_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self._urls_list.InsertColumn(0, "Short Link", width=400)

		self._metrics_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self._metrics_list.InsertColumn(0, "Datetime", width=150)
		self._metrics_list.InsertColumn(1, "IP Address", width=300)
		self._metrics_list.InsertColumn(2, "User Agent", width=1300)

		
		self._urls_list_previous_page_button=wx.Button(self, wx.ID_ANY, "<", size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)
		self._urls_list_next_page_button=wx.Button(self, wx.ID_ANY, ">", size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)
		self._urls_list_previous_page_button.Disable()

		#self._metrics_previous_page_button=wx.Button(self, wx.ID_ANY, "<")
		#self._metrics_next_page_button=wx.Button(self, wx.ID_ANY, ">")
		#self._metrics_previous_page_button.Disable()


		self._urls_list_navi_sizer=wx.BoxSizer(wx.HORIZONTAL)
		self._urls_list_navi_sizer.Add(self._urls_list_previous_page_button)
		self._urls_list_navi_sizer.Add(self._urls_list_next_page_button)
		
		#self._metrics_navi_sizer=wx.BoxSizer(wx.HORIZONTAL)
		#self._metrics_navi_sizer.Add(self._metrics_previous_page_button)
		#self._metrics_navi_sizer.Add(self._metrics_next_page_button)



		self._left_sizer=wx.BoxSizer(wx.VERTICAL)
		self._left_sizer.Add(self._urls_list, 1, wx.EXPAND)
		self._left_sizer.Add(self._urls_list_navi_sizer, 0, wx.ALIGN_RIGHT)

		self._right_sizer=wx.BoxSizer(wx.VERTICAL)
		self._right_sizer.Add(self._metrics_list, 1, wx.EXPAND)
		#self._right_sizer.Add(self._metrics_navi_sizer, 0, wx.ALIGN_RIGHT)

		self._container_sizer=wx.BoxSizer(wx.HORIZONTAL)
		self._container_sizer.Add(self._left_sizer,2, wx.EXPAND)
		self._container_sizer.Add(self._right_sizer, 6, wx.EXPAND)

		self._main_sizer=wx.BoxSizer(wx.VERTICAL)
		self._main_sizer.Add(self._toolbar, 0)
		self._main_sizer.Add(self._container_sizer, 1, wx.EXPAND)


		self.SetSizer(self._main_sizer)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_short_url_select, self._urls_list)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_short_url_deselect, self._urls_list)

		self.Bind(wx.EVT_BUTTON, self._previous_urls_page, self._urls_list_previous_page_button)
		self.Bind(wx.EVT_BUTTON, self._next_urls_page, self._urls_list_next_page_button)
		self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._urls_list)
		self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._metrics_list)

		self.Bind(wx.EVT_TOOL, self._do_show_new_short_url_frame, id=1)
		self.Bind(wx.EVT_TOOL, self._do_delete_short_url, id=2)

		
		self._frame._on_load.append(self._do_propagate_short_urls)

	def _on_sort(self, event):
		self.Layout()
		self.Update()

	def _do_delete_short_url(self, event):
		if self._urls_list.GetFocusedItem() == -1:
				rumps.notification('adistools','Warning', message='Select short URL to delete.', sound=True)
				return False
		try:

			deleted_url_status=self._root._api_conn.delete_short_url(self._metrics_query)
			
			rumps.notification("adistools",deleted_url_status['status'],deleted_url_status['message'])
			self._do_propagate_short_urls()
		
		except APIConnException as e:
			rumps.notification('adistools','Error', message=e.message, sound=True)


	def _do_show_new_short_url_frame(self, event):
		self._new_short_url_frame.Show()
		self._frame.Hide()

	def _do_propagate_short_urls(self, event=None):
		self._short_urls=self._root._api_conn.get_short_urls(self._urls_query)
		self._short_urls_indexes=list(self._short_urls.keys())
		
		self._urls_list.DeleteAllItems()
		
		for a in self._short_urls:
			self._urls_list.InsertItem(
				self._short_urls_indexes.index(a),
				self._short_urls[a]['redirection_query']
			)
		self.Layout()
		self.Update()

	def _do_propagate_metrics(self):
		metrics=self._root._api_conn.get_short_url_metrics(self._metrics_query)
		indexes=list(metrics.keys())

		self._metrics_list.DeleteAllItems()

		for item in metrics:
			for metric in metrics[item]:
				self._metrics_list.InsertItem(
					metrics[item].index(metric),
					metric['time']['strtime']
					)

				self._metrics_list.SetItem(
					metrics[item].index(metric),
					1,
					metric['client_details']['remote_addr']
					)

				self._metrics_list.SetItem(
					metrics[item].index(metric),
					2,
					metric['client_details']['user_agent']
					)

		self.Layout()
		self.Update()

	def _on_short_url_select(self, event):
		self._do_propagate_metrics()

	def _on_short_url_deselect(self,event):
		self._metrics_list.DeleteAllItems()


	def _change_urls_page(self):
		self._do_propagate_short_urls()
		if self._urls_page==1:
			self._urls_list_previous_page_button.Disable()
		else:
			self._urls_list_previous_page_button.Enable()

	def _next_urls_page(self, event):
		self._urls_page+=1
		self._change_urls_page()

	def _previous_urls_page(self, event):
		self._urls_page-=1
		self._change_urls_page()

	@property
	def _urls_query(self):
		q={
			"page": self._urls_page
		}
		return q

	@property
	def _metrics_query(self):
		q={
			"redirection_uuid":self._short_urls[self._short_urls_indexes[self._urls_list.GetFocusedItem()]]['redirection_uuid'],
		}
		return q	
	