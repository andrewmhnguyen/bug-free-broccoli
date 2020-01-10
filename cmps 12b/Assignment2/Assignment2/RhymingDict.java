import java.io.*;
import java.util.*;
import java.util.Arrays;
import java.nio.file.Files;
import java.nio.file.Paths;

public class RhymingDict { 	
  

	// Given a pronunciation, get the rhyme group
	// get the more *heavily emphasized vowel* and follwing syllables
	// For "tomato", this is "-ato", and not "-omato", or "-o"
	// Tomato shares a rhyming group with "potato", but not "grow"
	private static String getRhymeGroup(String line) {

		int firstSpace = line.indexOf(" "); 

		String pronunciation = line.substring(firstSpace + 1, line.length());

		int stress0 = pronunciation.indexOf("0");
		int stress1 = pronunciation.indexOf("1");
		int stress2 = pronunciation.indexOf("2");

		if (stress2 >= 0)
			return pronunciation.substring(stress2 - 2, pronunciation.length());
		if (stress1 >= 0)
			return pronunciation.substring(stress1 - 2, pronunciation.length());
		if (stress0 >= 0)
			return pronunciation.substring(stress0 - 2, pronunciation.length());
		
		// No vowels at all? ("hmmm", "mmm", "shh")
		return pronunciation;
	}

	private static String getWord(String line) {
		int firstSpace = line.indexOf(" ");

		String word = line.substring(0, firstSpace);

		return word; 
	}

