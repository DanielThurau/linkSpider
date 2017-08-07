#!/usr/local/bin/python3

# File Name: linkSpider/spider.py
# Description: Use bfs to smartly explore all links on a 
# given web application. Needs to pass certain
# conditions to be considerd a unique link and explored.

from lxml import html 		# HTML Parsers

import json 				# Formats data in json format
import re 					# Regular expression library
import requests				# Performs HTML requests


# return true if either is in there
# return false if neither are
# 2 cases , something like /bank, or /bank
def checkContents(tup, searchable):
	# print(tup)
	if not tup:
		return False
	if(tup[0] == ""):
		return False

	if tup[0][0] == '/' and len(tup[0]) > 1:	# if /bank, first if becomes bank, second becomes /bank
		toSearch = (tup[0][1:], tup[1])
		if toSearch in searchable:
			return True
	elif tup[0][0] != '/':
		toSearch = ('/' + tup[0], tup[1])
		if toSearch in searchable:
			return True
	
	if tup in searchable: # if just bank, check that or /bank
		return True

	return False




def checkContentSingle(tup, searchable):
	if tup[0] == '/' and len(tup) > 1:	# if /bank, first if becomes bank, second becomes /bank
		toSearch = tup[1:]
		if toSearch in searchable:
			return True
	else:
		toSearch = "/" + tup
		if toSearch in searchable:
			return True
	
	if tup in searchable: # if just bank, check that or /bank
		return True


	return False

def checkDomain(url, domain):
	if domain in url: # explicitly okay
		return True
	elif 'http' not in url: # relative to root -> okay
		return True
	else:
		return False

# Check if right most filename in vertice is in neighbor
def checkContain(parent, child, delim,depth=0):
	popped = ""

	# Pop until '/' is reached
	while True:
		if parent[-1] == delim: # if char is '/' remove a depth level, 
			depth = depth - 1
			if depth < 0: # if deoth level is reached
				parent = parent[:-1] # Pop last char
				break

		if depth == 0:	# start adding to popped when depth level is allowed
			child = parent[-1] + child

		parent = parent[:-1] # Pop last char

	if popped in child:
		return True
	else:
		return False


# getLinks requests an html page using given url
# and parses links from page
def getLinks(url):
	global global_start_url

	# print(url)
	if url[0] == "":
		return []
	elif 'http' not in url[0]:
		if url[0][0] != '/' and url[1] == global_start_url:
			getURL = url[1] + url[0]
		if url[0][0] == '/' and url[1] == global_start_url:
			getURL = url[1][:-1] + url[0]
		if url[0][0] == '/' and url[1] != global_start_url:
			if '?' in url[0] and '?' not in url[1] and checkContain(url[0], url[1], "?"):
				temp = prune(url[0], "?")
				whatiwant = url[0].replace(temp[:-1], "")
				getURL = global_start_url + url[1] + whatiwant
				url = (url[1] + whatiwant, url[1])
			elif url[1] in url[0]:
				getURL = global_start_url + url[0]
			elif url[1][-1] != '/':
				getURL = global_start_url + url[0]
			else:
				getURL = global_start_url + url[1] + url[0]
		if url[0][0] != '/' and url[1] != global_start_url:
			if url[0] == url[1]:
				getURL = global_start_url + url[0]
			if url[0] != url[1]:
				if '?' in url[0] and '?' not in url[1] and checkContain(url[0], url[1], "?"):
					temp = prune(url[0], "?")
					whatiwant = url[0].replace(temp[:-1], "")
					getURL = global_start_url + url[1] + whatiwant
					url = (url[1] + whatiwant, url[1])
				elif url[1][-1] != '/':
					getURL = global_start_url + url[0]
				else:
					getURL = global_start_url + url[0] + url[1]
	else:
		getURL = url[0]

	page = requests.get(getURL)
	webpage = html.fromstring(page.content)

	return (webpage.xpath('//base/@href') + webpage.xpath('//a/@href') \
		+ webpage.xpath('//link/@href') + webpage.xpath('//iframe/@src') \
		+ webpage.xpath('//form/@action')), url


# Sanitizes link after performing opearations. 
# Removes any '../' and '//'
# ignores and 'file://'
def clean(links):
	global global_start_url

	newlinks = []
	for link in links:
		# Add to newlinks unchanged
		if "file://" in link[0] and not checkContents(link, newlinks):
			newlinks.append(link)
			continue
		# Replace direcotry changes
		link = (link[0].replace("../",""), link[1])
		link = (link[0].replace("..",""), link[1])

		
		# Remove any double slashes w/o removing ://
		if "//" in link[0]:
			for m in re.finditer('//', link[0]):
				if link[0][int(m.start()-1)] != ":":
					link = (link[0][:int(m.start())] + link[0][int(m.start()+1):],link[1])

		# add the modifies url
		# If removing these chars changes the link to the 
		# global_start_url, ignore
		if link[0] == global_start_url or link[0] == "":
			continue
		elif not checkContents(link, newlinks):
			newlinks.append(link)
	return newlinks

# Prune a url to deleimeter 
def prune(url, delimeter):
	while len(url) > 0 and url[-1] != delimeter:
		url = url[:-1]
	return url;
	

def addNeighbors(vertice, adj, neighborList):
	print(("Adding neighbors for vertice:" + vertice[0]))
	global global_allowed_domain
	global global_start_url



	for neighbor in neighborList:

		if(checkDomain(neighbor, global_allowed_domain)):
			tup = (neighbor, vertice[0])
			if not checkContents(neighbor, adj[vertice]):
				adj[vertice].append(tup)
	return adj[vertice]

# if there is a hidden directory, pop it
def checkHop(url, adj):
	global global_start_url

	newList = []
	for neighbor in adj[url]:
		if "file://" in neighbor[0]:
			 continue
		newURL = neighbor[0];
		while len(newURL) > 0:
			if newURL == global_start_url:
				break

			if newURL[-1] == "/":
				newURL = prune(newURL[:-1],"/")
			else:
				newURL = prune(newURL,"/")
			if not checkContents((newURL, neighbor[1]), adj[url]):
				newList.append((newURL,neighbor[1]))

	adj[url] = adj[url]+newList
	return adj[url]

def checkQ(url, adj):
	global global_start_url

	if "?" in url[0]:
		newUrl = prune(url[0], "?")
		if not checkContents((newUrl,url[1]),adj[url]):
			adj[url].append((newUrl[:-1],url[1]))
	return adj[url]


def prettyPrint(neighbors):
	for neighbor in neighbors:
		print("		" + neighbor[0])

def BFS(s, adj):
	# Global variable adjaceny list. Not built because of unknown data
	# global adj
	# Level keeps track of how many steps it took to get to said node
	level = {s[0]: 0}
	parent = {s : None}
	i = 1;
	frontier = [s]
	while frontier:
		nextItem = []
		for u in frontier:
			if u not in adj:
				adj[u] = [];
				links, update = getLinks(u)

				if update[0] not in level:
					level[update[0]] = level[u[0]]
					del level[u[0]]

				adj[u] = addNeighbors(u, adj, links);
				adj[u] = checkHop(u, adj)
				adj[u] = checkQ(u, adj)
				adj[u] = clean(adj[u])
				# prettyPrint(adj[u])
			for v in adj[u]:

				if checkContentSingle(v[0], level) == False:
					level[v[0]] = i
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
startLink = (global_start_url, "/")
hold = BFS(startLink, adj);



# # preOrderPrint 
# # print(hold);
print(len(hold));

# Prints the key in the dictionary, which is the url
for x in hold:
	print(str(x))

