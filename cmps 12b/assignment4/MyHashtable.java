class MyHashtable implements DictionaryInterface {

   //defines class Entry and gives contructors
	protected class Entry{
      String key;
      Object value;
      
      Entry(){
         key = null;
         value = null;
      }
      
      Entry(String i){
         key = i;
         value = null;
      }
      
      Entry(Object i){
         key = null;
         value = i;
      }
      
      Entry(String a, Object b){
         key = a;
         value = b;
      }
   }
   
   protected int tableSize;
   protected int size;
   protected MyLinkedList[] table;
   
   //checks if hashtable is empty
   public boolean isEmpty(){
      if(size == 0){
         return false;
      }
      return true;
   }
   
   //returns size
   public int size(){
      return size;
   }
   
   //adds new value to the hashtable and returns null or old value if there was one 
   public Object put(String key, Object value){
      int hashCode = key.hashCode();
      int arrayIndex = Math.abs(hashCode)%tableSize;
      if(table[arrayIndex] == null){
         MyLinkedList bucket = new MyLinkedList();
         Entry newEntry = new Entry(key, value);
         bucket.add(0, newEntry);
         table[arrayIndex] = bucket;
         size ++;
         return null;
      }
      else{
         for(int i = 0; i < table[arrayIndex].size(); i ++){
            Entry oldEntry = (Entry) table[arrayIndex].get(i);
            if (key.equals(oldEntry.key)){
               Entry newEntry = new Entry(key, oldEntry.value);
               oldEntry.value = value;
               return newEntry;
            }
         }
         Entry newEntry = new Entry(key, value);
         table[arrayIndex].add(0, newEntry);
         size++;
         return null;
      }
   }
   
   //returns value stored in the key
   public Object get(String key){
      int hashCode = key.hashCode();
      int arrayIndex = Math.abs(hashCode) % tableSize;
      if (table[arrayIndex]==null){
         return null;
      }
      else {
         for(int i = 0; i < table[arrayIndex].size(); i ++){
            Entry oldEntry = (Entry) table[arrayIndex].get(i);
            if ((oldEntry.key).equals(key)){
               return oldEntry.value;
            }
         }
         return null;
      }
   }
   
   //removes kay/value pair associated with the key from the hashtable
   public void remove(String key){
      int hashCode = key.hashCode();
      int arrayIndex = Math.abs(hashCode) % tableSize;
      if(table[arrayIndex]!=null){
            for(int i = 0; i < table[arrayIndex].size(); i ++){
            Entry oldEntry = (Entry) table[arrayIndex].get(i);
            if (key.equals(oldEntry.key)){
               table[arrayIndex].remove(i);
               size--;
            }
         }
      }
   }
   
   //empties the hashtable
   public void clear(){
      table = new MyLinkedList[tableSize];
      size = 0;
   }
   
   //returns an array of all the keys stored in the table
   public String[] getKeys(){
      String[] keys = new String[size];
      int index = 0;
      for(int i = 0; i < tableSize; i++){
         if(table[i]!=null){
            for(int j = 0; j < table[i].size(); j++){
               Entry newEntry = (Entry) table[i].get(j);
               keys[index] = newEntry.key;
               index++;
            }
         }
      }
      return keys;
   }
   
   //constructor for hashtable
   public MyHashtable(int tableSize){
      this.tableSize = tableSize;
      size = 0;
      table = new MyLinkedList[tableSize];
   }
   
   // Returns the size of the biggest bucket (most collisions) in the hashtable. 
	public int biggestBucket() {
		int biggestBucket = 0; 
		for(int i = 0; i < table.length; i++) {
			// Loop through the table looking for non-null locations. 
			if (table[i] != null) {
				// If you find a non-null location, compare the bucket size against the largest
				// bucket size found so far. If the current bucket size is bigger, set biggestBucket
				// to this new size. 
				MyLinkedList bucket = table[i];
				if (biggestBucket < bucket.size())
					biggestBucket = bucket.size();
			}
		}
		return biggestBucket; // Return the size of the biggest bucket found. 
	}

	// Returns the average bucket length. Gives a sense of how many collisions are happening overall.
	public float averageBucket() {
		float bucketCount = 0; // Number of buckets (non-null table locations)
		float bucketSizeSum = 0; // Sum of the size of all buckets
		for(int i = 0; i < table.length; i++) {
			// Loop through the table 
			if (table[i] != null) {
				// For a non-null location, increment the bucketCount and add to the bucketSizeSum
				MyLinkedList bucket = table[i];
				bucketSizeSum += bucket.size();
				bucketCount++;
			}
		}

		// Divide bucketSizeSum by the number of buckets to get an average bucket length. 
		return bucketSizeSum/bucketCount; 
	}

	public String toString() {
		String s = "";
		for(int tableIndex = 0; tableIndex < tableSize; tableIndex++) {
			if (table[tableIndex] != null) {
				MyLinkedList bucket = table[tableIndex];
				for(int listIndex = 0; listIndex < bucket.size(); listIndex++) {
					Entry e = (Entry)bucket.get(listIndex);
					s = s + "key: " + e.key + ", value: " + e.value + "\n";
				}
			}
		}
		return s; 
	}
}