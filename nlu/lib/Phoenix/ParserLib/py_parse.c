#include "Python.h"

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "parse.h"
#include "pconf.h"
#include "globals_parse.h"

#define PHOENIXPARSE_DOC "Parse a string with Phoenix.\n"

void strip_line(char * line);

extern char	dict_file[LABEL_LEN],
		priority_file[LABEL_LEN],
		frames_file[LABEL_LEN],
		*grammar_file;
		
static char	outbuf[10000],		/* output text buffer for parses */
		*out_ptr= outbuf;
		
static int	utt_num = 0;

static PyObject *phoenix_parse(PyObject *self, PyObject *args)
{
	const char * line;
	const char * dir;
	const char * grammar_tmp;
	
	if (!PyArg_ParseTuple(args, "sss", &line, &dir, &grammar_tmp)) {
		return (PyObject*)NULL;
	}
	grammar_file = malloc(strlen(grammar_tmp)+1);
	strcpy(grammar_file,grammar_tmp);
	
	strip_line(line);
	
	init_parse(dir, dict_file, grammar_file, frames_file, priority_file);
	
	out_ptr= outbuf; *out_ptr= 0;

	/* echo the line */
	if (verbose > 1){
		sprintf(out_ptr, ";;;%d %s\n", utt_num, line);
		out_ptr += strlen(out_ptr);
	}
	
	parse(line, gram);
	extract=1;
	if( num_parses > MAX_PARSES ) num_parses= MAX_PARSES;
	int i;
	if( ALL_PARSES ) {
            for(i= 0; i < num_parses; i++ ) {
	    	sprintf(out_ptr, "PARSE_%d:\n", i);
	    	out_ptr += strlen(out_ptr);
	    	print_parse(i, out_ptr, extract, gram);
	    	out_ptr += strlen(out_ptr);
	    	sprintf(out_ptr, "END_PARSE\n");
	    	out_ptr += strlen(out_ptr);
            }
	}
	else {
	    	print_parse(0, out_ptr, extract, gram);
	    	out_ptr += strlen(out_ptr);
	}
	printf(outbuf);
	//sprintf(out_ptr, "\n");
	out_ptr += strlen(out_ptr);
	free(grammar_file);
	return Py_BuildValue("s", outbuf);
}

static PyMethodDef phoenixMethods[] = {
  {"parse", phoenix_parse},
  {NULL, NULL }
};

void initphoenix_driver(void)
{
  const char *phoenix_documentation = "Phoenix parser.\n";

  Py_InitModule3("phoenix_driver", phoenixMethods, phoenix_documentation);

}

void strip_line(char *line)
{
  char	*from, *to;

  for(from= to= line; ;from++ ) {
    if( !(*from) ) break;


    switch(*from) {

      /* filter these out */
    case '(' :
    case ')' :
    case '[' :
    case ']' :
    case ':' :
    case ';' :
    case '?' :
    case '!' :
    case '\n' :
      break;

      /* replace with space */
    case ',' :
    case '\\' :
      *to++ = ' ';
      break;

    case '#' :
	for( ++from; *from != '#' && *from; from++);
	if( *from == '#' ) from++;
	break; 

    case '-' :
      /* if partial word, delete word */
      if( isspace( (int) *(from+1) ) ) {
	while( (to != line) && !isspace( (int) *(--to) ) ) ;
	/* replace with space */
	*to++ = ' ';
      }
      else {
	/* copy char */
	*to++ = *from;
      }
      break;


    default:
      /* copy char */
      *to++ = (islower((int)*from)) ? (char) toupper((int)*from) : *from;
    }
    if( !from ) break;

  }
  *to= 0;

}


