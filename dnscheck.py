import sys
import sh
import jinja2
from sh import dig
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pprint


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def myapp():

#### DEFINE HOST VARIABLES ####

	SERVERS = {"MYSERVER1": {}, "MYSERVER2": {}, "MYSERVER3": {}, "MYSERVER4": {}, "MYSERVER5": {}, "MYSERVER6": {}, "MYSERVER7T": {}}
	OUTPUT = []

#### ITEMS WE REQUEST USER INPUT FOR ####

	if request.method == 'POST':
		DOMAIN = request.form["domain_html"]
		if DOMAIN == "":
			search = "-"
			return render_template('template.j2')
		RECORD_TYPE = request.form["record_html"]

	else:
		return render_template('template.j2', data="")

#### CHECK OUR DNS SERVERS WITH USER INPUT FROM 'domain' and 'record_type' ####

	for SERVER, value in SERVERS.iteritems():
		if "any" in RECORD_TYPE:
			output = dig("@" + SERVER, RECORD_TYPE , DOMAIN)
		else:
			output = dig("@" + SERVER, "+short", RECORD_TYPE , DOMAIN)
		rows = output.split('\n')
		SERVERS[SERVER]['output'] = rows

#### PRINT OUTPUT TO TERMINAL FOR EASIER TROUBLESHOOTING ####

	pprint.pprint(SERVERS)

	return render_template('template.j2', data=SERVERS)

if __name__ == "__main__":
	app.debug = True
    	app.run("0.0.0.0", port=81)
