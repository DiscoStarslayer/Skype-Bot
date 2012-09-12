import random
import Database

class ball:
	def __init__(self):
		self.db = Database.Data()
		self.replies = self.db.ToList('8ball')

	def get(self):
		print("returning 8ball")
		return self.replies[random.randint(0, len(self.replies))]
