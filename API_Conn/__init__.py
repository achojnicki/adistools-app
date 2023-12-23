from exceptions import APIConnException
from constants import API_URL

import requests

class API_Conn:
	_session_uuid=None
	def __init__(self, parent):
		self._parent=parent

	def _append_session(self, data):
		data['session_uuid']=self._session_uuid
		return data
	def login(self, cred):
		conn=requests.post(
			API_URL + "/login",
			cred)
		resp=conn.json()
		print(resp)
		if resp['status']=='Success':
			self._session_uuid=resp['data']['session_uuid']
			return True
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def get_logs(self, query):
		conn=requests.post(
			API_URL + "/logs",
			self._append_session(query)
			)
		resp=conn.json()
		print(resp)
		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	@property
	def session_uuid(self):
		return self._session_uuid