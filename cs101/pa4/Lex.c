//Andrew Nguyen
//anguy224
//Programming Assignment 2

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#include "List.h"

#define MAX_LEN 160

int main(int argc, char * argv[]){
   int count = 0;
   FILE *in, *out;
   char line[MAX_LEN];
   
   // check command line for correct number of arguments
   if( argc != 3 ){
      printf("Usage: %s <input file> <output file>\n", argv[0]);
      exit(1);
   }

   // open files for reading and writing 
   in = fopen(argv[1], "r");
   out = fopen(argv[2], "w");
   if( in==NULL ){
      printf("Unable to open file %s for reading\n", argv[1]);
      exit(1);
   }
   if( out==NULL ){
      printf("Unable to open file %s for writing\n", argv[2]);
      exit(1);
   }

   while (fgets(line, MAX_LEN, in) != NULL){
      count++;
   }
   
   rewind(in);   
   
   char lines[count - 1][MAX_LEN];
   int count2 = -1;
   
   while (fgets(line, MAX_LEN, in) != NULL){
      count2++;
      strcpy(lines[count2], line);
   }
   
   List list = newList();

   for (int i=0; i<count; i++) {
      char *tmp = lines[i];
      int j = i-1;
      moveBack(list);
      while (j>=0 && strcmp(tmp, lines[get(list)])<=0){
         j--;
         movePrev(list);
      }
      
      if(index(list) < 0)
         prepend(list, i);
      else
         insertAfter(list, i);
   }
   
   moveFront(list);
   while (index(list)>=0){
      fprintf(out, "%s", lines[get(list)]);
      moveNext(list);
   }

   freeList(&list);

   /* close files */
   fclose(in);
   fclose(out);
   

   return(0);
}