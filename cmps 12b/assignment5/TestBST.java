public class TestBST{

	public static void main(String[] args) {
		BinarySearchTree tree = new BinarySearchTree(); 

		//Testing for inserting words into the tree
		//Prints inorder traversal of tree 
		tree.put("dog");
		tree.put("cat");
		tree.put("alligator");
      tree.put("giraffe");
      tree.put("elephant");
		tree.put("hippo");
		tree.put("zebra");
		tree.printTreeStructure();

		System.out.println("Contains dog: " + tree.contains("dog"));
		System.out.println("Contains alligator: " + tree.contains("alligator"));
		System.out.println("Contains horse: " + tree.contains("horse"));

		System.out.println();
		tree.delete("dog");
		tree.printTreeStructure();

		System.out.println();
		tree.delete("elephant");
		tree.printTreeStructure();

		System.out.println();
		tree.delete("cat");
		tree.printTreeStructure();

		tree.put("penguin");
		tree.put("aardvark"); 
		tree.put("bear");
		tree.printTreeStructure();

		MyQueue inOrder = tree.inOrder();
		MyQueue preOrder = tree.preOrder();
		MyQueue postOrder = tree.postOrder();

		System.out.println("In order: " + inOrder);
		System.out.println("Preorder: " + preOrder);
		System.out.println("Postorder: " + postOrder);
      
		//Testing if clearing the tree works
		System.out.println();
		tree.makeEmpty(); 
		System.out.println(tree.isEmpty()); 

		// Testing the balancing
		// Make a very unbalanced tree
		while (!inOrder.isEmpty()) {
			String s = (String)inOrder.dequeue(); 
			tree.put(s);
			System.out.println(s);
		}
		tree.printTreeStructure(); 

		tree.balanceBST();
		tree.printTreeStructure();
		
	}
}