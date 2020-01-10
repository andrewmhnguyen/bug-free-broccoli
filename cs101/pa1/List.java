//Andrew Nguyen
//anguy224
//Program Assignment 1

public class List{   
   private class Node{
      int data;
      Node prev;
      Node next;
      
      // Constructor
      Node(int data, Node prev, Node next)
      {
         this.data = data;
         this.prev = prev;
         this.next = next;
      }
   
      public String toString()
      {
         return String.valueOf(data);
      }
      
      public boolean equals(Object x)
      {
         boolean equal = false;  
         if(x instanceof Node)
         {
            Node compare = (Node) x;
            if (this.data == compare.data)
            {
               equal = true;
            }
         }
         return equal;
      }
   }
   
   private Node front;
   private Node back;
   private Node cursor;
   private int length;
   private int index;
   
   //Constructor
   List() // Creates a new empty list.
   {
      front = null;
      back = null;
      cursor = null;
      length = 0;
      index = -1;
   }
   
   // Access functions
   int length() // Returns the number of elements in this List.
   {
      return length;
   }
   
   int index() // If cursor is defined, returns the index of the cursor element,
    // otherwise returns -1.
   {
      return index;
   }
   
   int front() // Returns front element. Pre: length()>0
   {
      int check = length;
      if (check>0)
      {
         return front.data;
      }
      else
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
      }
   }
   
   int back() // Returns back element. Pre: length()>0
   {
      int check = length;
      if (check>0)
      {
         return back.data;
      }
      else
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
      }
   }
   
   int get() // Returns cursor element. Pre: length()>0, index()>=0
   {
      int check = length;
      int check2 = index;
      if (check<1)
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
         
      }
      else if (check2<0)
      {
         throw new RuntimeException("List Error: cursor isn't defined");
      }
      else
      {
         return cursor.data;
      }
   }
   
   boolean equals(List L) // Returns true if and only if this List and L are the same
    // integer sequence. The states of the cursors in the two Lists
    // are not used in determining equality.
   {
      if (L.length() == length)
      {
         Node compare1 = L.front;
         Node compare2 = this.front;
         
         for(int i=0; i<length; i++)
         {
            if(compare1.equals(compare2))
            {
               compare1 = compare1.next;
               compare2 = compare2.next;
            }
            else
            {
               return false;
            }
         }
      }
      else
      {
         return false;
      }
      return true;
   } 
   
   
   // Manipulation procedures
   void clear() // Resets this List to its original empty state.
   {
      front = null;
      back = null;
      cursor = null;
      length = 0;
      index = -1;
   }
   
   void moveFront() // If List is non-empty, places the cursor under the front element,
    // otherwise does nothing.
   {
      if (length>0)
      {
         cursor = front;
         index = 0;
      }
   }
   
   void moveBack() // If List is non-empty, places the cursor under the back element,
   // otherwise does nothing.
   {
      if (length>0)
      {
         cursor = back;
         index = length-1;
      }
   }
   
   void movePrev() // If cursor is defined and not at front, moves cursor one step toward
   // front of this List, if cursor is defined and at front, cursor becomes
   // undefined, if cursor is undefined does nothing.
   {
      if (cursor!=null && index!=0)
      {
         cursor = cursor.prev;
         index--;
      }
      
      else if (cursor!=null && index==0)
      {
         cursor = null;
         index = -1;
      }
   }
   
   void moveNext() // If cursor is defined and not at back, moves cursor one step toward
    // back of this List, if cursor is defined and at back, cursor becomes
   // undefined, if cursor is undefined does nothing.
   {
      if (cursor!=null && index!=length-1)
      {
         cursor = cursor.next;
         index++;
      }
      
      else if (cursor!=null && index==length-1)
      {
         cursor = null;
         index = -1;
      }
   }
   
   void prepend(int data) // Insert new element into this List. If List is non-empty,
   // insertion takes place before front element.
   {
      Node temp = new Node(data, null, null);
      if (length>0)
      {
         temp.next = front;
         front.prev = temp;
         front = temp;
         index = index+1;
         length++;
      }
      else
      {
         back = temp;
         front = temp;
         length++;
      }
   }
   
   void append(int data) // Insert new element into this List. If List is non-empty,
    // insertion takes place after back element.
   {
      Node temp = new Node(data, null, null);
      if (length>0)
      {
         temp.prev = back;
         back.next = temp;
         back = temp;
         length++;
      }
      else
      {
         front = temp;
         back = temp;
         length++;
      }
   }
   
   void insertBefore(int data) // Insert new element before cursor.
    // Pre: length()>0, index()>=0
   {
      int check = index;
      int check2 = length;
      if (check<0)
      {
         throw new RuntimeException("List Error: cursor isn't defined");
      }
      else if (check2<1)
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
      }
      
      Node temp = new Node(data, null, null);
      if (cursor.prev== null)
      {
         front = temp;
         cursor.prev = temp;
         temp.next = cursor;
         length++;
         index++;
      }
      else
      {  
         temp.next = cursor;
         temp.prev = cursor.prev;
         cursor.prev.next = temp;
         cursor.prev = temp;
         length++;
         index++;
      }
   }
   
   void insertAfter(int data) // Inserts new element after cursor.
    // Pre: length()>0, index()>=0
   {
      int check = length;
      int check2 = index;
      if (index<0)
      {
         throw new RuntimeException("List Error: cursor isn't defined");
      }
      else if (length<1)
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
      }
      
      Node temp = new Node(data, null, null);
      if (cursor.next == null)
      {
         back = temp;
         cursor.next = temp;
         temp.prev = cursor;
         length++;
      }
      else
      {
         temp.next = cursor.next;
         temp.prev = cursor;
         cursor.next.prev = temp;
         cursor.next = temp;
         length++;
      }
   }
   
   void deleteFront() // Deletes the front element. Pre: length()>0
   {
      int check = length;
      if (check<1)
      {
         throw new RuntimeException("List Error: cannot be called on an empty list");
      }
      if(cursor == front)
      {
         cursor = null;
         index = -1;
      }
      front = front.next;
      front.prev = null;
      length--;
      if (index>=0){
         index--;       
      }
      
   }
   
   void deleteBack() // Deletes the back element. Pre: length()>0
   {
      if(length < 1)
      {
         throw new RuntimeException("List Error: deleteBack() called on an empty List");
      }
      if(length == 1)
      {
         if(cursor == back) 
         {
            cursor = null;
            index = -1;
         }
         back = null;
         length--;
      }
      
      else
      {
         if(cursor == back)
         {
            cursor = null;
            index = -1;
         }
         back = back.prev;
         back.next = null;
         --length;
      }
   }
   
   void delete() // Deletes cursor element, making cursor undefined.
    // Pre: length()>0, index()>=0
   {
      int check = this.length;
      int check2 = this.index;
      if(check<1)
      {
         throw new RuntimeException("Lisst Error: cannot be called on an empty list");
      }
      else if (check2<0)
      {
         throw new RuntimeException("List Error: index isn't defined");
      }
      
      if (cursor==back)
      {
         deleteBack();
      }
      else if (cursor==front)
      {
         deleteFront();
      }
      else
      {
         cursor.prev.next = cursor.next;
         cursor.next.prev = cursor.prev;
         cursor = null;
         index = -1;
         length--;
      }
   }
   public String toString() // Overrides Object's toString method. Returns a String
   // representation of this List consisting of a space
   // separated sequence of integers, with front on left.
   {
      Node print = front;
      String toPrint = new String();
      for(int i=0; i<length; i++)
      {
         if (print == null){
            break;
         }
         toPrint = toPrint + print.data + " ";
         print = print.next;
      }
      return toPrint;
   }
   
   List copy() // Returns a new List representing the same integer sequence as this
    // List. The cursor in the new list is undefined, regardless of the
    // state of the cursor in this List. This List is unchanged.
   {
      List cop = new List();
      if(front == null){
         return cop;
      }
      Node copy = front;
      for(int i=0; i<length; i++)
      {
         if (copy == null){
            break;
         }
         cop.append(copy.data);
         copy = copy.next;
      }
      return cop;
   }

}