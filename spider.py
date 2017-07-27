#!/usr/local/bin/python3
# Author: Daniel Thurau
# File Name: linkSpider/spider.py
# Description: Use bfs/dfs to smartly explore all links 
# avalible from a given start url. Needs to pass certain
# conditions to be considerd a unique link to be explored.
from lxml import html
import requests
import json

# Adjacency list containing lists. 
# Key: url. Value: list of 
adj = {};
visited = {}
queue = []
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
	return webpage.xpath('//a/@href')

def addVertice(vertice):
	global adj
	adj[vertice] = [];


def addNeighbors(vertice, neighborList):
	print(("Adding neighbors for vertice:" + vertice))
	global adj
	global global_allowed_domain
	global global_start_url
	for neighbor in neighborList:
		if(checkDomain(neighbor, global_allowed_domain)):
			if 'http' in neighbor:
				adj[vertice].append(neighbor)
			else:
				adj[vertice].append(global_start_url + neighbor)




def BFS(s):
	# Global variable adjaceny list. Not built because of unknown data
	global adj
	# Level keeps track of how many steps it took to get to said node
	level = {s: 0}
	parent = {s : None}
	i = 1;
	frontier = [s]
	while frontier:
		nextItem = []
		for u in frontier:
			if u not in adj:
				addVertice(u);
				addNeighbors(u,getLinks(u));
			for v in adj[u]:
				if v not in level:
					level[v] = i
					parent[v] = u
					nextItem.append(v)
		frontier = nextItem
		i = i + 1
		print(i)
	return level





global_start_url = input("Enter starting URL: ")
global_allowed_domain = input("Enter allowed domains: ")


hold = BFS(global_start_url);
print(hold);
print(len(hold));


