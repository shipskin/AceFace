'''
Module Description:
Generates a dictionary called 'namedb'
namedb is a dictionary of names, that include a subdictionary with -
total detection count hitcount and inital detection time {hits, time}


'''



class TagGenerator(object):

    def __init__(self):
        self.namedb = dict()

    def addAthlete(self,name, time):
        if name in self.namedb:
		    # add hit to db.name
            self.namedb[name]['hits'] += 1
        else:
		    # setup db with tags and initial time detected
		    self.namedb[name] = {'hits':0,'time':int(time)}
