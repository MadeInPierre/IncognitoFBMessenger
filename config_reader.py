class ConfigReader():
	def __init__(self):
		self.configfile = ".config"

	def getFacebookCredentials(self):
		config = self.readConfig()
		email = config["fbemail"]
		password = config["fbpassword"]
		return email, password

	def readConfig(self):
		config_dict = {}

		with open(self.configfile) as f:
		    content = f.readlines()
		content = [x.strip() for x in content] #remove whitespaces and \n

		for line in content:
			if line[0] != "#": #ignore comments
				splitted = line.split("=")
				config_dict[splitted[0]] = splitted[1]

		return config_dict

'''
#.config file template :
# Facebook login needed (NO SPACES)
fbemail=youremailhere
fbpassword=yourpasswordhere
'''