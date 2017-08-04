# File Name: linkSpider/spider.py
# Description: Use bfs to smartly explore all links on a 
# given web application. Needs to pass certain
# conditions to be considerd a unique link and explored.
from lxml import html
import requests
import json
import re


# Adjacency list containing lists. 
# Key: url. Value: list of 
adj = {};
count_unique_links = 1;

def checkDomain(url, domain):
	if domain in url:
		return True
	elif 'http' not in url:
		return True
	else:
		return False

def getLinks(url):
	page = requests.get(url)
	webpage = html.fromstring(page.content)
	bases = webpage.xpath('//base/@href')
	for base in bases:
		print(base)
	hrefs =  webpage.xpath('//a/@href')
	links = webpage.xpath('//link/@href')
	iframes = webpage.xpath('//iframe/@src')
	return (links + hrefs + iframes)


# def getSearch(url):
# 	page = requests.get(url)
# 	webpage = html.fromstring(page.content)
# 	items = webpage.xpath('//input/@type')
# 	returnable = []
# 	for item in items:
# 		if returnable 

def clean(links):
	global global_start_url
	newlinks = []
	for link in links:
		if "file://" in link:
			newlinks.append(link)
			continue
		link = link.replace("../","")
		link = link.replace("..","")
		if link == global_start_url:
			continue
		if "//" in link:
			for m in re.finditer('//', link):
				if link[int(m.start()-1)] != ":":
					link = link[:int(m.start())] + link[int(m.start()+1):]
		newlinks.append(link)
	return newlinks

def addVertice(vertice, adj):
	adj[vertice] = [];


def prune(url, delimeter):
	while url[-1] != delimeter:
		url = url[:-1]

	return url;
	

def addNeighbors(vertice, adj, neighborList):
	print(("Adding neighbors for vertice:" + vertice))
	global global_allowed_domain
	global global_start_url


	for neighbor in neighborList:
		# neighbor = neighbor.replace("../", "")
		if(checkDomain(neighbor, global_allowed_domain)):

			# if "?" in neighbor and vertice[-1] != "/" and neighbor[0] != "/":
			# 	url = prune(vertice, "/")
			# 	neighbor = url + neighbor
			if 'http' in neighbor:
				adj[vertice].append(neighbor)
			else:
				adj[vertice].append(global_start_url + neighbor)
	return adj[vertice]

def checkHop(url, adj):
	global global_start_url


	for neighbor in adj[url]:
		if "file://" in neighbor:
			 continue
		neighbor_ex = neighbor.split("/")
		neighbor_ex = neighbor_ex[:-1]
		neighbor_ex = "/".join(neighbor_ex) + "/"
		neighbor_ex.strip()
		while(neighbor_ex  != global_start_url):
			if neighbor_ex not in adj[url]:
				adj[url].append(neighbor_ex)

			neighbor_ex = neighbor_ex.split("/")
			neighbor_ex = neighbor_ex[:-1]
			neighbor_ex = neighbor_ex[:-1]
			neighbor_ex = "/".join(neighbor_ex) + "/"
			neighbor_ex.strip()
	return adj[url]

def checkQ(url, adj):
	global global_start_url

	if "?" in url:
		newUrl = prune(url, "?")
		if newUrl not in adj[url]:
			adj[url].append(newUrl[:-1])
	return adj[url]

def BFS(s, adj):
	# Global variable adjaceny list. Not built because of unknown data
	# global adj
	# Level keeps track of how many steps it took to get to said node
	level = {s: 0}
	parent = {s : None}
	i = 1;
	frontier = [s]
	while frontier:
		nextItem = []
		for u in frontier:
			if u not in adj:
				adj[u] = [];
				adj[u] = addNeighbors(u, adj, getLinks(u));
				adj[u] = checkHop(u, adj)
				adj[u] = checkQ(u, adj)
				adj[u] = clean(adj[u])
			for v in adj[u]:
				if v not in level:
					level[v] = i
					parent[v] = u
					nextItem.append(v)
		frontier = nextItem
		i = i + 1
		print(i)
	return level





global_start_url = "http://demo.testfire.net/"
global_allowed_domain = "demo.testfire.net"



# test = "http://demo.testfire.net/bank/ass"
# print(test)
# print(getVertice(test))

# test2 = "http://demo.testfire.net/bank/"
# print(test2)
# print(getVertice(test2))




hold = BFS(global_start_url, adj);



# # preOrderPrint 
# # print(hold);
print(len(hold));


for x in hold:
	print(str(x))

