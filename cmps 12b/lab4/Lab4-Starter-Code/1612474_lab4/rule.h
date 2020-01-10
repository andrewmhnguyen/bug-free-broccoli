#ifndef TRACERY_HELPERS_H
#define TRACERY_HELPERS_H
#include "list.h"

typedef struct 
{
  /*
   * TODO 0
   */
  // define the things a rule struct needs
  char* key;
  List* expansions;
  /*
   * TODO 0
   */
    
} Rule;



Rule* make_rule(char* key);

void free_rule(Rule* rule);

List* read_grammar(char* filename);

char* expand(char* rule, List* grammar);

void print_grammar(List* grammar);

#endif
