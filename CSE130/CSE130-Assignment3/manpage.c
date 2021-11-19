
/*********************************************************************
 *
 * Copyright (C) 2020-2021 David C. Harrison. All right reserved.
 *
 * You may not use, distribute, publish, or modify this code without 
 * the express written permission of the copyright holder.
 *
 ***********************************************************************/

#include "manpage.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <semaphore.h>
#include <time.h>
#include <assert.h>
#include <errno.h>
#include <signal.h>
#include <pthread.h>
sem_t sems[7];

/*
 * See manpage.h for details.
 *
 * As supplied, shows random single messages.
 */

void *thread_fun(void *arg){
  int pid = getParagraphId();
  if (pid > 0){
    //wait for semaphore for paragraph i - 1 to go up
    sem_wait(&sems[pid-1]);
  }
  showParagraph();
  if (pid < 6){
    //put flag for i up 
    sem_post(&sems[pid]);
  }
  pthread_exit(NULL);
  return NULL;
}

void manpage() 
{
  pthread_t threads[7];
  //initialize semaphores
  for (int i = 0; i < 7; i++){
    sem_init(&sems[i], 0, 0);
  }
  //create all threads
  for (int i = 0; i < 7; i++){
    pthread_create(&threads[i], NULL, thread_fun, NULL);
  }
  //wait for all threads to finish 
  for (int i = 0; i < 7; i++){
    pthread_join(threads[i], NULL);
  }
  
}
