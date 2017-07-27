

fname = "output.csv"
unique_urls = {};
with open(fname) as f:
	for line in f:
		line.strip();
		unique_urls[line] = 1;


		
print("---------------------------------------------------------");
print("There were " + str(len(unique_urls)) + " unique urls tranversed");
print("---------------------------------------------------------");
