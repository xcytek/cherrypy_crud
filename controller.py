import cherrypy
import database
from jinja2 import Environment, FileSystemLoader, Template
env = Environment(loader=FileSystemLoader('views'))

class Crud :			
	style = """	
	*{
		margin: 0 auto;	
	}

	body{	
		
	}

	footer{
		background-color: #333;
		color: white;
		font-size: 16px;
		padding: 30px 0;
		text-align: center;
	}

	header{
		background-color: #3890FC;
		color: white;
		font-size: 48px;
		padding: 80px 0;
		text-align: center;
	}

	nav{		
		background-color: #000;	
		padding: 10px 0;
		text-align: center;
	}

	nav ul li{
		display: inline-block;
		font-size: 16px;
		padding: 0 25px;
		text-transform: uppercase;			
	}

	nav ul li a{
		color: white;
		text-decoration: none;
	}

	#parrafo{
		width: 900px;
		font-size: 18px;
		text-align: justify;
	}

	#parrafo form{	
		padding: 25px;
		text-align: right;
		width: 400px;
	}

	#parrafo input[type=text]{
		text-align: center;
		width: 70%;
	}

	#parrafo label{
		float: left;
	}

	#parrafo p{
		margin: 10px 0;
	}

	article{
		border-bottom: 1px solid #999;
		padding-left: 35px;
		width: 600px;
	}

	article .nombre{
		font-size: 30px;
	}

	article .edad{
		text-decoration: underline;
	}

	article .pais{
		font-size: 20px;
		font-weight: bold;
	}

	article .email{	
		font-style: italic;
	}


	"""
	@cherrypy.expose
	def index(self, id=None) :
		tmpl = env.get_template('index.html')	
		if database.connect('start_thread') :
			#Modificar y Actualizar
			if id:
				persona_mod = database.get_persona(id)
				do_action = 'actualizar'
				id_field = '<p><input type="hidden" name="id_mod" value="'+str(id)+'" /></p>'
			#Insertar nuevo
			else:
				persona_mod=''
				do_action = 'insertar'
				id_field = ''				

			rec = database.get_records()				

		return tmpl.render(title="Inicio", personas=rec, persona_mod=persona_mod, do_action=do_action, id_field=id_field, style=self.style)

	@cherrypy.expose
	def insertar(self, nombre=None, edad=None, email=None, pais=None) :
		if database.connect('start_thread'):
			p = [nombre, edad, email, pais]
			if database.insert_person(p):
				raise cherrypy.HTTPRedirect("/")	

	@cherrypy.expose
	def actualizar(self, id_mod=None, nombre=None, edad=None, email=None, pais=None):		
		if database.connect('start_thread'):
			p = [nombre, edad, email, pais]
			if database.update_person(id_mod, p):
				raise cherrypy.HTTPRedirect("/")

	@cherrypy.expose
	def eliminar(self, id=None):
		if database.connect('start_thread'):
			database.delete_person(id)
			raise cherrypy.HTTPRedirect('/')
	



#Ejecutamos el servidor CherryPy
#**********************************************************
import os.path
siteconf = os.path.join(os.path.dirname(__file__), 'crud.conf')

if __name__ == '__main__':
	site = Crud()	
	cherrypy.quickstart(site, config=siteconf)
else:    
    cherrypy.tree.mount(site, config=siteconf)