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

# def getSearch(url):
# 	page = requests.get(url)
# 	webpage = html.fromstring(page.content)
# 	items = webpage.xpath('//input/@type')
# 	returnable = []
# 	for item in items:
# 		if returnable 


def addVertice(vertice):
	global adj
	adj[vertice] = [];


def addNeighbors(vertice, neighborList):
	print(("Adding neighbors for vertice:" + vertice))
	global adj
	global global_allowed_domain
	global global_start_url
	for neighbor in neighborList:
		# neighbor = neighbor.replace("../", "")
		if(checkDomain(neighbor, global_allowed_domain)):
			if 'http' in neighbor:
				adj[vertice].append(neighbor)
			else:
				adj[vertice].append(global_start_url + neighbor)

def checkHop(url):
	# print("Entered check hop")
	global adj
	global global_start_url
	# print("-----------------------------------------------------")
	# print(adj[url])
	# url_ex = url.split("/");
	for neighbor in adj[url]:
		# print(neighbor)
		# neighbor = neighbor.replace("../", "")
		neighbor_ex = neighbor.split("/")
		neighbor_ex = neighbor_ex[:-1]
		neighbor_ex = "/".join(neighbor_ex) + "/"
		neighbor_ex.strip()
		# neighbor_ex = neighbor_ex.replace("//","/")
		# print("		" + neighbor_ex)
		# count = 0;
		# print(global_start_url);
		while(neighbor_ex  != global_start_url):
			# print("		" + neighbor_ex)
			if neighbor_ex not in adj[url]:
				# print("Not in neighbors")
				adj[url].append(neighbor_ex[:-1])

			neighbor_ex = neighbor_ex.split("/")
			# print(neighbor_ex)
			neighbor_ex = neighbor_ex[:-1]
			neighbor_ex = neighbor_ex[:-1]
			# print(neighbor_ex)
			neighbor_ex = "/".join(neighbor_ex) + "/"
			# print("		" + neighbor_ex)
			neighbor_ex.strip()
			# neighbor_ex = neighbor_ex.replace("//","/")
		# 	count+=1;


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
				addVertice(u);
				addNeighbors(u,getLinks(u));
				checkHop(u)
			for v in adj[u]:
				if v not in level:
					level[v] = i
					parent[v] = u
					nextItem.append(v)
		frontier = nextItem
		i = i + 1
		print(i)
	return level



def preOrderPrint(url, adj, i, visited):
	for i in range(0,i):
		print("   ", end="")
	print(url)
	items = adj[url]
	for u in items:
		if u != url and u not in visited:
			visited[u] = 1
			preOrderPrint(u, adj, i+1, visited)
		# else:
		# 	for i in range(0,i):
		# 		print("   ", end="")
		# 	print(u) 
	# return

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))






# global_start_url = input("Enter starting URL: ")
# global_allowed_domain = input("Enter allowed domains: ")
global_start_url = "http://demo.testfire.net/"
global_allowed_domain = "demo.testfire.net"





hold = BFS(global_start_url, adj);


# print(json.dumps(adj, indent=1))
# pretty(adj);
print("--------------------------------------------")
visited = {}
preOrderPrint(global_start_url, adj, 0, visited);

# preOrderPrint 
# print(hold);
# print(len(hold));


# for x in hold:
# 	print(str(x))

