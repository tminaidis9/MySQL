import sys, os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
from bottle import route, run, static_file, request
import settings
import app

def renderTable(tuples):
    printResult = """<style type='text/css'> h1 {color:red;} h2 {color:blue;} p {color:green;} </style>
    <table border = '1' frame = 'above'>"""

    header='<tr><th>'+'</th><th>'.join([str(x) for x in tuples[0]])+'</th></tr>'
    data='<tr>'+'</tr><tr>'.join(['<td>'+'</td><td>'.join([str(y) for y in row])+'</td>' for row in tuples[1:]])+'</tr>'
        
    printResult += header+data+"</table>"
    return printResult

@route('/mostcommonsymptoms')
def mostcommonsymptoms():
    r1 = request.query.vax_name or "Unknown vax name"
    table = app.mostcommonsymptoms(r1)
    return "<html><body>" + renderTable(table) + "</body></html>"
	

@route('/buildnewblock')
def buildnewblock():
    blockfloor = request.query.blockfloor    
    table = app.buildnewblock(blockfloor)
    return "<html><body>" + renderTable(table) + "</body></html>"
	
@route('/findnurse')
def findnurse():
    x = request.query.x
    y = request.query.y    
    table = app.findnurse(x,y)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/patientreport')
def patientreport():
    patientName = request.query.patientName    
    table = app.patientreport(patientName)
    return "<html><body>" + renderTable(table) + "</body></html>"

 
@route('/:path')
def callback(path):
    return static_file(path, 'web')

@route('/')
def callback():
    return static_file("index.html", 'web')

run(host='localhost', port=settings.web_port, reloader=True, debug=True)