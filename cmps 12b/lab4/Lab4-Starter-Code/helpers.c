
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"

char* copy_string(char* string){
  char* new_string = calloc(strlen(string)+1,sizeof(char));
  strcpy(new_string,string);
  return new_string;
}

char *strtok_new(char * string, char const * delimiter){
  static char *source = NULL;
  char *p, *riturn = 0;
  if(string != NULL)         source = string;
  if(source == NULL)         return NULL;

  if((p = strpbrk (source, delimiter)) != NULL) {
    *p  = 0;
    riturn = source;
    source = ++p;
  }
  return riturn;
}

List* split(char* string, char* delimiters){

  char* temp = calloc(strlen(string)+2,sizeof(char));
  strncpy(temp,string,strlen(string));
  temp[strlen(string)] = delimiters[0];
  char * pch;
  pch = strtok_new(temp,delimiters);

  int count = 0;
  List* list = make_list();
	
  while (pch)
    {

      char* element = copy_string(pch);
      add(list,list->size,element);
      pch = strtok_new(NULL, delimiters);
    }
  free(temp);

  
  return list;

}

char* join(List* string_list){

  int total_size = 0;

  for (int ii = 0; ii < string_list->size; ii++){
    total_size += strlen((char*) get(string_list,ii));
  }

  char* concatenated_string = calloc(total_size + 1, sizeof(char));

  int sentinel = 0;

  

  for (int ii = 0; ii < string_list->size; ii++){
    int jj = 0;
    while ( ((char*)get(string_list,ii))[jj] != '\0'){
      concatenated_string[sentinel] = ((char*)get(string_list,ii))[jj];
      sentinel++;
      jj++;
    }
  }

  return concatenated_string;

}


void* get_random(List* list){
	
  return get(list,rand() %list->size);
}

