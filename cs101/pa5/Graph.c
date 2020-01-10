//Andrew Nguyen
//anguy224
//Programming Assignment 5

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
   int *discover;
   int *finish;
   int order;
   int size;
};

Graph newGraph(int n){
   Graph graph = malloc(sizeof(struct GraphObj));
   graph->neigh = calloc(n+1,sizeof(List));
   graph->color = calloc(n+1,sizeof(int));
   graph->parent = calloc(n+1,sizeof(int));
   graph->discover = calloc(n+1,sizeof(int));
   graph->finish = calloc(n+1, sizeof(int));
   graph->order = n;
   graph->size = 0;
   
   for (int i=0; i<n+1; i++){
      graph->neigh[i] = newList();
      graph->color[i] = WHITE;
      graph->parent[i] = NIL;
      graph->discover[i] = UNDEF;
	  graph->finish[i] = UNDEF;
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
   free(freed->discover);
   free(freed->finish);
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

int getParent(Graph G, int u){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   return G->parent[u];
}

int getDiscover(Graph G, int u){
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   return G->discover[u];
}

int getFinish(Graph G, int u){
   if (G == NULL){
	   printf("Graph Error: graph is null\n");
	   exit(1);
   }
   if (u<1 || u>getOrder(G)){
      printf("Graph Error: int u not within bounds\n");
      exit(1);
   }
   return G->finish[u];
}

/*** Manipulation procedures ***/
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

void Visit(Graph G, List S, int u, int *time){
	G->color[u] = GRAY;
	G->discover[u] = ++*time;
	moveFront(G->neigh[u]);
	while (index(G->neigh[u])>=0){
		int temp = get(G->neigh[u]);
		if (G->color[temp] == WHITE){
			G->parent[temp] = u;
			Visit(G, S, temp, time);
		}
		moveNext(G->neigh[u]);
	}
	G->color[u] = BLACK;
	G->finish[u] = ++*time;
	prepend(S, u);
}

void DFS(Graph G, List S){
	if (length(S) != getOrder(G)){
		printf("Graph Error: sizes not matching\n");
		exit(1);
	}
	
	for (int i=1; i<=getOrder(G); i++){
		G->color[i] = WHITE;
		G->parent[i] = NIL;
		G->discover[i] = UNDEF;
		G->finish[i] = UNDEF;
	}	

	int time = 0;
	moveFront(S);
	
	while (index(S)>=0){
		int temp = get(S);
		if (G->color[temp] == WHITE){
			Visit(G, S, temp, &time);
		}
		moveNext(S);
	}

	for (int size = length(S)/2; size>0; size--){
		deleteBack(S);
	}
}

/*** Other operations ***/
void printGraph(FILE* out, Graph G){
   for(int i = 1; i <= getOrder(G); ++i) {
		fprintf(out, "%d: ", i);
		printList(out, G->neigh[i]);
		fprintf(out, "\n");
	}
}

Graph copyGraph(Graph G){
	Graph copy = newGraph(getOrder(G));
	for (int i=1; i <= getOrder(G); i++){
		moveFront(G->neigh[i]);
		while (index(G->neigh[i])>=0){
			addArc(copy, i, get(G->neigh[i]));
			moveNext(G->neigh[i]);
		}
	}
	return copy;
}

Graph transpose(Graph G){
	Graph trans = newGraph(getOrder(G));
	for (int i=1; i<=getOrder(G); i++){
		moveFront(G->neigh[i]);
		while (index(G->neigh[i])>=0){
			addArc(trans, get(G->neigh[i]), i);
			moveNext(G->neigh[i]);
		}
	}
	return trans;
}