public interface ListInterface {

	// Returns true if the list is empty, false otherwise. 
	public boolean isEmpty();

	// Returns the size of the list (number of items in the list)
	public int size();

	// Adds an Object to the list at the specified index. 
	public void add(int index, Object value)
		throws ListIndexOutOfBoundsException;

	// Removes an item from the list at the specified index. 
	public void remove(int index)
		throws ListIndexOutOfBoundsException;

	// Removes all the items from the list. 
	public void removeAll();

    // Returns the Object stored in the list at the specified index. 
	public Object get(int index)
		throws ListIndexOutOfBoundsException;

	// Returns the index at which an Object is stored in the list, -1 if it's not in the list.
	public int find(Object o);
     
}