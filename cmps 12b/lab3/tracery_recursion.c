#include <stdio.h>
#include <stdlib.h>

char* make_string_from(char* from, int count) {
	/* TODO 2 */
  char* char_array = calloc(count+1,sizeof(char));
  for(int i = 0; i < count; i++){
    char_array[i]=from[i];
  }
  return char_array;
	/* TODO 2 */
}

int main(int argc, char** argv) {
	/* TODO 1 */
  for(int i = 0; i <argc; i++){
    printf("%s\n", argv[i]);
  }
 	/* TODO 1 */

  
 	/* TODO 3 */
  char char_buffer[1000];
  int buffer_index = 0;
  char* rule = NULL;
  char* expansion = NULL;
  char c = getchar();
  while (c!=EOF){
    if (c==':'){
      rule = make_string_from(char_buffer,buffer_index);
      buffer_index = 0;
    }
    else if (c==','||c=='\n'){
      expansion = make_string_from(char_buffer,buffer_index);
      buffer_index = 0;
      printf("A potential expansion for rule '%s' is '%s'\n", rule, expansion);
      if(c=='\n'){
        free(rule);
      }      
      free(expansion);
    }
    else{
      char_buffer[buffer_index] = c;
      buffer_index = buffer_index + 1;
    }
    c = getchar();
  }
 	/* TODO 3 */
}


