#include <stdlib.h>
#include <stdio.h>
#include "Dictionary.h"
#include "list.h"


typedef struct DictionaryObj {
   int tableSize;
   int size;
   List** table;
} DictionaryObj;


typedef struct EntryObj {
   char* key;
   char* value;
} EntryObj;

// allows EntryObj* to be called Entry in this file
typedef struct EntryObj* Entry;

/*
 *
 * YOUR FUNCTION IMPLEMENTATIONS GO BELOW HERE
 *
*/

//newEntry creation
Entry newEntry(char* key, char* value){
  Entry entry = (Entry)calloc(1,sizeof(EntryObj));
   entry->key = key;
   entry->value = value;
   return entry;
}
   
//frees an entry
void freeEntry(Entry* pE){
   free(pE);
}


//allocates space for a new dictionary, intializes variables and returns it
Dictionary newDictionary(int tableSize){
   Dictionary insert = malloc(sizeof(DictionaryObj));
   insert->tableSize = tableSize;
   insert->size = 0;
   insert->table = calloc(tableSize, sizeof(List*));
   return insert;
}

//frees all data associated with the dictionary 
void freeDictionary(Dictionary* pD){
  makeEmpty((*pD));
  for(int i = 0; i < (*pD)->tableSize; i++){
    if((*pD)->table[i] != NULL){
    free_list((*pD)->table[i]);
    }
  }
   free((*pD)->table);
   free((*pD));
}

//returns an int - 1 is true, 0 is false
int isEmpty(Dictionary D){
   if(D->size == 0){
      return 1;
   }
   return 0;
}

//returns number of key/value pairs in D
int size(Dictionary D){
   return D->size;
}

//adds a new key/value pair into the dictionary
void insert(Dictionary D, char* key, char* value){
   int arrayIndex = hash(D, key);
   if(D->table[arrayIndex]==NULL&&lookup(D, key)==NULL){
     D->table[arrayIndex] = make_list();
     add(D->table[arrayIndex], 0, newEntry(key,value));
     D->size = D->size + 1;
   }
   else if(D->table[arrayIndex]!=NULL && lookup(D, key) == NULL){
     add(D->table[arrayIndex],0,newEntry(key,value));
     D->size = D->size + 1;
   }
   else{
      for(int i = 0; i < D->table[arrayIndex]->size; i++){
         Entry oldEntry = get(D->table[arrayIndex], i);
         if(key == oldEntry->key){
	   freeEntry(get(D->table[arrayIndex],i));
           set(D->table[arrayIndex], i, newEntry(key,value));
         }
      }
   }
}

//returns value in Dictionary D associated with key
char* lookup(Dictionary D, char* key){
   int arrayIndex = hash(D, key);
   if(D->table[arrayIndex] == NULL){
      return NULL;
   }
   else {
      for(int i = 0; i < D->table[arrayIndex]->size; i++){
         Entry oldEntry = get(D->table[arrayIndex], i);
         if(key == oldEntry->key){
            return oldEntry->value;
         }
      }
      return NULL;
   }
}

//removes entry associated with key
void delete(Dictionary D, char* key){
   int arrayIndex = hash(D, key);
   if(D->table[arrayIndex] != NULL){
      for(int i = D->table[arrayIndex]->size - 1; i >= 0; i--){
         Entry oldEntry = get(D->table[arrayIndex], i);
	 if(oldEntry!=NULL){
	   if(oldEntry->key == key){
	     freeEntry(get(D->table[arrayIndex],i));
	     remove_node(D->table[arrayIndex],i);
	     D->size = D->size - 1;
	   }
	 }
      }
   }
}

//removes all entries from Dictionary D
void makeEmpty(Dictionary D){
  for(int i=0; i<D->tableSize;i++){
    if(D->table[i]!= NULL){
       for(int j=0; j<D->table[i]->size; j++){
	 Entry entry = get(D->table[i],j);
          if(entry!=NULL){
             delete(D, entry->key);
          }
       }
    }
  }
}

//prints content of dictionary D to a file 
void printDictionary(FILE* out, Dictionary D){
  for(int tableIndex = 0; tableIndex < D->tableSize; tableIndex++){
    if(D->table[tableIndex]!=NULL){
      List* bucket = D->table[tableIndex];
      for(int listIndex = 0; listIndex < bucket->size; listIndex++){
	Entry entry = get(bucket, listIndex);
	fprintf(out,"%s %s \n", entry->key, entry->value);
      }
    }
  }
}

/*
 *
 * YOUR FUNCTION IMPLEMENTATIONS GO ABOVE HERE
 *
*/

/*
 * YOUR CODE GOES ABOVE THIS COMMENT
 * DO NOT ALTER THESE FUNCTIONS
 * THESE ARE THE THREE FUNCTIONS THAT WILL ALLOW YOU TO CONVERT 
 * A STRING INTO A VALID ARRAY INDEX
 * YOU WILL ONLY NEED TO CALL hash(Dictionary D, char* key)
*/

// rotate_left()
// rotate the bits in an unsigned int
unsigned int rotate_left(unsigned int value, int shift) {
   int sizeInBits = 8*sizeof(unsigned int);
   shift = shift & (sizeInBits - 1);
   if ( shift == 0 ) {
      return value;
   }
   return (value << shift) | (value >> (sizeInBits - shift));
}

// pre_hash()
// turn a string into an unsigned int
unsigned int pre_hash(char* input) { 
   unsigned int result = 0xBAE86554;
   while (*input) { 
      result ^= *input++;
      result = rotate_left(result, 5);
   }
   return result;
}

// hash()
// turns a string into an int in the range 0 to tableSize-1
int hash(Dictionary D, char* key){
   return pre_hash(key) % D->tableSize;
}
