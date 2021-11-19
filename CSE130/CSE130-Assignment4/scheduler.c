/**
 * See scheduler.h for function details. All are callbacks; i.e. the simulator 
 * calls you when something interesting happens.
 */
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>


#include "simulator.h"
#include "scheduler.h"


//list implementation taken from code that I wrote during CS101
typedef struct ListObj* List;
// Constructors-Destructors ---------------------------------------------------
List newList(void);
void freeList(List* pL);

// Access functions -----------------------------------------------------------
int length(List L);
thread_t* front(List L);
thread_t* back(List L);
thread_t* get(List L);

// Manipulation procedures ----------------------------------------------------
void clear(List L);
void moveFront(List L);
void moveBack(List L);
void movePrev(List L);
void moveNext(List L);
void prepend(List L, thread_t *t);
void append(List L, thread_t *t);
void insertBefore(List L, thread_t *t);
void insertAfter(List L, thread_t *t);
void deleteFront(List L);
void deleteBack(List L);
void delete(List L);

// Other operations -----------------------------------------------------------
List copyList(List L);

typedef struct NodeObj {
   struct NodeObj* next;
   struct NodeObj* prev;
   thread_t *t;
   int arr_time;
   int scp_time;
   int ecp_time;
   int scp2_time;
   int sio_time;
   int eio_time;
   int dep_time;
   int turn_time;
   int wait_time;
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
Node newNode(thread_t *t, Node next, Node prev){
   Node node = malloc(sizeof(NodeObj));
   node->t = t;
   node->next = next;
   node->prev = prev;
   node->arr_time = -1;
   node->scp_time = -1;
   node->ecp_time = -1;
   node->scp2_time = -1;
   node->sio_time = -1;
   node->eio_time = -1;
   node->dep_time = -1;
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

thread_t* front(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){
      return L->front->t;
   }
   else{
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
}

thread_t* back(List L){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   if (L->length>0){
      return L->back->t;
   }
   else{
      printf("List Error: cannot be called on an empty list\n");
      exit(1);
   }
}


thread_t* get(List L){
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
      return L->cursor->t;
   }
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

void prepend(List L, thread_t *t){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   Node temp = newNode(t, NULL, NULL);
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

void append(List L, thread_t *t){
   if (L == NULL){
      printf("List Error: cannot call on NULL list reference\n");
      exit(1);
   }
   Node temp = newNode(t, NULL, NULL);
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

void insertBefore(List L, thread_t *t){
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
      
   Node temp = newNode(t, NULL, NULL);
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

void insertAfter(List L, thread_t *t){
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
      
   Node temp = newNode(t, NULL, NULL);
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

   if (L->cursor == L->front){
      L->cursor = NULL;
      L->index = -1;
   }

   if (L->length != 1){
      L->front = L->front->next;
      L->front->prev = NULL;
      L->length = L->length - 1;
      if(L->index>=0){
         L->index = L->index - 1;
      }
   }
   else{
      L->front = NULL;
      L->back = NULL;
      L->cursor = NULL;
      L->index = -1;
      L->length = 0;
   }
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
      if( L->cursor == L->back){
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
      append(copy, temp->t);
      temp = temp->next;
   }
   return copy;
}

bool list = false;
bool runt = false;

List ready_list;
List time_list;

void scheduler(enum algorithm algorithm, unsigned int quantum) { }

void sim_tick() { }

void sys_exec(thread_t *t) { 
   //if ready_list is null, initialize it
   if (list == false){
      ready_list = newList();
      time_list = newList();
      list = true;
   }

   //time that thread arrives at cpu
   append(time_list, t);
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->arr_time = sim_time();
      }
      temp = temp->next;
   }

   //if no thread is running - dispatch it
   if (runt == false){
      runt = true;
      Node temp = time_list->front;
      for (int i=0; i<time_list->length; i++){
         if (t == temp->t){
            if (temp->scp_time == -1){
               temp->scp_time = sim_time();
            }
            else{
               temp->scp2_time = sim_time();
            }
         }
         temp = temp->next;
      }
      sim_dispatch(t);
   }
   //if not, put it on the ready queue 
   else {
      append(ready_list, t);
   }
   
}

void sys_read(thread_t *t) { 
   //take thread off of processor for io
   //means that a different thread can go onto processor 
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->ecp_time = sim_time();
      }
      temp = temp->next;
   }
   runt = false;
   //check if ready queue is empty -> if not, dispatch first thread on ready queue
   if (length(ready_list)!=0){
      runt = true;
      thread_t *s = front(ready_list);
      deleteFront(ready_list);
      Node temp = time_list->front;
      for (int i=0; i<time_list->length; i++){
         if (s == temp->t){
            if (temp->scp_time == -1){
               temp->scp_time = sim_time()+1;
            }
            else{
               temp->scp2_time = sim_time()+1;
            }
         }
         temp = temp->next;
      }
      sim_dispatch(s);
   }
}

void sys_write(thread_t *t) { 
   //take thread off of processor for io 
   //means that a different thread can go onto processor
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->ecp_time = sim_time();
      }
      temp = temp->next;
   }
   runt = false;
   //check if ready queue is empty -> if not, dispatch first thread on ready queue
   if (length(ready_list)!=0){
      runt = true;
      thread_t *s = front(ready_list);
      deleteFront(ready_list);
      Node temp = time_list->front;
      for (int i=0; i<time_list->length; i++){
         if (s == temp->t){
            if (temp->scp_time == -1){
               temp->scp_time = sim_time()+1;
            }
            else{
               temp->scp2_time = sim_time()+1;
            }
         }
         temp = temp->next;
      }
      sim_dispatch(s);
   }
}

