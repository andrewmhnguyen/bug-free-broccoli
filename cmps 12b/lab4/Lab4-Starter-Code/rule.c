
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"
#include "rule.h"
#include "helpers.h"

//makes a rule and gives it value key and adds an empty list called expansions
Rule* make_rule(char* key){
  /*
    TODO 3
  */
  Rule* newRule = calloc(1,sizeof(Rule));
  newRule->key = key;
  List* newList = calloc(1,sizeof(List));
  newList->size=0;
  newList->head=0;
  newRule->expansions = newList;
  return newRule; 
  /*
    TODO 3
  */
}

//frees a rule and the key and expansions inside of it 
void free_rule(Rule* rule){
  /*
    TODO 3
  */
  free(rule->key);
  free(rule->expansions);
  free(rule);	
  /*
    TODO 3
  */
	
}


List* read_grammar(char* filename){
   
  /*
   * TODO 4A
   */ 
  //Construct a new List* called grammar that we will fill up in the following code
  List* grammar = calloc(1,sizeof(List));
  /* 
   * TODO 4A
   */
  FILE* input_file = fopen(filename,"r");
  char buffer[1000];
  
  int number_of_expansions = 0;
  int buffer_index = 0;
  int number_of_rules = 0;

  for (char current = fgetc(input_file); current != EOF; current = fgetc(input_file)){
    if (current == ':'){
      
	  
      char* key = calloc(buffer_index+1,sizeof(char));
      memcpy(key,buffer,buffer_index);
      /*
       * TODO 4B
       */ 
	   
      //Construct a new Rule* and add it to grammar
      Rule* rule = make_rule(key);
      add(grammar, number_of_rules, rule);
      number_of_expansions = 0;
      number_of_rules++;
      /*
       * TODO 4B
       */ 
      buffer_index = 0;
    }
    else if (current == ',' || current == '\n'){
      
      char* expansion = calloc(buffer_index+1,sizeof(char));      
      memcpy(expansion,buffer,buffer_index);
		
      /*
       * TODO 4C
       */ 
      //takes rule and adds an expansion to it
      Rule* rule = get(grammar, number_of_rules-1);
      add(rule->expansions, number_of_expansions, expansion);
      number_of_expansions = number_of_expansions + 1;
      /*
       * TODO 4C
       */ 
      buffer_index = 0;
		 
    }
    else {
      buffer[buffer_index] = current;
      buffer_index++;
    }
  }
  fclose(input_file);

  
  /*
   * TODO 4D
   */ 
  return grammar;// replace this to return the grammar we just filled up
  /*
   * TODO 4D
   */ 
}



char* expand(char* text, List* grammar){

  /*
   * BONUS TODO
   */
	
  /*
   * BONUS TODO
   */
}

//Iterates through a grammar list and prints out all of the rules
void print_grammar(List* grammar){
  
  for (int ii = 0; ii < grammar->size; ii++){
    Rule* rule = get(grammar,ii);
    for (int jj = 0; jj < rule->expansions->size; jj++){
      printf("A potential expansion of rule '%s' is '%s'\n",rule->key, (char*) get(rule->expansions,jj));
    }
  }
  
}
