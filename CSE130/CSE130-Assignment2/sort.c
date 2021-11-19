#include "merge.h"
#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int gleft;
int gright;
int mid;
int left_mid;
int right_mid;
pthread_t thread_id1;
pthread_t thread_id2;
pthread_t thread_id3;

/* LEFT index and RIGHT index of the sub-array of ARR[] to be sorted */
void singleThreadedMergeSort(int arr[], int left, int right) 
{
  if (left < right) {
    int middle = (left+right)/2;
    singleThreadedMergeSort(arr, left, middle); 
    singleThreadedMergeSort(arr, middle+1, right); 
    merge(arr, left, middle, right); 
  } 
}

/* 
 * This function stub needs to be completed
 */
void *leftright(void *input){
  left_mid = (gleft+mid)/2;
  int *var= input;
  singleThreadedMergeSort(var, left_mid+1, mid);
  pthread_exit(NULL);
}

void *rightleft(void *input){
  int *var= input;
  right_mid = (gright+mid+1)/2;
  singleThreadedMergeSort(var, mid+1, right_mid);
  pthread_join(thread_id3, NULL);
  merge(var, mid+1, right_mid, gright);
  pthread_exit(NULL);
}

void *rightright(void *input){
  right_mid = (gright+mid+1)/2;
  int *var= input;
  singleThreadedMergeSort(var, right_mid+1, gright);
  pthread_exit(NULL);
}

void multiThreadedMergeSort(int arr[], int left, int right) 
{
  // Your code goes here
  gleft = left;
  gright = right;
  mid = (gleft+gright)/2;
  left_mid = (gleft+mid)/2;

  pthread_create(&thread_id1, NULL, leftright, (void *) arr);
  pthread_create(&thread_id2, NULL, rightleft, (void *) arr);
  pthread_create(&thread_id3, NULL, rightright, (void *) arr);
  singleThreadedMergeSort(arr, left, left_mid);
  pthread_join(thread_id1, NULL);
  merge(arr, left, left_mid, mid);
  pthread_join(thread_id2, NULL);
  merge(arr, gleft, mid, gright);
}


