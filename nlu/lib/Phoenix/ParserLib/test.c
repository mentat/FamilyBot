#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "parse.h"
#include "pconf.h"
#include "globals_parse.h"

#define PHOENIXPARSE_DOC "Parse a string with Phoenix.\n"

void strip_line(char * line);

int main(int argc, char**argv) {
	
	printf("hi there\n");
	char dir[] = "Grammar";
	char dict_file[] = "";
	char grammar_file[] = "EX.net";
	char frames_file[] = "";
	char priority_file[] = "";
	char line[] = "I want to fly from new york to los angeles";
 

	init_parse(dir, dict_file, grammar_file, frames_file, priority_file);

	printf("grammar ok");
	
	parse(line, gram);
	return 0;
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