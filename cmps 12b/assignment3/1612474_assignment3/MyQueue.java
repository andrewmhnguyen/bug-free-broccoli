public class MyQueue implements QueueInterface {
	/* 
	* TODO 2: Implement "MyQueue"
	*/
   private MyLinkedList list;
   
   //queue constructor
   public MyQueue() {
      list = new MyLinkedList();
   }
   
   //checks to see if queue is empty
   public boolean isEmpty(){
      if (list.isEmpty() == true){
         return true;
      }
      return false;
   }

   //adds Object item to the end of the queue
	public void enqueue(Object item){
      list.add(list.size(), item);
   }

   //removes object at front of queue and returns it
	public Object dequeue(){
      if(list.size()==0){
         throw new QueueException("called on empty queue");
      }
      Object dequeued = list.get(0);
      list.remove(0);
      return dequeued;
   }
   
   //returns object at front of the queue
   public Object peek(){
      if(list.size()==0){
         throw new QueueException("called on empty queue");
      }
      Object peeked = list.get(0);
      return peeked;
   }

   //removes all object in the queue
	public void dequeueAll(){
      list.removeAll();
   }
   
   //toString method for printing
   public String toString(){
      String finished = "";
      for(int i = 0; i<list.size(); i++){
         if(i==list.size-1){
            finished = finished+list.get(i);
         }
         else{
            finished = finished+list.get(i)+ ", ";
         }
      }
      return finished;
   }
	
	/* 
	* TODO 2: Implement "MyQueue"
	*/

} 