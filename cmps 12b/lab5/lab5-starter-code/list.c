#include <stdlib.h>
#include "list.h"
#include <stdio.h>

Node* make_node(void* data, Node* next){
	Node* node = calloc(1,sizeof(Node));
	node->data = data;
	node->next = next;
	return node;
}

List* make_list(){
	List* list = calloc(1,sizeof(List));
	list->head = NULL;
	list->size = 0;
	return list;
}

void free_node(Node* node){
    if(node != NULL){
        free(node->data);
    }
	free(node);
}

void free_list(List* list) {
	Node* current = list->head;
	
	while (current != NULL){
		Node* next = current->next;
		
		free_node(current);
		current = next;		
	}
	free(list);
	}

void add(List* list, int index, void* data) {
	Node* current = list-> head;
	list->size++;
	if (index == 0){
		list->head = make_node(data,current);
	}
	else {
		while (index-1 > 0){
			current = current->next;
			index--;
		}
		current->next = make_node(data,current->next);
	}
}

void* get(List* list, int index){
	Node* current = list->head;
	
	while (index != 0){
		current = current->next;
		index--;
	}
	return current->data;
}

void remove_node(List* list, int index){
	
	
	if (index == 0){
		Node* to_remove = list->head;
		list->head = list->head->next;

		free(to_remove);
	}
	else {
		Node* current = list->head;
		
		while (index > 1){
			current = current->next;
			index--;
		}
		Node* to_remove = current->next;
		current->next = current->next->next;
		free(to_remove);
	}
	list->size--;
}

void set(List* list, int index, void* data){
	Node* current = list->head;
	
	while (index != 0){
		current = current->next;
		index--;
	}
	current->data = data;
}
