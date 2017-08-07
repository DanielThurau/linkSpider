#!/usr/local/bin/python3

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
def checkContain(vertice, neighbor, depth=0):
	popped = ""

	# Pop until '/' is reached

	while True:

		if vertice[-1] == "/": # if char is '/' remove a depth level, 
			depth = depth - 1
			if depth < 0: # if deoth level is reached
				break

		if depth == 0:	# start adding to popped when depth level is allowed
			popped = vertice[-1] + popped

		vertice = vertice[:-1] # Pop last char

	if popped in neighbor:
		return True
	else:
		return False


# getLinks requests an html page using given url
# and parses links from page
def getLinks(url):
	global global_start_url

	print(url)
	if 'http' not in url[0]:
		if url[0][0] != '/':
			getURL = url[1] + url[0]
		if url[0][0] == "/" and url[1] == global_start_url:
			getURL = url[1][:-1] + url[0]


	else:
		getURL = url[0]

	page = requests.get(getURL)
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
		if "file://" in link and link not in newlinks:
			newlinks.append(link)
			continue
		# Replace direcotry changes
		link = link.replace("../","")
		link = link.replace("..","")

		
		# Remove any double slashes w/o removing ://
		if "//" in link:
			for m in re.finditer('//', link):
				if link[int(m.start()-1)] != ":":
					link = link[:int(m.start())] + link[int(m.start()+1):]

		# add the modifies url
		# If removing these chars changes the link to the 
		# global_start_url, ignore
		if link == global_start_url:
			continue
		elif link not in newlinks:
			newlinks.append(link)
	return newlinks

# Prune a url to deleimeter 
def prune(url, delimeter):
	while url[-1] != delimeter:
		url = url[:-1]
	return url;
	

def addNeighbors(vertice, adj, neighborList):
	print(("Adding neighbors for vertice:" + vertice[0]))
	global global_allowed_domain
	global global_start_url


	for neighbor in neighborList:

		if(checkDomain(neighbor, global_allowed_domain)):
			tup = (neighbor, vertice[0])
			if neighbor not in adj[vertice]:
				adj[vertice].append(tup)
	return adj[vertice]

# if there is a hidden directory, pop it
def checkHop(url, adj):
	global global_start_url

	newList = []
	for neighbor in adj[url]:
		# try:
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


def prettyPrint(neighbors):
	for neighbor in neighbors:
		print("		" + neighbor[0])

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
				# adj[u] = checkHop(u, adj)
				# adj[u] = checkQ(u, adj)
				# adj[u] = clean(adj[u])
				prettyPrint(adj[u])
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
startLink = (global_start_url, "/")
hold = BFS(startLink, adj);



# # preOrderPrint 
# # print(hold);
print(len(hold));

# Prints the key in the dictionary, which is the url
for x in hold:
	print(str(x))

