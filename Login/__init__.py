from sys import exit

import wx


class Login(wx.Frame):
	def __init__(self, root):
		self._root=root
		wx.Frame.__init__(self, None, title="Log in", size=(200,75), style=wx.DEFAULT_FRAME_STYLE)

		self._login_form=wx.BoxSizer(wx.VERTICAL)
		self._login_field=wx.TextCtrl(
			self,
			style=wx.TE_PROCESS_ENTER,
			)

		self._password_field=wx.TextCtrl(
			self,
			style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER,
			)

		self._login_form.Add(self._login_field, 0, wx.EXPAND)
		self._login_form.Add(self._password_field, 0, wx.EXPAND)
		self.SetSizer(self._login_form)

		self._login_field.Bind(wx.EVT_TEXT_ENTER, self.do_login)
		self._password_field.Bind(wx.EVT_TEXT_ENTER, self.do_login)

		self.Bind(wx.EVT_CLOSE, self._on_close)
	def _on_close(self, event):
		exit(0)

	def do_login(self, event):
		try:
			r=self._root._api_conn.login(self.cred)
			if r:
				wx.MessageBox('Login Successful','Success')
				self.Destroy()
				self._root._adistools_gui.Show()

		except Exception as e:
			wx.MessageBox(e.message, 'Error')

	@property
	def cred(self):
		creds={
			"user_email":self._login_field.GetValue(),
			"user_password": self._password_field.GetValue()
			}
		return creds

