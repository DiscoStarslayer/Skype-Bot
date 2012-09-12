import random
import Database

class excuse:
	
	def __init__(self):
		self.db = Database.Data()
		self.excuses = self.db.ToList('excuses')
		self.count = 0
		random.shuffle(self.excuses)

	def get(self):
		self.count = (self.count + 1) % len(self.excuses)
		return self.excuses[self.count]