	// Load the dictionary
	private static String[] loadDictionary() {
		// Load the file and read it

		String[] lines = null; // Array we'll return holding all the lines of the dictionary
		
		try {
			String path = "cmudict/cmudict-short.dict";
			// Creating an array of strings, one for each line in the file
			lines = new String(Files.readAllBytes(Paths.get(path))).split("\\r?\\n");
			
		}
		catch (IOException ex){
			ex.printStackTrace();
		}

		return lines; 
	}

	
	public static void main(String []args) {

		String[] dictionaryLines = loadDictionary();

		/*//This code is in here to help you test MyLinkedList without having to mess around with the dictionary. 
		  // Feel free to change this test code as you're testing your linked list. But be sure to comment this code
		   //out when you submit it. 
         		
		MyLinkedList testList = new MyLinkedList(); 
		testList.add(0, "hello");
		testList.add(1, "world");
		testList.add(2, "!");
		System.out.println(testList);
		System.out.println("index 2 = " + testList.get(0));
		System.out.println("world at index " + testList.find("world"));
		System.out.println("hello at index " + testList.find("hello"));
		System.out.println("! at index " + testList.find("!"));
		System.out.println("wow at index " + testList.find("wow"));
		testList.remove(2);
		System.out.println(testList);
		testList.remove(0);
		System.out.println(testList);
		testList.remove(0);
		System.out.println(testList);
		System.out.println("hello at index " + testList.find("hello"));
      */		
      
		// List of rhyme groups. The items in this linked list will be RhymeGroupWords. 
		ListInterface rhymeGroups = new MyLinkedList(); 

		/* TODO: Add in your code to load the dictionary into your linked lists. Remember that rhymeGroups is a 
		   list of RhymeGroupWords. Inside each of this objects is another linked list which is a list of words within the same
		   rhyme group. I would recommend first getting this working with MyLinkedList for both lists (rhyme groups and 
		   word lists) then get it working using MySortedLinkedList for the word groups. */
      
      //Get the 8 rhyme groups
      String[] dictionary = loadDictionary();
      int i = 0;
      int j = 0;
      String rhyme1 = "";
      String rhyme2 = "";
      String rhyme3 = "";
      String rhyme4 = "";
      String rhyme5 = "";
      String rhyme6 = "";
      String rhyme7 = "";
      String rhyme8 = "";
      while(i < 8){
         if (i < 1){
            rhyme1 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 2 && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false)){
            rhyme2 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 3 &&
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false)){
            rhyme3 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 4 &&
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme3))==false)){
            rhyme4 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 5 &&
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme3))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme4))==false)){
            rhyme5 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 6&&
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme3))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme4))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme5))==false)){
            rhyme6 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 7 &&
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme3))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme4))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme5))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme6))==false)){
            rhyme7 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         if (i < 8 && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme1))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme2))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme3))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme4))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme5))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme6))==false) && 
         ((getRhymeGroup(dictionary[j]).equals(rhyme7))==false)){
            rhyme8 = getRhymeGroup(dictionary[j]);
            i++;
            j++;
         }
         j++;  
      }
      
      //Sort words and adds them into the 8 rhyme groups
      MyLinkedList list1 = new MyLinkedList();
      MyLinkedList list2 = new MyLinkedList();
      MyLinkedList list3 = new MyLinkedList();
      MyLinkedList list4 = new MyLinkedList();
      MyLinkedList list5 = new MyLinkedList();
      MyLinkedList list6 = new MyLinkedList();
      MyLinkedList list7 = new MyLinkedList();
      MyLinkedList list8 = new MyLinkedList();
      
      for( int a = 0; a < dictionary.length; a ++){
         if(getRhymeGroup(dictionary[a]).equals(rhyme1)){
            list1.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme2)){
            list2.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme3)){
            list3.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme4)){
            list4.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme5)){
            list5.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme6)){
            list6.add(0, getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme7)){
            list7.add(0, getWord(dictionary[a]));
         }
         else{
            list8.add(0, getWord(dictionary[a]));
         }
      }
      
      
      RhymeGroupWords group1 = new RhymeGroupWords (rhyme1, list1);  
      RhymeGroupWords group2 = new RhymeGroupWords (rhyme2, list2); 
      RhymeGroupWords group3 = new RhymeGroupWords (rhyme3, list3); 
      RhymeGroupWords group4 = new RhymeGroupWords (rhyme4, list4); 
      RhymeGroupWords group5 = new RhymeGroupWords (rhyme5, list5); 
      RhymeGroupWords group6 = new RhymeGroupWords (rhyme6, list6); 
      RhymeGroupWords group7 = new RhymeGroupWords (rhyme7, list7); 
      RhymeGroupWords group8 = new RhymeGroupWords (rhyme8, list8);  
      
      rhymeGroups.add(0, group1);
      rhymeGroups.add(1, group2);
      rhymeGroups.add(2, group3);
      rhymeGroups.add(3, group4);
      rhymeGroups.add(4, group5);
      rhymeGroups.add(5, group6);
      rhymeGroups.add(6, group7);
      rhymeGroups.add(7, group8);
      
      //Adding rhyme groups to the rhymeGroups list - sorted
      MySortedLinkedList sortedList1 = new MySortedLinkedList();
      MySortedLinkedList sortedList2 = new MySortedLinkedList();
      MySortedLinkedList sortedList3 = new MySortedLinkedList();
      MySortedLinkedList sortedList4 = new MySortedLinkedList();
      MySortedLinkedList sortedList5 = new MySortedLinkedList();
      MySortedLinkedList sortedList6 = new MySortedLinkedList();
      MySortedLinkedList sortedList7 = new MySortedLinkedList();
      MySortedLinkedList sortedList8 = new MySortedLinkedList();
      
      for( int a = 0; a < dictionary.length; a ++){
         if(getRhymeGroup(dictionary[a]).equals(rhyme1)){
            sortedList1.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme2)){
            sortedList2.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme3)){
            sortedList3.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme4)){
            sortedList4.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme5)){
            sortedList5.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme6)){
            sortedList6.add(getWord(dictionary[a]));
         }
         else if(getRhymeGroup(dictionary[a]).equals(rhyme7)){
            sortedList7.add(getWord(dictionary[a]));
         }
         else{
            sortedList8.add(getWord(dictionary[a]));
         }
      }
      
      rhymeGroups.removeAll();
      
      RhymeGroupWords sortedGroup1 = new RhymeGroupWords (rhyme1, sortedList1);  
      RhymeGroupWords sortedGroup2 = new RhymeGroupWords (rhyme2, sortedList2); 
      RhymeGroupWords sortedGroup3 = new RhymeGroupWords (rhyme3, sortedList3); 
      RhymeGroupWords sortedGroup4 = new RhymeGroupWords (rhyme4, sortedList4); 
      RhymeGroupWords sortedGroup5 = new RhymeGroupWords (rhyme5, sortedList5); 
      RhymeGroupWords sortedGroup6 = new RhymeGroupWords (rhyme6, sortedList6); 
      RhymeGroupWords sortedGroup7 = new RhymeGroupWords (rhyme7, sortedList7); 
      RhymeGroupWords sortedGroup8 = new RhymeGroupWords (rhyme8, sortedList8);  
      
      rhymeGroups.add(0, sortedGroup1);
      rhymeGroups.add(1, sortedGroup2);
      rhymeGroups.add(2, sortedGroup3);
      rhymeGroups.add(3, sortedGroup4);
      rhymeGroups.add(4, sortedGroup5);
      rhymeGroups.add(5, sortedGroup6);
      rhymeGroups.add(6, sortedGroup7);
      rhymeGroups.add(7, sortedGroup8);
      
		/* End TODO for adding dictionary in rhymeGroups. */

		// This code prints out the rhyme groups that have been loaded above. 
		for(int c =0; c < rhymeGroups.size(); c++) {
			RhymeGroupWords rg = (RhymeGroupWords) rhymeGroups.get(c);
			System.out.print(rg.getRhymeGroup() + ": ");
			System.out.println(rg.getWordList());
		} 

		/* TODO: Add the code here to iterate through pairs of arguments, esting to see if they are in the same rhyme group or not.
		*/
      
      //go through each word list to see if it is in there 
      int d = 0;
      int maxer = args.length-1;
      if(args.length%2 != 0){
         maxer = maxer - 1;
      }
      while ( d < maxer){
      
         //checks which list where the first word is located
         int groupFound = -1;
         int groupFound2 = -1;
         boolean found = false;
         int findnumb1 = list1.find(args[d]);
         int findnumb2 = list2.find(args[d]);
         int findnumb3 = list3.find(args[d]);
         int findnumb4 = list4.find(args[d]);
         int findnumb5 = list5.find(args[d]);
         int findnumb6 = list6.find(args[d]);
         int findnumb7 = list7.find(args[d]);
         int findnumb8 = list8.find(args[d]);
      
         if (findnumb1 != -1){
            groupFound = 1;
         }
         else if (findnumb2 != -1){
            groupFound = 2;
         }
         else if (findnumb3 != -1){
            groupFound = 3;
         }   
         else if (findnumb4 != -1){
            groupFound = 4;
         }
         else if (findnumb5 != -1){
            groupFound = 5;
         }
         else if (findnumb6 != -1){
            groupFound = 6;
         }
         else if (findnumb7 != -1){
            groupFound = 7;
         }
         else if (findnumb8 != -1){
            groupFound = 8;
         }
         
         //checks which list where the second word is located
         int findnumbsec1 = list1.find(args[d+1]);
         int findnumbsec2 = list2.find(args[d+1]);
         int findnumbsec3 = list3.find(args[d+1]);
         int findnumbsec4 = list4.find(args[d+1]);
         int findnumbsec5 = list5.find(args[d+1]);
         int findnumbsec6 = list6.find(args[d+1]);
         int findnumbsec7 = list7.find(args[d+1]);
         int findnumbsec8 = list8.find(args[d+1]);
      
         if (findnumbsec1 != -1){
            groupFound2 = 1;
         }
         else if (findnumbsec2 != -1){
            groupFound2 = 2;
         }
         else if (findnumbsec3 != -1){
            groupFound2 = 3;
         }   
         else if (findnumbsec4 != -1){
            groupFound2 = 4;
         }
         else if (findnumbsec5 != -1){
            groupFound2 = 5;
         }
         else if (findnumbsec6 != -1){
            groupFound2 = 6;
         }
         else if (findnumbsec7 != -1){
            groupFound2 = 7;
         }
         else if (findnumbsec8 != -1){
            groupFound2 = 8;
         }
         
         //compares the two lists on where the word is found 
         if(groupFound == -1 && groupFound2 != -1){
            System.out.println(args[d] + " is not in the dictionary");
         }
         else if (groupFound2 == -1 && groupFound != -1){ 
            System.out.println(args[d+1] + " is not in the dictionary");
         }
         else if (groupFound2 == -1 && groupFound == -1){
            System.out.println(args[d] + " and " + args[d+1] + " are both not in the dictionary");
         }
         else if(groupFound==groupFound2 && groupFound!= -1){
            System.out.println(args[d] + " and " + args[d+1] + " rhyme");
         }
         else{
            System.out.println(args[d] + " and " + args[d+1] + " don't rhyme");
         }
         
         d = d+2;
      }
      
      
	}
}
