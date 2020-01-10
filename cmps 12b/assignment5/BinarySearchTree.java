public class BinarySearchTree implements BSTInterface{
   
   BSTNode root;
   
   //constructor for BinarySearchTree
   BinarySearchTree(){
      root = null;
   }
   
   //class for BSTNode
   protected class BSTNode{
      String item;
      BSTNode left;
      BSTNode right;
      
      BSTNode(String o){
         item = o;
         left = null;
         right = null;
      }
   }

   public boolean isEmpty(){
      if(root == null){
         return true;
      }
      return false;
   }
   
   public void makeEmpty(){
      root = null;
   }
   
   public MyQueue inOrder(){
      MyQueue ordered = new MyQueue();
      inOrderRecursive(root, ordered);
      return ordered;
   }
   
   public MyQueue preOrder(){
      MyQueue ordered = new MyQueue();
      preOrderRecursive(root, ordered);
      return ordered;
   }
   public MyQueue postOrder(){
      MyQueue ordered = new MyQueue();
      postOrderRecursive(root, ordered);
      return ordered;
   }
   
   public boolean contains(String s){
      return recursiveSearch(root, s);
   }
   
   public void put(String s){
      root = recursiveInsert(root, s);
   }
   
   public void delete(String s){
      root = recursiveRemove(root, s);
   }
   
   public void balanceBST(){
      MyQueue newQueue = inOrder();
      MyQueue temp = new MyQueue();
      int counter = 0;
      while(newQueue.isEmpty()==false){
         temp.enqueue(newQueue.dequeue());
         counter ++;
      }
      String[] newArray = new String[counter];
      for(int i = 0; i < counter; i++){
         newArray[i]=(String)temp.dequeue();
      }
      makeEmpty();
      root = balanceRecursive(newArray, 0, counter);
   }
   
   
	// TODO: Fill this in and call it from contains()
	protected boolean recursiveSearch(BSTNode node, String s) {
		if(node == null){
         return false;
      }
      else{
         if(s.compareTo(node.item) == 0){
            return true;
         }
         else if(s.compareTo(node.item)<1){
            return recursiveSearch(node.left, s);
         }
         else{
            return recursiveSearch(node.right, s);
         }
      }
	}

	// TODO: Fill this in and call it from put()
	protected BSTNode recursiveInsert(BSTNode node, String s){
	   if (node == null){
         BSTNode insert = new BSTNode(s);
         return insert;
      }
      else{
         if(s.compareTo(node.item)<0){
            node.left = recursiveInsert(node.left, s);
         }
         else if(s.compareTo(node.item)>0){
            node.right = recursiveInsert(node.right, s);
         }
      }
      return node;
	}

	// TODO: Fill this in and call it from delete()
	protected BSTNode recursiveRemove(BSTNode node, String s) {
      if(node != null){
         if(s.compareTo(node.item)<0){
            node.left = recursiveRemove(node.left, s);
         }
         else if (s.compareTo(node.item)>0){
            node.right = recursiveRemove(node.right, s);
         }
         else{
            node = deleteNode(node);
         }
      }
      return node;
	}
	
	// TODO: Fill this in and call it from recursiveRemove()
	protected BSTNode deleteNode(BSTNode node) {
      if(node.left == null && node.right == null){
         node = null;
      }
      else if(node.left != null && node.right == null){
         node = node.left;
      }
      else if(node.left == null && node.right != null){
         node = node.right;
      }
      else{
         node.item = getSmallest(node.right);
         node.right = recursiveRemove(node.right, node.item);
      }
      return node;
	}

	// TODO: Fill this in and call it from deleteNode()
	protected String getSmallest(BSTNode node) {
      String smallest = node.item;
      while(node.left != null){
         smallest = node.left.item;
         node = node.left;
      }
      return smallest;
	}


	// TODO: Fill this in and call it from inOrder()
	protected void inOrderRecursive(BSTNode node, MyQueue queue) {
      if(node != null){
         inOrderRecursive(node.left, queue);
         queue.enqueue(node.item);
         inOrderRecursive(node.right, queue);
      }
	}


	// TODO: Fill this in and call it from preOrder()
	protected void preOrderRecursive(BSTNode node, MyQueue queue) {
      if(node != null){
         queue.enqueue(node.item);
         preOrderRecursive(node.left, queue);
         preOrderRecursive(node.right, queue);
      }
	}

	// TODO: Fill this in and call it from postOrder()
	protected void postOrderRecursive(BSTNode node, MyQueue queue) {
      if(node != null){
         postOrderRecursive(node.left, queue);
         postOrderRecursive(node.right, queue);
         queue.enqueue(node.item);
      }
	}

	// Prints out the tree structure, using indenting to show the different levels of the tree
	public void printTreeStructure() { 
		printTree(0, root);
	}

	// Recursive helper for printTreeStructure()
	protected void printTree(int depth, BSTNode node) {
		indent(depth);
		if (node != null) {
	    	System.out.println(node.item);
	    	printTree(depth + 1, node.left);
	    	printTree(depth + 1, node.right);
	 	} 
	 	else {
	  		System.out.println("null");
	  	}
	}

	// Indents with with spaces 
	protected void indent(int depth) {
		for(int i = 0; i < depth; i++)
			System.out.print("  "); // Indents two spaces for each unit of depth
	}


	// Extra Credit 

	// TODO: If doing the extra credit, fill this in and call it from balanceBST()
	protected BSTNode balanceRecursive(String[] array, int first, int last) {
      if (first == last){
         return null;
      }
      int middle = (first+last)/2;
      BSTNode newNode = new BSTNode(array[middle]);
      newNode.left = balanceRecursive(array, first, middle);
      newNode.right = balanceRecursive(array, middle+1, last);
      return newNode;
	} 
}