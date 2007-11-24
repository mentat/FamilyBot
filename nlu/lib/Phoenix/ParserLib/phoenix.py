import phoenix_driver, re

FRAME_NAME = re.compile(r'^([A-Za-z]+):\[')

def parse(strg, dir="Grammar", net="EX.net"):
	p_parse = phoenix_driver.parse(strg, dir, net)
	parses = list()
	current_parse = list()
	for line in p_parse.split("\n"):
			
		frame = {}
		name_match = FRAME_NAME.match(line)
		if name_match is None:
			if len(current_parse) > 0:
				parses.append(current_parse)
				current_parse = []
			continue
		else:
			frame['name'] = name_match.group(1)
			#print "Name is %s" % name_match.group(1)
	
		frame['nodes']=[]
		line = line[line.find(':')+1:].strip()

		for node in line.split(' '):
			parts = []
			for part in node.split('.'):
				part = part.strip('[]')
				parts.append(part)
				#print part
			frame['nodes'].append({'value':parts[-1] ,'name':parts[:-1]})
		#print "appending frame"
		
		current_parse.append(frame)
	
	return parses