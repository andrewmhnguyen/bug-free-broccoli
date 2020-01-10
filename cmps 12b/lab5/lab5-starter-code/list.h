#ifndef CMPS12B_LIST
#define CMPS12B_LIST

typedef struct node_type{
	/*
	* TODO 1
	*/
  struct node_type* next;
  void* data;
	/*
	* TODO 1
	*/
	
} Node;

typedef struct {
	
	/*
	* TODO 1
	*/
  Node* head;
  int size;
	/*
	* TODO 1
	*/
} List;

Node* make_node(void* data, Node* next);
List* make_list();

void free_node(Node* node);
void free_list(List* list);

void add(List* list, int index, void* data);
void* get(List* list, int index);
void set(List* list, int index, void* data);
void remove_node(List* list, int index);

#endif

