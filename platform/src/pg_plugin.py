import inspect
from pg_pool import PostgresConnectionPool

from bottle import HTTPResponse, HTTPError

class PGPlugin(object):
    def __init__(self, *args, **kwargs):
    	self.keyword = kwargs.pop('keyword', 'pool')
	self.pool = PostgresConnectionPool(*args, **kwargs)

    def setup(self, app):
        for other in app.plugins:
	    if not isinstance(other, PGPlugin):
	        continue
	    if other.keyword == self.keyword:
	        raise PluginError("Keyword conflict in PGPlugin")

    def apply(self, callback, context):
        if self.keyword not in inspect.getargspec(context['callback'])[0]:
	    return callback

	def wrapper(*args, **kwargs):
	        kwargs[self.keyword] = self.pool
		return callback(*args, **kwargs)
	
	return wrapper

