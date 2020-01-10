//Andrew Nguyen
//anguy224
//Programming Assignment 5

#include<stdio.h>
#include<string.h>
#include<stdlib.h>

#include "Graph.h"

#define MAX_LEN 255

int main(int argc, char * argv[]){
   int length, x, y, count, temp;
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
   
      
   fgets(line, MAX_LEN, in);   
   length = 0;
   sscanf(line, "%d", &length);
   
   List list = newList();
   for (int i=1; x<=length; i++){
	   append(list,i);
   }
   
   Graph graph = newGraph(length);
   
   while (fgets(line, MAX_LEN, in) != NULL){
      x = 0;
      y = 0;
      sscanf(line, "%d %d", &x, &y);
      if (x == 0 && y == 0) 
         break;
      addEdge(graph, x, y);   
   }
   
   DFS(graph, list);
   Graph trans = transpose(graph);
   count = 0;
   DFS(trans, list);
   moveFront(list);
   
   while (index(list)>=0){
	   if (getParent(trans, get(list)) == NIL){
		   count++;
	   }
   }
   
   List list2[count];
   
   for (int i=0; i<count; i++){
	   list2[i] = newList();
   }
   
   moveFront(list);
   int temp = count;
   
   while (index(list)>=0){
	   if (getParent(trans, get(list)) == NIL){
		   temp--;
	   }
	   if (temp == count){
		   break;
	   }
	   append(list2[temp], get(list));
	   moveNext(list);
   }
   
   fprintf(out, "Adjacency list representation of G:\n");
   printGraph(out, graph);
   fprintf(out, "\nG contains %d strongle connected components:", count);
   
   for (int i=0; i<count; i++){
	   fprintf(out, "\nComponent %d: ", (i+1));
	   printList(out, list2[i]);
	   freeList(&(list2[i]));
   }
   
   fprintf(out, "\n");
   freeGraph(&graph);
   freeGraph(&trans);
   freeList(&list);
   
   /* close files */
   fclose(in);
   fclose(out);
   
   
   return(0);
}