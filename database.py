import MySQLdb
import cherrypy

def connect(thread_index):
	cherrypy.thread_data.db = MySQLdb.connect('localhost', 'root', '', 'ci_prueba')

	return True


#Hace que el array que obtenemos de la consulta MySql sea legible	
def make_readable(mask, data):
	x=[]
	d={}	
	for item in data:		
		for i in range(len(mask)):
			d[mask[i]] = item[i]
		x.append(d)
		d={}

	return x

def get_records():
	c = cherrypy.thread_data.db.cursor() 
	c.execute('select * from tb_personas order by id desc') 
	res = c.fetchall() 
	c.close() 
	mask = ['id','nombre','edad','email','pais']

	return make_readable(mask, res)

def get_persona(id):
	c = cherrypy.thread_data.db.cursor() 
	query = "select * from tb_personas where id=%s" % (id)	
	c.execute(query) 
	res = c.fetchone()
	c.close() 	
	
	return res

def insert_person(persona):
	c = cherrypy.thread_data.db.cursor() 
	fields = "(nombre, edad, email, pais)"
	values = " values ('%s', %s, '%s', '%s')" % (persona[0], persona[1], persona[2], persona[3])
	query = "insert into tb_personas "+fields+ values
	c.execute(query) 
	cherrypy.thread_data.db.commit()
	c.close() 

	return 	True

def update_person(id, p):
	c = cherrypy.thread_data.db.cursor()
	update = "nombre = '%s', edad = %s, email = '%s', pais = '%s'" % (p[0], p[1], p[2], p[3])
	where = " where id = %s" % id
	query = "update tb_personas set " + update + where
	c.execute(query)
	cherrypy.thread_data.db.commit()
	c.close()

	return True

def delete_person(id):
	c = cherrypy.thread_data.db.cursor()
	delete = " where id = %s" % id
	query = "delete from tb_personas " + delete
	c.execute(query)
	cherrypy.thread_data.db.commit()
	c.close()

	return True

