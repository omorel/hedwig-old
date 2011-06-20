from hedwig.models import DBSession
from hedwig.models import User

def my_view(request):
	dbsession = DBSession()
	root = User(u'olivier')
	root.load()
	return {'root':root, 'project':'hedwig'}

