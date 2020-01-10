 
public class MyLinkedList implements ListInterface {
   
   Node head;
   int size;
   
   // Returns true if the list is empty, false otherwise. 
	public boolean isEmpty(){
      if (size == 0){
         return true;
      }
      else {
         return false;
      }
   }
	// Returns the size of the list (number of items in the list)
	public int size(){
      return size;
   }

	// Adds an Object to the list at the specified index. 
	public void add(int index, Object value){
   
      if (index >= 0 && index <= size){
         Node newNode = new Node(value);
         if ( index == 0 ){
            newNode.next = head;
            head = newNode;
         }
         else {
            Node previous = head;
            Node curr = head.next;
            int i = 1;
            while (i <= index){
               if (i == index){
                  previous.next = newNode;
                  newNode.next = curr;
                  break;
               }
               previous = previous.next;
               curr = curr.next;
               i++;
            }
         }
         size ++;
      }
      else{  
		   throw new ListIndexOutOfBoundsException("Index " + index + " is out of boudns in add()");
      }
   }

	// Removes an item from the list at the specified index. 
	public void remove(int index){
      if ( index >= 0 && index < size){
         if ( index == 0 ) {
            head = head.next;
         }
         else {
            int i = 0;
            Node current = head;
            while ( i < index - 1){
               current = current.next;
               i++;
            }
            current.next = current.next.next;
         }
         size --;
      }
      else {
		   throw new ListIndexOutOfBoundsException(
         "Index " + index + " is out of bounds in remove()");
      }
   }
	// Removes all the items from the list. 
	public void removeAll(){
      size = 0;
      head = new Node();
      
   }

    // Returns the Object stored in the list at the specified index. 
	public Object get(int index){
      if (index >= 0 && index < size){
         Node current = head;
         int j = 0;
         while (j < index){
            current = current.next;
            j++;
         }
         return current.item;
      }
      else {
		   throw new ListIndexOutOfBoundsException(
            "Index " + index  + " is out of bounds in get()");
      }
   }
	// Returns the index at which an Object is stored in the list, -1 if it's not in the list.
	public int find(Object o){
      int found = -1;
      Node current = head;
      if (current == null){
         return -1;
      }
      Object holder = current.item;
      for( int i = 0; i < size; i++){  
         if(holder.equals(o)){
            found = i;
            return found;
         }
         else{         
            current = current.next;
            if (current != null){
               holder = current.item;
            }
            else{
               return -1;
            }
         }
      }
      return found;
   }
   
   public String toString(){
      Node current = head;
      int i = 0;
      String s = "(";
      if (size == 0){
         s = s + ")";
      }
      while (i < size){
         if (i == size - 1){
            s = s + current.item + ")";
         }
         else{
            s = s + current.item + ", ";
         }
         i++;
         current = current.next;
      }
      return s;
   }
}

class Node{
   Object item;
   Node next;
   
   Node (){
      item = null;
      next = null;
   }
   
   Node (Object i){
      item = i;
      next = null;
   }
   
   Node (Object i, Node nextNode){
      item = i;
      next = nextNode;
   }
} 
