from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

def index(request):
	file = open('index.html', 'r')
	data = file.read()
	file.close()
	
	return Response(data)

def aboutme(request):
	file = open('about/aboutme.html', 'r')
	data = file.read()
	file.close()
	
	return Response(data)

class middleware(object):

	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		htmlFile = self.app(environ, start_response)[0].decode()
		topStr = '<div class=''top''>Middleware TOP</div>'
		botStr = '<div class=''bottom''>Middleware BOTTOM</div>'
		b = '<body>'
		cb = '</body>'
		headHtml, bodyHtml = htmlFile.split(b)
		data, endHtml = bodyHtml.split(cb)
		data = b + topStr + data + botStr + cb
		return [headHtml.encode('utf8') + data.encode('utf8') + endHtml.encode('utf8')]		


if __name__ == '__main__':
	config = Configurator()
	config.add_route('default', '/')
	config.add_view(index, route_name = 'default')
	config.add_route('index', '/index.html')
	config.add_view(index, route_name = 'index')
	config.add_route('aboutme', '/about/aboutme.html')
	config.add_view(aboutme, route_name = 'aboutme')
	
	app = config.make_wsgi_app()
	wsgi_app = middleware(app)
	
	server = make_server('0.0.0.0', 8000, wsgi_app)
	server.serve_forever()