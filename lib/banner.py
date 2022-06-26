#-*-coding: utf-8-*-


def print_banner():
	#display banner
	with open("banner.txt", "r") as f:
		print(f.read())