void sys_exit(thread_t *t) { 
   //thread completed
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->dep_time = sim_time();
      }
      temp = temp->next;
   }

   runt = false;
   //check if ready queue is empty -> if not, dispatch first thread on ready queue
   if (length(ready_list)!=0){
      runt = true;
      thread_t *s = front(ready_list);
      deleteFront(ready_list);
      Node temp = time_list->front;
      for (int i=0; i<time_list->length; i++){
         if (s == temp->t){
            if (temp->scp_time == -1){
               temp->scp_time = sim_time()+1;
            }
            else{
               temp->scp2_time = sim_time()+1;
            }
         }
         temp = temp->next;
      }
      sim_dispatch(s);
   }
}

void io_complete(thread_t *t) { 
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->eio_time = sim_time();
      }
      temp = temp->next;
   }
   //if no thread is running - dispatch it
   if (runt == false){
      runt = true;
      Node temp = time_list->front;
      for (int i=0; i<time_list->length; i++){
         if (t == temp->t){
            if (temp->scp_time == -1){
               temp->scp_time = sim_time()+1;
            }
            else{
               temp->scp2_time = sim_time()+1;
            }
         }
         temp = temp->next;
      }
      sim_dispatch(t);
   }
   //if not, put it on the ready queue 
   else {
      append(ready_list, t);
   }
}

void io_starting(thread_t *t) {
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      if (t == temp->t){
         temp->sio_time = sim_time();
      }
      temp = temp->next;
   }
 }

stats_t *stats() { 
   int thread_count = length(time_list);
   stats_t *stats = malloc(sizeof(stats_t));
   stats->tstats = malloc(sizeof(stats_t)*thread_count);

   for(int i = 0; i<length(time_list); i++){
      stats->tstats[i].tid = i+1;

      Node temp = time_list->front;
      for (int j=0; j<time_list->length; j++){
         if (stats->tstats[i].tid == temp->t->tid){
            temp->turn_time = temp->dep_time - temp->arr_time + 1;
            stats->tstats[i].turnaround_time = temp->turn_time;
            if (temp->scp2_time == -1){
               temp->wait_time = temp->scp_time - temp->arr_time;
               stats->tstats[i].waiting_time = temp->wait_time;
            }
            else{
               temp->wait_time = (temp->scp_time - temp->arr_time) + (temp->sio_time - temp->ecp_time - 1) + (temp->scp2_time - temp->eio_time -1);
               stats->tstats[i].waiting_time = temp->wait_time;
            }
         }
         temp = temp->next;
      }
   }

   stats->thread_count = thread_count;
   int turnaround = 0;
   Node temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      turnaround = turnaround + temp->turn_time;
      temp = temp->next;
   }
   stats->turnaround_time = turnaround/thread_count;

   int wait = 0;
   temp = time_list->front;
   for (int i=0; i<time_list->length; i++){
      wait = wait + temp->wait_time;
      temp = temp->next;
   }
   stats->waiting_time = wait/thread_count;

   return stats;
}

