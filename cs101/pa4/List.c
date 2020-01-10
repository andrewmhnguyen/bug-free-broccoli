//Andrew Nguyen
//anguy224
//Programming Assignment 4

#include <stdio.h>
#include <stdlib.h>
#include "List.h"

typedef struct NodeObj {
   struct NodeObj* next;
   struct NodeObj* prev;
   int data;
} NodeObj;

typedef NodeObj* Node;

typedef struct ListObj{
  Node front;
  Node back;
  Node cursor;
  int length;
  int index;
} ListObj;

// Constructors/De-constructors -----------------------------------------------
Node newNode(int data, Node next, Node prev){
   Node node = malloc(sizeof(NodeObj));
   node->data = data;
   node->next = next;
   node->prev = prev;
   return node;
}

void freeNode(Node* pN) {
   if(pN != NULL && *pN != NULL) {
      free(*pN);
      *pN = NULL;
   }
}

List newList(void){
   List list = malloc(sizeof(ListObj));
   list->back = list->front = list->cursor = NULL;
   list->length = 0;
   list->index = -1; 
   return list;
}

void freeList(List* pL) {
   if(pL != NULL && *pL != NULL) { 
      Node temp = (*pL)->front; 
      while(temp != NULL) {
         Node dele = temp;
         temp = temp->next;
         free(dele);
         
      }
      
      free(*pL);
      *pL = NULL;
   }
}

// Access functions -----------------------------------------------------------
int length(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   return L->length;
}

int index(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   return L->index;
}

int front(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){
      return L->front->data;
   }
   else{
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
}

int back(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){
      return L->back->data;
   }
   else{
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
}


int get(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if(L->length<1){
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
   else if(L->index<0){
      printf("List Error: cursor isn't defined\n");
      exit(1);
   }
   else{
      return L->cursor->data;
   }
}

int equals(List A, List B){
   int eq = 0;
   Node N = NULL;
   Node M = NULL;
   
   if ( A==NULL || B==NULL ){
      printf( "List Error: calling equals() on NULL List reference\n" );
      exit(1);
   }
   
   eq = ( A->length == B->length );
   N = A->front;
   M = B->front;
   while ( eq && N!=NULL){
      eq = (N->data==M->data);
      N = N->next;
      M = M->next;
   }
   return eq;
}


// Manipulation procedures ----------------------------------------------------
void clear(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   Node temp = L->front;
   while (temp != NULL){
      Node clear = temp;
      temp = temp->next;
      free(clear);
   }

   L->front = L->back = L->cursor = NULL;
   L->length = 0;
   L->index = -1; 
}

void moveFront(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){
      L->cursor = L->front;
      L->index = 0;
   }
}

void moveBack(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){ 
      L->cursor = L->back;
      L->index = L->length - 1;
   }
}

void movePrev(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->cursor!=NULL && L->index!=0)
   {
      L->cursor = L->cursor->prev;
      L->index = L->index - 1;
   }
      
   else if (L->cursor!=NULL && L->index==0)
   {
      L->cursor = NULL;
      L->index = -1;
   }
}

void moveNext(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->cursor!=NULL && L->index!=L->length-1)
   {
      L->cursor = L->cursor->next;
      L->index = L->index + 1;
   }
      
   else if (L->cursor!=NULL && L->index==L->length-1)
   {
      L->cursor = NULL;
      L->index = -1;
   }
}

void prepend(List L, int data){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   Node temp = newNode(data, NULL, NULL);
   if (L->length>0){
      temp->next = L->front;
      L->front->prev = temp;
      L->front = temp;
      L->index = L->index + 1;
      L->length = L->length + 1;
   }
   else{
      L->back = temp;
      L->front = temp;
      L->length = L->length + 1;
   }
}

void append(List L, int data){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   Node temp = newNode(data, NULL, NULL);
   if (L->length>0){
      temp->prev = L->back;
      L->back->next = temp;
      L->back = temp;
      L->length = L->length + 1;
   }
   else{
      L->front = temp;
      L->back = temp;
      L->length = L->length + 1;
   }
}

void insertBefore(List L, int data){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   
   if (L->index<0){
      printf("List Error: cursor isn't defined\n");
      exit(1);
   }
   else if (L->length<1){
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
      
   Node temp = newNode(data, NULL, NULL);
   if (L->cursor->prev== NULL){
      L->front = temp;
      L->cursor->prev = temp;
      temp->next = L->cursor;
      L->length = L->length + 1;
      L->index = L->index + 1;
   }
   else{  
      temp->next = L->cursor;
      temp->prev = L->cursor->prev;
      L->cursor->prev->next = temp;
      L->cursor->prev = temp;
      L->length = L->length + 1;
      L->index = L->index + 1;
   }
}

void insertAfter(List L, int data){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   
   if (L->index<0){
      printf("List Error: cursor isn't defined\n");
      exit(1);
   }
   else if (L->length<1){
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
      
   Node temp = newNode(data, NULL, NULL);
   if (L->cursor->next== NULL){
      L->back = temp;
      L->cursor->next = temp;
      temp->prev = L->cursor;
      L->length = L->length + 1;
   }
   else{  
      temp->next = L->cursor->next;
      temp->prev = L->cursor;
      L->cursor->next->prev = temp;
      L->cursor->next = temp;
      L->length = L->length + 1;
   }
   

}

void deleteFront(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   
   if (L->length<1){
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
   
   Node temp = L->front;
	L->front = L->front->next;
   
	if(L->front == NULL){
		L->back = NULL;
	}
	else{
		L->front->prev = NULL;
	}
   
   if(L->index>=0){
      L->index = L->index - 1;
   }
   
   L->length = L->length - 1;
	freeNode(&temp);
}


void deleteBack(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length<1){
      printf("List Error: cannot be called on an empty list \n");
      exit(1);
   }
   Node temp = L->back;
   if (L->length == 1){
      if (L->cursor == L->back){
         L->cursor = NULL;
         L->index = -1;
      }
      L->back = NULL;
      L->length = L->length - 1;
   }
   else{
      if (L->cursor == L->back){
         L->cursor = NULL;
         L->index = -1;
      }
      L->back = L->back->prev;
      L->back->next = NULL;
      L->length = L->length - 1;
   }
   freeNode(&temp);
   
   
}

void delete(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->index<0){
      printf("List Error: cursor isn't defined\n");
      exit(1);
   }
   else if (L->length<1){
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
   
   if (L->cursor == L->back){
      deleteBack(L);
   }
   else if (L->cursor == L->front){
      deleteFront(L);
   }
   else{
      Node temp = L->cursor;
      L->cursor->prev->next = L->cursor->next;
      L->cursor->next->prev = L->cursor->prev;
      freeNode(&temp);
      L->cursor = NULL;
      L->index = -1;
      L->length = L->length - 1;   
   }
}

// Other operations -----------------------------------------------------------
void printList(FILE* out, List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   
   Node temp = L->front;
	while(temp != NULL) {
		fprintf(out, "%d ", temp->data);
		temp = temp->next;
	}
}

List copyList(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   
   List copy = newList();
   Node temp = L->front;
   for (int i=0; i<L->length; i++){
      if (copy == NULL){
         break;
      }
      append(copy, temp->data);
      temp = temp->next;
   }
   return copy;
}
