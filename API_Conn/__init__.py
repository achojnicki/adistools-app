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
		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def get_short_urls(self, query):
		conn=requests.post(
			API_URL+ "/shortened_urls",
			self._append_session(query)
			)
		resp=conn.json()

		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e
	
	def get_short_url_metrics(self, query):
		conn=requests.post(
			API_URL+ "/shortened_url_metrics",
			self._append_session(query)
			)
		resp=conn.json()

		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def create_short_url(self, query):
		conn=requests.post(
			API_URL+ "/create_short_url",
			self._append_session(query)
			)
		resp=conn.json()
		print(resp)

		if resp['status']=='Success':
			return resp
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e
	
	def delete_short_url(self, query):
		conn=requests.post(
			API_URL+ "/delete_short_url",
			self._append_session(query)
			)
		resp=conn.json()
		print(resp)

		if resp['status']=='Success':
			return resp
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e
	
	def get_pixel_trackers(self, query):
		conn=requests.post(
			API_URL+ "/pixel_trackers",
			self._append_session(query)
			)
		resp=conn.json()

		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def get_pixel_tracker_metrics(self, query):
		conn=requests.post(
			API_URL+ "/pixel_tracker_metrics",
			self._append_session(query)
			)
		resp=conn.json()

		if resp['status']=='Success':
			return resp['data']
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def create_pixel_tracker(self, query):
		conn=requests.post(
			API_URL+ "/create_pixel_tracker",
			self._append_session(query)
			)
		resp=conn.json()
		print(resp)

		if resp['status']=='Success':
			return resp
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e

	def delete_pixel_tracker(self, query):
		conn=requests.post(
			API_URL+ "/delete_pixel_tracker",
			self._append_session(query)
			)
		resp=conn.json()
		print(resp)

		if resp['status']=='Success':
			return resp
		else:
			e=APIConnException()
			e.message=resp['message']
			raise e


	@property
	def session_uuid(self):
		return self._session_uuid