public class MyStack implements StackInterface {
	/* 
	* TODO 1: Implement "MyStack"
	*/
   private MyLinkedList list;
   
   //constructs stack
   public MyStack() {
      list = new MyLinkedList();
   }

   //checks to see if the stack is empty
	public boolean isEmpty(){
      if (list.isEmpty() == true){
         return true;
      }
      return false;
   }

   //adds Object o the the top of the stack
	public void push(Object o){
      list.add(0, o);
   }

   //removes object at top of the stack and returns it 
	public Object pop(){
      if(list.size()==0){
         throw new StackException("pop used on empty stack");
      }
      Object popped = list.get(0);
      list.remove(0);
      return popped;
   }

   //returns object at the top of the stack
	public Object peek(){
      if(list.size()==0){
         throw new StackException("peek used on empty stack");
      }
      Object peeked = list.get(0);
      return peeked;
   }

   //removes all
	public void popAll(){
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
	* TODO 1: Implement "MyStack"
	*/
}