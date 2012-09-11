

class Data:
	'''Class to write dynamicly created commands to a file'''

	def ToList(self, fileName):
		item = open(fileName)
		lines = item.readlines()
		for i in range(len(lines)):
			lines[i] = lines[i].replace("\a", "\n").strip()
		return lines
		item.close()
	
	def ToDict(self, fileName):
		lines = self.ToList(fileName)
		ret = dict()
		for i in lines:
			tokens = i.split(' ')
			string = ''
			for i in range(len(tokens)-1):
				string = string + tokens[i+1] + ' '
			ret[tokens[0]] = string.strip()
		return ret
		
	def SaveDict(self, writeDict, fileName):
		db = open(fileName, 'w')
		for i in writeDict:
			temp = writeDict[i].replace("\n", "\a")
			string = i + ' ' + temp + '\n'
			db.write(string)
		db.close()


