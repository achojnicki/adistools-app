import wx
import wx.grid

from exceptions import APIConnException
from constants import PIXEL_TRACKER_DOMAIN

import rumps

class new_pixel_tracker(wx.Frame):
	def __init__(self, root, parent):
		self._root=root
		self._parent=parent

		wx.Frame.__init__(self, self._parent, title="New Pixel Tracker", size=(400,80), style=wx.DEFAULT_FRAME_STYLE)

		self._name_label=wx.StaticText(self, wx.ID_ANY, label="Name")
		self._name_field=wx.TextCtrl(self, wx.ID_ANY)

		self._create_button=wx.Button(self, wx.ID_ANY, label="Create")


		self._sizer=wx.FlexGridSizer(2,2,0)
		self._sizer.Add(self._name_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		self._sizer.Add(self._name_field, 5, wx.EXPAND)
		self._sizer.AddSpacer(1)
		self._sizer.Add(self._create_button, 0, wx.ALIGN_RIGHT)


		self._sizer.AddGrowableCol(1)
		self.SetSizer(self._sizer)

		self.Bind(wx.EVT_CLOSE, self._on_close)
		self.Bind(wx.EVT_BUTTON, self._do_create_pixel_tracker, self._create_button)
		

		self.SetMinSize((400,80))
		self.SetMaxSize((400,80))

	def _on_close(self, event=None):
		self._name_field.SetValue('')

		self.Destroy()
		self._parent.Show()


	def _do_create_pixel_tracker(self, event):
		try:
			result=self._root._api_conn.create_pixel_tracker(self.query)
		
			data=result['data']
			indexes=list(data.keys())

			if result['status']=='Success':
				rumps.notification('adistools',subtitle=result['status'], message=result['message'], sound=True)
				self._on_close()
				self._parent.Show()

		except APIConnException as e:
			rumps.notification('adistools','Error', message=e.message, sound=True)

		
	@property
	def query(self):
		q={
			"pixel_tracker_name":self._name_field.GetValue(),
		}
		return q

class pixel_tracker_page(wx.Panel):
	def __init__(self, root, parent, frame):
		self._root=root
		self._frame=frame

		self._pixel_trackers_page=1
		self._metrics_page=1

		self._new_pixel_tracker_frame=new_pixel_tracker(
			root=self._root,
			parent=self._frame
		)

		self._pixel_trackers={}
		self._pixel_trackers_indexes=[]

		wx.Panel.__init__(self, parent)

		self._toolbar=wx.ToolBar(self, id=wx.ID_ANY, style=wx.TB_HORIZONTAL)
		new_icon=wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, (16, 16))
		delete_icon=wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16, 16))
		copy_icon=wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, (16, 16))
		
		self._toolbar.AddTool(1, "New pixel tracker", new_icon, wx.NullBitmap, wx.ITEM_NORMAL)
		self._toolbar.AddTool(2, "Delete pixel tracker", delete_icon, wx.NullBitmap, wx.ITEM_NORMAL)
		self._toolbar.AddTool(3, "Copy pixel tracker to clipboard", copy_icon, wx.NullBitmap, wx.ITEM_NORMAL)
		self._toolbar.Realize()

		self._pixel_trackers_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self._pixel_trackers_list.InsertColumn(0, "Pixel Tracker", width=400)

		self._metrics_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self._metrics_list.InsertColumn(0, "Datetime", width=150)
		self._metrics_list.InsertColumn(1, "IP Address", width=300)
		self._metrics_list.InsertColumn(2, "User Agent", width=1300)

		
		self._pixel_trackers_list_previous_page_button=wx.Button(self, wx.ID_ANY, "<", size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)
		self._pixel_trackers_list_next_page_button=wx.Button(self, wx.ID_ANY, ">", size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)
		self._pixel_trackers_list_previous_page_button.Disable()

		#self._metrics_previous_page_button=wx.Button(self, wx.ID_ANY, "<")
		#self._metrics_next_page_button=wx.Button(self, wx.ID_ANY, ">")
		#self._metrics_previous_page_button.Disable()


		self._pixel_trackers_list_navi_sizer=wx.BoxSizer(wx.HORIZONTAL)
		self._pixel_trackers_list_navi_sizer.Add(self._pixel_trackers_list_previous_page_button)
		self._pixel_trackers_list_navi_sizer.Add(self._pixel_trackers_list_next_page_button)
		
		#self._metrics_navi_sizer=wx.BoxSizer(wx.HORIZONTAL)
		#self._metrics_navi_sizer.Add(self._metrics_previous_page_button)
		#self._metrics_navi_sizer.Add(self._metrics_next_page_button)



		self._left_sizer=wx.BoxSizer(wx.VERTICAL)
		self._left_sizer.Add(self._pixel_trackers_list, 1, wx.EXPAND)
		self._left_sizer.Add(self._pixel_trackers_list_navi_sizer, 0, wx.ALIGN_RIGHT)

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

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_pixel_trackers_select, self._pixel_trackers_list)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_pixel_trackers_deselect, self._pixel_trackers_list)
		self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._pixel_trackers_list)
		self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._metrics_list)
		self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self._veto_event, self._pixel_trackers_list)
		self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self._veto_event, self._metrics_list)



		self.Bind(wx.EVT_BUTTON, self._previous_pixel_trackers_page, self._pixel_trackers_list_previous_page_button)
		self.Bind(wx.EVT_BUTTON, self._next_pixel_trackers_page, self._pixel_trackers_list_next_page_button)


		self.Bind(wx.EVT_TOOL, self._do_show_new_pixel_tracker_frame, id=1)
		self.Bind(wx.EVT_TOOL, self._do_delete_pixel_tracker, id=2)
		self.Bind(wx.EVT_TOOL, self._do_copy_pixel_tracker_to_clipboard, id=3)

		self._frame._on_load.append(self._do_propagate_pixel_trackers)


	def _veto_event(self, event):
		event.Veto()

	def _on_sort(self, event):
		self.Layout()
		self.Update()

	def _do_copy_pixel_tracker_to_clipboard(self, event):
		if self._pixel_trackers_list.GetFocusedItem() == -1:
			rumps.notification('adistools','Warning', message='Select pixel tracker to copy.', sound=True)
			return False
		
		pixel_tracker_uuid=self._pixel_trackers[self._pixel_trackers_indexes[self._pixel_trackers_list.GetFocusedItem()]]['pixel_tracker_uuid']
		data=wx.TextDataObject()
		data.SetText(PIXEL_TRACKER_DOMAIN.format(pixel_tracker_uuid=pixel_tracker_uuid))
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(data)
			wx.TheClipboard.Flush()
			wx.TheClipboard.Close()


	def _do_delete_pixel_tracker(self, event):
		if self._pixel_trackers_list.GetFocusedItem() == -1:
				rumps.notification('adistools','Warning', message='Select pixel tracker to delete.', sound=True)
				return False
		try:

			deleted_url_status=self._root._api_conn.delete_pixel_tracker(self._metrics_query)
			
			rumps.notification("adistools",deleted_url_status['status'],deleted_url_status['message'])
			self._do_propagate_pixel_trackers()
		
		except APIConnException as e:
			rumps.notification('adistools','Error', message=e.message, sound=True)


	def _do_show_new_pixel_tracker_frame(self, event):
		self._new_pixel_tracker_frame.Show()
		self._frame.Hide()

	def _do_propagate_pixel_trackers(self, event=None):
		self._pixel_trackers=self._root._api_conn.get_pixel_trackers(self._pixel_trackers_query)
		self._pixel_trackers_indexes=list(self._pixel_trackers.keys())
		
		self._pixel_trackers_list.DeleteAllItems()
		
		for a in self._pixel_trackers:
			self._pixel_trackers_list.InsertItem(
				self._pixel_trackers_indexes.index(a),
				self._pixel_trackers[a]['pixel_tracker_name']
			)
		self.Layout()
		self.Update()

	def _do_propagate_metrics(self):
		metrics=self._root._api_conn.get_pixel_tracker_metrics(self._metrics_query)
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

	def _on_pixel_trackers_select(self, event):
		self._do_propagate_metrics()

	def _on_pixel_trackers_deselect(self,event):
		self._metrics_list.DeleteAllItems()


	def _change_pixel_trackers_page(self):
		self._do_propagate_pixel_trackers()
		if self._pixel_trackers==1:
			self._pixel_trackers_previous_page_button.Disable()
		else:
			self._pixel_trackers_previous_page_button.Enable()

	def _next_pixel_trackers_page(self, event):
		self._pixel_trackers_page+=1
		self._change_pixel_trackers_page()

	def _previous_pixel_trackers_page(self, event):
		self._pixel_trackers_page-=1
		self._change_pixel_trackers_page()

	@property
	def _pixel_trackers_query(self):
		q={
			"page": self._pixel_trackers_page
		}
		return q

	@property
	def _metrics_query(self):
		q={
			"pixel_tracker_uuid":self._pixel_trackers[self._pixel_trackers_indexes[self._pixel_trackers_list.GetFocusedItem()]]['pixel_tracker_uuid'],
		}
		return q	
	