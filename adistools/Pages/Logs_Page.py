import wx
import wx.grid

colors={
	"DEBUG": wx.Colour(169,169,169),
	"ERROR": wx.Colour(139, 0, 0),
	"FATAL": wx.Colour(240, 0, 0),
	"WARNING": wx.Colour(180, 180,0),
	"SUCCESS":wx.Colour(1, 150, 32),

}

class logs_page(wx.Panel):
	def __init__(self, root, parent, frame):
		self._root=root
		self._frame=frame
		self._page=1

		wx.Panel.__init__(self, parent)

		self._grid=wx.grid.Grid(self)
		self._grid.CreateGrid(0,9)
		self._grid.EnableEditing(False)

		self._grid.SetColLabelValue(0, "Datetime")
		self._grid.SetColSize(0, 150)

		self._grid.SetColLabelValue(1, "Project Name")
		self._grid.SetColSize(1, 200)

		self._grid.SetColLabelValue(2, "Log Level")
		self._grid.SetColSize(2, 70)

		self._grid.SetColLabelValue(3, "Message")
		self._grid.SetColSize(3, 800)

		self._grid.SetColLabelValue(4, "PID")
		self._grid.SetColSize(4, 50)

		self._grid.SetColLabelValue(5, "PPID")
		self._grid.SetColSize(5, 50)

		self._grid.SetColLabelValue(6, "Line Number")
		self._grid.SetColSize(6, 80)

		self._grid.SetColLabelValue(7, "Function")
		self._grid.SetColSize(7, 200)

		self._grid.SetColLabelValue(8, "File")
		self._grid.SetColSize(8, 900)

		
		self._previous_page_button=wx.Button(self, wx.ID_ANY, "<",size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)
		self._next_page_button=wx.Button(self, wx.ID_ANY, ">",size=(50, 15), style=wx.BU_EXACTFIT|wx.BORDER_NONE)

		self._previous_page_button.Disable()


		self._project_name_field=wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, size=(150, -1))
		self._project_name_field.SetHint('Project Name')

		self._log_level_field=wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER, size=(150, -1))
		self._log_level_field.SetHint('Log Level')

		self._filter_button=wx.Button(self, wx.ID_ANY, "Filter")


		self._page_navi_sizer=wx.BoxSizer(wx.HORIZONTAL)

		self._page_navi_sizer.Add(self._previous_page_button)
		self._page_navi_sizer.Add(self._next_page_button)


		self._sizer=wx.BoxSizer(wx.VERTICAL)

		self._sizer.Add(self._grid, 1, wx.EXPAND)


		self._right_sizer=wx.BoxSizer(wx.VERTICAL)

		self._right_sizer.Add(self._project_name_field, 1, wx.EXPAND)
		self._right_sizer.Add(self._log_level_field, 1, wx.EXPAND)
		self._right_sizer.Add(self._filter_button, 1, wx.ALIGN_RIGHT)
		self._right_sizer.AddStretchSpacer(1000)
		self._right_sizer.Add(self._page_navi_sizer, 1)


		self._main_sizer=wx.BoxSizer(wx.HORIZONTAL)

		self._main_sizer.Add(self._sizer, 1, wx.EXPAND)
		self._main_sizer.Add(self._right_sizer)

		self.SetSizer(self._main_sizer)

		self._previous_page_button.Bind(wx.EVT_BUTTON, self._previous_page)
		self._next_page_button.Bind(wx.EVT_BUTTON, self._next_page)
		self._filter_button.Bind(wx.EVT_BUTTON, self._filter)


		self._frame._on_load.append(self._do_propagate_logs)


	def _filter(self, event):
		self._page=1
		self._change_page()

	def _do_propagate_logs(self, event=None):
		
		r=self._root._api_conn.get_logs(self.logs_query)
		
		if self._grid.NumberRows>0:
			self._grid.DeleteRows(0, -1)
		self._grid.AppendRows(len(r))
		
		for a in r:
			self._grid.SetCellValue(r.index(a),0,a['strtime'])
			self._grid.SetCellValue(r.index(a),1,a['project_name'])
			self._grid.SetCellValue(r.index(a),2,a['log_level'])
			self._grid.SetCellValue(r.index(a),3,a['message'])
			self._grid.SetCellValue(r.index(a),4,str(a['system']['pid']))
			self._grid.SetCellValue(r.index(a),5,str(a['system']['ppid']))
			self._grid.SetCellValue(r.index(a),6,str(a['caller']['line_number']))
			self._grid.SetCellValue(r.index(a),7,a['caller']['function'])
			self._grid.SetCellValue(r.index(a),8,a['caller']['filename'])


			attr=wx.grid.GridCellAttr()
			font=wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
			attr.SetFont(font)
			self._grid.SetAttr(r.index(a), 2, attr)
			self._grid.SetCellAlignment(r.index(a), 2, wx.ALIGN_CENTER, wx.ALIGN_CENTER)

			if a['log_level'] in colors:
				for x in range(9):
					self._grid.SetCellBackgroundColour(r.index(a), x, colors[a['log_level']])
			
		for a in range(self._grid.GetNumberCols()):
			self._grid.DisableColResize(a)
			
		for a in range(self._grid.GetNumberRows()):
			self._grid.DisableRowResize(a)


	def _change_page(self):
		self._do_propagate_logs()
		if self._page==1:
			self._previous_page_button.Disable()
		else:
			self._previous_page_button.Enable()

	def _next_page(self, event):
		self._page+=1
		self._change_page()

	def _previous_page(self, event):
		self._page-=1
		self._change_page()

	@property
	def logs_query(self):
		q={
			"project_name":self._project_name_field.GetValue(),
			"log_level":self._log_level_field.GetValue(),
			"page":self._page
		}
		return q


		
	