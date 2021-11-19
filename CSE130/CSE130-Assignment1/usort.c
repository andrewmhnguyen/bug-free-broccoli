/************************************************************************
 * 
 * CSE130 Winter 2021 Assignment 1
 * 
 * UNIX Shared Memory Multi-Process Merge Sort
 * 
 * Copyright (C) 2020-2021 David C. Harrison. All right reserved.
 *
 * You may not use, distribute, publish, or modify this code without 
 * the express written permission of the copyright holder.
 *
 ************************************************************************/

#include "merge.h"
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>



/* LEFT index and RIGHT index of the sub-array of ARR[] to be sorted */
void singleProcessMergeSort(int arr[], int left, int right) 
{
  if (left < right) {
    int middle = (left+right)/2;
    singleProcessMergeSort(arr, left, middle); 
    singleProcessMergeSort(arr, middle+1, right); 
    merge(arr, left, middle, right); 
  } 
}

/* 
 * This function stub needs to be completed
 */
void multiProcessMergeSort(int arr[], int left, int right) 
{
  // Your code goes here 

  // create shared memory
  int shmid = shmget(IPC_PRIVATE, 1024, 0666|IPC_CREAT);

  // attach to shared memory
  int *shm = (int*) shmat(shmid, (void*)0,0);

  //copy the array into shared memory 
  int middle = (left+right)/2;

  for(int i=left; i<=right; i++){
    shm[i] = arr[i];
  }

  switch (fork()){
    case -1:
      exit(-1);
    case 0:
      shm = (int*) shmat(shmid, (void*)0,0);
      singleProcessMergeSort(shm, left, middle);
      shmdt(shm);
      exit(-1);
    default:
      singleProcessMergeSort(shm, middle+1, right);
      wait(NULL);

      merge(shm, left, middle, right);

      for (int i = left; i<=right; i++){
        arr[i] = shm[i];
      }
      shmdt(shm);
      shmctl(shmid,IPC_RMID,NULL);
  }
}
