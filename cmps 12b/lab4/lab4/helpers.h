#ifndef CMPS12B_LAB4_HELPERS_H
#define CMPS12B_LAB4_HELPERS_H
#include "list.h"

List* split(char* string, char* delimiters);
char* join(List* string_array);
char* copy_string(char* string);
void* get_random(List* list);

#endif
