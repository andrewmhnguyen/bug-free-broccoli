#include<stdio.h>
#include<string.h>
#include<stdlib.h>

#include "Graph.h"

#define MAX_LEN 255

int main(int argc, char * argv[]){

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
   
   int length = 0;
   sscanf(line, "%d", &length);
   
   Graph graph = newGraph(length);
   
   while (fgets(line, MAX_LEN, in) != NULL){
      int x = 0;
      int y = 0;
      sscanf(line, "%d %d", &x, &y);
      if (x == 0 && y == 0) 
         break;
      addEdge(graph, a, b);   
   }
   printGraph(out, graph);
   
   int count = 0;
   
   while (fgets(line, MAX_LEN, in) != NULL)  {
      int des = 0;
      int sor = 0;
      
      sscanf(line, "%d %d", &des, &sor);
      
      if(des == 0 && sor == 0){
         break;
      }
      
      if(count++ != 0){
         fprintf(out, "\n");
      }
      fprintf(out, "\n");
      
      BFS(graph, des);
      
      int dis = getDistance(graph, sor);
      fprintf(out, "The distance from %d to %d is ", des, sor);
      
      if(dis == INF){
         fprintf(out, "infinity\n");
      }
      else{
         fprintf(out, "%d\n", dis);
      }
      
      List list = newList();
      getPath(list, graph, sor);
      
      if(front(lis) == NIL){
         fprintf(out, "No %d-%d path exists", des, sor);
      }
      else {
         fprintf(out, "A shortest %d-%d path is: ", des, sor);
         printList(out, list);
      }
      
      freeList(&list);
   }

   fprintf(out, "\n");
   freeGraph(&graph);   

   /* close files */
   fclose(in);
   fclose(out);
   
   
   return(0);
}