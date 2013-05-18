""" Cornice services.
"""
import json
from cornice import Service
import MySQLdb as mdb
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))


""" per cridar aquests serveis:

GET:
 $ curl http://localhost:6543/values/...obj_json...

POST:
 $ curl http://localhost:6543/set_values/ -d '{"cerca":"lalala"}'

"""

#values = Service(name='foo', path='/values/{cerca}/{municipios_id}/{provincias_id}/{regiones_id}',description="Cornice Demo")
values = Service(name='values', path='/values/{value}',
                 description="Cornice Demo")

set_values = Service(name='set_values', path='/set_values/',
                 description="Get...")


_VALUES = {}


@values.get()
def get_value(request):
    """Returns the value.
    """
    
    key = request.matchdict['value']
    #print key
    data = json.loads(key)
    
    
    cerca = data[0]['cerca']
    municipios_id = data[0]['municipios_id']
    provincias_id = data[0]['provincias_id']
    regiones_id = data[0]['regiones_id']
    
    con = mdb.connect('localhost','usuari','usuari','localitzador')
    
    with con:
	
	cur = con.cursor()
	cur.execute("INSERT INTO cerques (cerca,municipios_id,provincias_id,regiones_id) VALUES ('%s', %d, %d, %d)" % (cerca,int(municipios_id),int(provincias_id),int(regiones_id)))
	cur.execute("SELECT * FROM cerques")
	
	numrows = int(cur.rowcount)
	
	for i in range(numrows):
	    row = cur.fetchone()
	    print row[0],row[1],row[2],row[3],row[4]
    
    #print cerca
    #print " "
    #print localitat
    
    #return _VALUES.get(cerca)
    return "GET OK"


@set_values.post()
def set_value(request):
    """Set the value.

    Returns *True* or *False*.
    """
    """Returns the value.
    """
    
    #Obtenim les dades en format JSON i les parsejem.
    data = json.loads(request.body)
	
    cerca = data['cerca']
    municipios_id = data['municipios_id']
    provincias_id = data['provincias_id']
    regiones_id = data['regiones_id']
    
    try:
    
	#Obrim la connexio amb la base  de dades.
	con = mdb.connect('localhost','usuari','usuari','localitzador')
	
	with con:
	    
	    cur = con.cursor()
	    cur.execute("INSERT INTO cerques (cerca,municipios_id,provincias_id,regiones_id) VALUES ('%s', %d, %d, %d)" % (cerca,int(municipios_id),int(provincias_id),int(regiones_id)))
	    
	return True
    
    except:
	
	return False
