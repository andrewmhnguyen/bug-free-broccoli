public class Testing {
   public static void main (String[] args)
   {
      MyLinkedList a = new MyLinkedList();
      
      a.add(0,4);
      a.add(1,5);
      a.add(2,6);
      a.add(1,1);
      System.out.println("Size: " + a.size());
      System.out.println("Value at index 2 is : " + a.get(2));
      a.remove(0);
      System.out.println(a.get(0));
      System.out.println("5 is at index: " + a.find(5));
   }
}