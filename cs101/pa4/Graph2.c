//Andrew Nguyen
//anguy224
//Programming Assignment 4

#include <stdio.h>
#include <stdlib.h>
#include "Graph.h"

/*** Constructors-Destructors ***/

#define WHITE 1
#define GRAY 2
#define BLACK 3

struct GraphObj{
   List *neigh;
   int *color;
   int *parent;
   int *distance;
   int order;
   int size;
   int source;
};

Graph newGraph(int n){
   Graph graph = malloc(sizeof(struct GraphObj));
   graph->neigh = calloc(n+1,sizeof(List));
   graph->color = calloc(n+1,sizeof(int));
   graph->parent = calloc(n+1,sizeof(int));
   graph->distance = calloc(n+1,sizeof(int));
   graph->order = n;
   graph->size = 0;
   graph->source = NIL;
   
   for (int i=0; i<n+1; i++){
      graph->neigh[i] = newList();
      graph->color[i] = WHITE;
      graph->parent[i] = NIL;
      graph->distance[i] = INF;
   }
   
   return graph;
}

void freeGraph(Graph* pG){
   Graph freed = *pG;
   
   for (int i=0; i<freed->order+1; i++){
      freeList(&(freed->neigh[i]));
   }
   
   free(freed->neigh);
   free(freed->color);
   free(freed->parent);
   free(freed->distance);
   free(*pG);
   *pG = NULL;
}

/*** Access functions ***/
int getOrder(Graph G){
   return G->order;
}

int getSize(Graph G){
   return G->size;
}

int getSource(Graph G){
   return G->source;
}

int getParent(Graph G, int u){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   return G->parent[u];
}

int getDist(Graph G, int u){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   if (getSource(G) == NIL){
      return INF;
   }
   return G->distance[u];
}

void getPath(List L, Graph G, int u){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   if (getSource(G) == NIL){
      printf("Graph Error: BFS() must be called before getPath\n");
      exit(1);
   }
   
   
   if (u == G->source){
      append(L, G->source);
   }
   else if (G->parent[u] == NIL){
      append(L, NIL);
   }
   else{
      getPath(L, G, G->parent[u]);
      append(L, u);
   }
   
}

/*** Manipulation procedures ***/
void makeNull(Graph G){
   for (int i=1; i <= G->order; i++){
      clear(G->neigh[i]);
   }
}

void addEdge(Graph G, int u, int v){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   if (v<1 || v>getOrder(G)){
      printf("Graph Error: int v not within bounds\n");
      exit(1);
   }
   
   addArc(G, u, v);
   addArc(G, v, u);
   G->size = G->size - 1;
   
}

void addArc(Graph G, int u, int v){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   if (v<1 || v>getOrder(G)){
      printf("Graph Error: int v not within bounds\n");
      exit(1);
   }
   
   
   moveFront(G->neigh[u]);
   while (index(G->neigh[u])>-1 && v>get(G->neigh[u])){
      moveNext(G->neigh[u]);
   }
   
   if (index(G->neigh[u]) == -1){
      append(G->neigh[u], v);
   }
   else{
      insertBefore(G->neigh[u], v);
   }
   
   G->size = G->size + 1;
}

void BFS(Graph G, int s){
   for (int i=1; i<G->order+1; i++){
      G->color[i] = WHITE;
      G->parent[i] = NIL;
      G->distance[i] = INF;
   }
   
   G->source = s;
   G->color[s] = GRAY;
   G->distance[s] = 0;
   G->parent[s] = NIL;
   
   List temp = newList();
   append(temp, s);
   int x = 0;
   
   while(length(temp) != 0){
      moveFront(temp);
      x = get(temp);
      delete(temp);
      
      List next = G->neigh[x];
      moveFront(next);
      
      while (index(next) != -1){
         int j = get(next);
         if (G->color[j] == WHITE){
            G->color[j] = GRAY;
            G->distance[j] = G->distance[x] + 1;
            G->parent[j] = x;
            append(temp, j);
         } 
         moveNext(next);

      }
      G->color[x] = BLACK;
   } 
   
   freeList(&temp); 
}

/*** Other operations ***/
void printGraph(FILE* out, Graph G){
   for (int i=1; i<=getOrder(G); i++){
      fprintf(out, "%d: ", i);
      printList(out, G->neigh[i]);
      fprintf(out, "\n");
   }
}

