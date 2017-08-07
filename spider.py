# File Name: linkSpider/spider.py
# Description: Use bfs to smartly explore all links on a 
# given web application. Needs to pass certain
# conditions to be considerd a unique link and explored.

from lxml import html 		# HTML Parsers

import json 				# Formats data in json format
import re 					# Regular expression library
import requests				# Performs HTML requests


def checkDomain(url, domain):
	if domain in url: # explicitly okay
		return True
	elif 'http' not in url: # relative to root -> okay
		return True
	else:
		return False

# Check if right most filename in vertice is in neighbor
def checkContain(vertice, neighbor):
	popped = ""

	# Pop until '/' is reached
	while True:
		if vertice[-1] == "/":
			break;
		popped = vertice[-1] + popped
		vertice = vertice[:-1]

	if popped in neighbor:
		return True
	else:
		return False


# getLinks requests an html page using given url
# and parses links from page
def getLinks(url):
	page = requests.get(url)
	webpage = html.fromstring(page.content)

	return (webpage.xpath('//base/@href') + webpage.xpath('//a/@href') \
		+ webpage.xpath('//link/@href') + webpage.xpath('//iframe/@src') \
		+ webpage.xpath('//form/@action'))


# Sanitizes link after performing opearations. 
# Removes any '../' and '//'
# ignores and 'file://'
def clean(links):
	global global_start_url

	newlinks = []
	for link in links:
		# Add to newlinks unchanged
		if "file://" in link:
			newlinks.append(link)
			continue
		# Replace direcotry changes
		link = link.replace("../","")
		link = link.replace("..","")

		# If removing these chars changes the link to the 
		# global_start_url, ignore
		if link == global_start_url:
			continue
		# Remove any double slashes
		if "//" in link:
			for m in re.finditer('//', link):
				if link[int(m.start()-1)] != ":":
					link = link[:int(m.start())] + link[int(m.start()+1):]
		# add the modifies url
		newlinks.append(link)
	return newlinks

# Prune a url to deleimeter 
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
			# print("		Adding neighbor: " + neighbor)
			# try:
			# 	if vertice[-1] == "/" or "?" in neighbor and checkContain(vertice, neighbor):
			# 		base = prune(vertice, "/")
			# 		neighbor = base + neighbor
			# except IndexError:
			# 	pass
			if 'http' in neighbor:
				adj[vertice].append(neighbor)
			else:
				adj[vertice].append(global_start_url + neighbor)
	return adj[vertice]

def checkHop(url, adj):
	global global_start_url

	# if url == global_start_url:
	# 	return adj[url]
	newList = []
	for neighbor in adj[url]:
		# try:
		# 	if neighbor[-1] == "/":
		# 		neighbor = neighbor[:-1]
		# except IndexError:
		# 	continue
		# print("		checking hop on url: " + neighbor)
		if "file://" in neighbor:
			 continue
		newURL = neighbor;
		while True:
			if newURL == global_start_url:
				break
			if newURL[-1] == "/":
				newURL = prune(newURL[:-1],"/")
			else:
				newURL = prune(newURL,"/")
			# print("			Pruned neighbor : " + newURL)
			if newURL not in adj[url]:
				# print(newURL)
				newList.append(newURL)
				if newURL != global_start_url:
					newURL = newURL[:-1]

	adj[url] = adj[url]+newList
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

# Adjacency list containing lists. 
# Key: url. Value: list of 
adj = {};


hold = BFS(global_start_url, adj);



# # preOrderPrint 
# # print(hold);
print(len(hold));

# Prints the key in the dictionary, which is the url
for x in hold:
	print(str(x))

