//Andrew Nguyen
//anguy224
//Programming Assignment 4

#include<stdio.h>
#include<stdlib.h>
#include"Graph.h"

int main(int argc, char* argv[]){
   // Build graph A 
   
   Graph A = newGraph(100);
   for(i=1; i<100; i++){
      if( i%4==0 ) addArc(A, i, 100-i);
      if( i%5==1  ) addEdge(A, i, 100-i);
   }
      
   
   BFS(A,49);
   List list = newList();
   getPath(list, A, 60);
   printf("Path of 49 to 60: ");
   printList(stdout, list);
   printf("\n")
   int distance = getDist(A, 60);
   printf("distance: ");
   
   BFS(A,49);
   List list2 = newList();
   getPath(list2, A, 2);
   printf("Path of 49 to 2: ");
   printList(stdout, list2);
   printf("\n")
   
   BFS(A,49);
   List list = newList();
   getPath(list3, A, 100);
   printf("Path of 49 to 100: ");
   printList(stdout, list3);
   printf("\n")
   
      
      
   
      
   int i, s, max, min, d, n=35;
   List  C = newList(); // central vertices 
   List  P = newList(); // peripheral vertices 
   List  E = newList(); // eccentricities 
   Graph G = NULL;

   // Build graph G 
   G = newGraph(n);
   for(i=1; i<n; i++){
      if( i%7!=0 ) addEdge(G, i, i+1);
      if( i<=28  ) addEdge(G, i, i+7);
   }
   addEdge(G, 9, 31);
   addEdge(G, 17, 13);
   addEdge(G, 14, 33);

   // Print adjacency list representation of G
   printGraph(stdout, G);

   // Calculate the eccentricity of each vertex 
   for(s=1; s<=n; s++){
      BFS(G, s);
      max = getDist(G, 1);
      for(i=2; i<=n; i++){
         d = getDist(G, i);
         max = ( max<d ? d : max );
      }
      append(E, max);
   }

   // Determine the Radius and Diameter of G, as well as the Central and 
   // Peripheral vertices.
   append(C, 1);
   append(P, 1);
   min = max = front(E);
   moveFront(E);
   moveNext(E);
   for(i=2; i<=n; i++){
      d = get(E);
      if( d==min ){
         append(C, i);
      }else if( d<min ){
         min = d;
         clear(C);
         append(C, i);
      }
      if( d==max ){
         append(P, i);
      }else if( d>max ){
         max = d;
         clear(P);
         append(P, i);
      }
      moveNext(E);
   }

   // Print results 
   printf("\n");
   printf("Radius = %d\n", min);
   printf("Central vert%s: ", length(C)==1?"ex":"ices");
   printList(stdout, C);
   printf("\n");
   printf("Diameter = %d\n", max);
   printf("Peripheral vert%s: ", length(P)==1?"ex":"ices");
   printList(stdout, P);
   printf("\n");

   // Free objects 
   freeList(&C);
   freeList(&P);
   freeList(&E);
   freeGraph(&G);
   
      
   freeList(&list);
   freeList(&list2);
   freeList(&list3);
   freeGraph(&A); 
   
   return(0);
}