

public class TestQueuesAndStacks {

	// Test Queues
	public static void testQueue() {
		System.out.println("Test queues");
		MyQueue test = new MyQueue();
		test.enqueue("a");
		test.enqueue("b");
		System.out.println(test);
		test.enqueue("c");
		test.enqueue("d");
		test.enqueue("e");
		test.enqueue("f");
		System.out.println(test);
		String s = (String)test.dequeue();
		System.out.println("dequeued " + s + ": " + test);
		test.enqueue("x");
		test.enqueue("y");
		test.enqueue("z");
		System.out.println(test);
		try {
			for (int i = 0; i < 10; i++) {
				s = (String)test.dequeue();
				System.out.println("dequeued " + s + ": " + test);
			}
		} 
		catch(QueueException ex) {
			System.out.println("EXCEPTION: " + ex);
		}
		test.enqueue("j");
		test.enqueue("k");
		test.enqueue("l");
		System.out.println("Final value: " + test);
	}

	// Test Stacks
	public static void testStack() {

		System.out.println("Test stacks");
		MyStack test = new MyStack();
		test.push("a");
		test.push("b");
		System.out.println(test);
		test.push("c");
		test.push("d");
		test.push("e");
		test.push("f");
		System.out.println(test);
		String s = (String)test.pop();
		System.out.println("popped " + s + ": " + test);
		test.push("x");
		test.push("y");
		test.push("z");
		System.out.println(test);
		try{
			for (int i = 0; i < 10; i++) {
				s = (String)test.pop();
				System.out.println("popped " + s + ": " + test);
			}
		}
		catch(StackException ex) {
			System.out.println("EXCEPTION: " + ex);
		}
		test.push("j");
		test.push("k");
		test.push("l");
		System.out.println("Final value: " + test);

		
	}

	public static void main(String[] args) {

		testQueue();
		testStack();
	}
}