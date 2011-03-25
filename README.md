# FamilyBot

Copyright (c) 2007 - Jesse Lovelace <jesse.lovelace@gmail.com>
All rights reserved.

## About

FamilyBot is a natural language system that interprets English
speech in the "genealogy" domain.  The base knowledge base
for testing was Old-Testament genealogies from Adam to Jacob
(see the fixtures in dman/fixtures/initial_data.xml)

The project is split into three sections: the NLU (language 
understanding), the dialog manager, and the NLG (language generation).

### NLU

Uses Julius to understand the (trained) voice.  Note: Old-Testament names
are really hard to train and understand. :)

Next Phoenix uses the grammar (nlu/lib/Phoenix/Relations.gra) to build
frames.

I added a python module for Phoenix here: lib/Phoenix/ParseLib/py_parse.c
and a setup.py as well.  You can then import Phoenix via "import phoenix".

### DMAN

Checks context and content from NLU and builds genealogy from DB. Also
outputs in graphical form using *dot*.  Uses python for all this and
acts like a web service.

### NLG

Uses *Django* templates to create the spoken output of the system (nominally
using OSX's *say* command).

## Thanks

The project uses these packages:

 * Julius - for CSR (http://julius.sourceforge.jp/en_index.php)
 * Phoenix - for parsing (http://clear.colorado.edu)
 * Django - for the creating a Python web service.

## Testing Data

{
	'actions': [
		{
			'type':'output',
			'action':'children',
			'subject': {'id':1234, 'title':'mike'},
			'result': [
				{'id':333, 'title':'ann', 'gender':'F'},
				{'id':334, 'title':'jimmy', 'gender':'M'}
			]
		},
		{
			'type':'output',
			'action':'parents',
			'subject': {'id':1234, 'title':'anne'},
			'result': [
				{'id':333, 'title':'mike', 'gender':'M'},
				{'id':334, 'title':'susan', 'gender':'F'}
			]
		},
		{
			'type':'output',
			'action':'father',
			'subject': {'id':1234, 'title':'mike'},
			'result': [
				{'id':334, 'title':'jimmy', 'gender':'M'}
			]
		},
		{
			'type':'output',
			'action':'mother',
			'subject': {'id':1234, 'title':'mike'},
			'result': [
				{'id':334, 'title':'ann', 'gender':'F'}
			]
		},
		{
			'type':'output',
			'action':'father',
			'subject': {'id':1234, 'title':'mike'},
			'result': [
				{'id':334, 'title':'jimmy', 'gender':'M'}
			]
		},
		{
			'type':'context',
			'action':'children',
			'subject': {'id':1234, 'title':'mike'},
			'result':[
				{'id':333, 'title':'ann', 'parent':1234, 'spouse':[33], 'gender':'F'},
				{'id':334, 'title':'jimmy','parent':1234, 'spouse':[34,45], 'gender':'M'}
			]
		}
	]
}