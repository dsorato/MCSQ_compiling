import sys, os
import credentials as creds
from sqlalchemy import create_engine

class DBConnection(object):
	def __init__(self):
		self.connection_string = "postgres://"+creds.PGUSER+":"+creds.PGPASSWORD+"@"+ creds.PGHOST +":5432"

	def connect(self):
		db = create_engine(self.connection_string)
		print("Connected to ESS database!")

		return db

	def disconnect(self, connection, cursor):
		if(connection):
			cursor.close()
			connection.close()
			print("Diconnected from ESS.")




