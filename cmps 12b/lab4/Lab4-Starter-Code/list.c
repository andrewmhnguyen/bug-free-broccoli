#include <stdlib.h>
#include "list.h"
#include <stdio.h>
#include <assert.h>

//makes a node with data and sets a node to connect to 
Node* make_node(void* data, Node* next){
	/* 
	* TODO 2
	*/ 
  Node* makeNode = calloc(1,sizeof(Node));
  makeNode -> newData = data;
  makeNode -> newNext = next;
  return makeNode;
	/* 
	* TODO 2
	*/ 
}

//makes a list of size 0 and sets a head as null
List* make_list(){
	/* 
	* TODO 2
	*/ 
  List* newList = calloc(1,sizeof (List));
  newList -> size = 0;
  newList -> head = NULL;	
  return newList;
	/* 
	* TODO 2
	*/ 
}

//frees a node and if the node has data, frees that data too 
void free_node(Node* node){
	
	/* 
	* TODO 2
	*/
  
  if (node-> newData != NULL){
    free(node->newData);
  } 
  free(node);
	/* 
	* TODO 2
	*/ 
}

//iterates through a list and frees the nodes and finally frees the list at the end
void free_list(List* list) {
	
	/* 
	* TODO 2
	*/ 
  for(int i = 0;i<list->size;i++){
    Node* current = list->head;
    Node* newHead = current->newNext;
    free_node(list->head);
    list->head = newHead;
    
  }
  free(list);
	/* 
	* TODO 2
	*/ 
}

//adds items to list at index with data
void add(List* list, int index, void* data) {
	
	/* 
	* TODO 2
	*/ 
  assert( !(index > list->size || index < 0) && "Index was out of bounds");

  Node* currentNode = list->head;

  //iterates to correct index
  for(int i = 0; i < index-1; i++){
    currentNode = currentNode->newNext;
  }
  
  //determining where to add deciding on the index 
  //at the start of the list
  if(index==0){
    Node* newNode = calloc(1,sizeof(Node));
    newNode->newData = data;
    newNode->newNext = list->head;
    list->head = newNode;
  }
  //at the end of the list
  else if(index == list->size){
    Node* newNode = calloc(1,sizeof(Node));
    newNode->newData = data;
    newNode->newNext = NULL;
    currentNode->newNext=newNode;
  }
  //in the middle of the list
  else{
    Node* newNode = calloc(1,sizeof(Node));
    newNode->newNext = currentNode->newNext;
    currentNode->newNext = newNode;
  }
  
  int size = list->size +1;
  list->size = size;
	/* 
	* TODO 2
	*/ 
}

//gets item at the index
void* get(List* list, int index){
	/* 
	* TODO 2
	*/ 
  assert( !(index > list->size || index < 0) && "Index was out of bounds");
  Node* currentNode = list->head;
  int i =0; 
  //iterates to correct index
  while(i<index){
    currentNode = currentNode->newNext;
    i++; 
  }
  return currentNode->newData;
	/* 
	* TODO 2
	*/ 
}

//sets item in the list at the index with the data
void set(List* list, int index, void* data) {
	
	/* 
	* TODO 2
	*/ 
  assert( !(index > list->size || index < 0) && "Index was out of bounds");
  Node* currentNode = list->head;
  //iterates to correct index
  for(int i =0; i < index; i++){
    currentNode = currentNode->newNext;
  }
  currentNode->newData = data;
	/* 
	* TODO 2
	*/ 
}
