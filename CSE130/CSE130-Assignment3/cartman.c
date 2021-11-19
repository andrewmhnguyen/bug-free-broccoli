
#include "cartman.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <semaphore.h>
#include <time.h>
#include <assert.h>
#include <errno.h>
#include <signal.h>
#include <pthread.h>
#include <stdbool.h>
#include <time.h>

sem_t sems[10];
pthread_t threads[5];
int count = 0;
/*
 * You need to implement this function, see cartman.h for details 
 */
// cartman informed of arrival and must ensure safe transit across the critical section
// using the reserve function 
struct carts {
    unsigned int cart1;
    enum junction junction1;
    enum track track1;
};


void *thread_func(void *arg){
  struct carts *carte = arg;
  unsigned int cart = carte->cart1;
  enum junction junction = carte->junction1;
  enum track track = carte->track1;

  sem_wait(&sems[track+5]); 
  count++;


  if (count == 1){
    if (track == 0){
      sem_wait(&sems[6]);
      sem_wait(&sems[9]);
    } else if (track == 4){
      sem_wait(&sems[5]);
      sem_wait(&sems[8]);
    } else {
      sem_wait(&sems[track+4]);
      sem_wait(&sems[track+6]);
    }
  }
  
  sem_wait(&sems[junction]);
  reserve(cart, junction);
  
  int junc = junction;
  int trac = track;

  if (junc==trac){
    if (junction<4){
      sem_wait(&sems[junction+1]);
      reserve(cart, junction+1);

    } 
    else {
      sem_wait(&sems[0]);
      reserve(cart, 0);
    }
  }
  else {
    if (junction>0){
      sem_wait(&sems[junction-1]);
      reserve(cart, junction-1);
    } 
    else {
      sem_wait(&sems[4]);
      reserve(cart, 4);
    }
  }
  cross(cart, track, junction);
  
  pthread_exit(NULL);
}

void arrive(unsigned int cart, enum track track, enum junction junction) 
{
  struct carts *carter;
  carter = malloc(sizeof(*carter));
  carter->cart1 = cart;
  carter->junction1 = junction;
  carter->track1 = track;
  //create a thread for the cart
  pthread_create(&threads[junction], NULL, thread_func, carter);
}
/*
 * You need to implement this function, see cartman.h for details 
 */
// once across critical section of track, should be invoked to let cartman know the cart is safely across
// junction is then marked available again by calling release 
void depart(unsigned int cart, enum track track, enum junction junction) 
{
  release(cart, junction);
  sem_post(&sems[junction]);
  //release the two junctions that have been reserved previously 
  int junc = junction;
  int trac = track;
  if (junc == 0 && trac == 4){
    junc = 5;
  }
  if (junc>trac){
    if (junction>0){
      release(cart, junction-1);
      sem_post(&sems[junction-1]);
    }
    else{
      release(cart, 4);
      sem_post(&sems[4]);
    }
  }
  else {
    if (junction<4){
      release(cart, junction+1);
      sem_post(&sems[junction+1]);
    }
    else{
      release(cart, 0);
      sem_post(&sems[0]);
    }
  }
  count--;
  if (count == 0){
    for (int i=5; i<10; i++){
      sem_post(&sems[i]);
    }
  }
}

/*
 * You need to implement this function, see cartman.h for details 
 */
void cartman() 
{
  //initialize semaphores
  for (int i = 0; i < 10; i++){
    sem_init(&sems[i], 0, 1);
  }
}

