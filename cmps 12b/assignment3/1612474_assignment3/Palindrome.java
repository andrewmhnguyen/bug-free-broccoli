import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException; 
import java.util.Arrays;
import java.util.ArrayList;

public class Palindrome {

	static WordDictionary dictionary = new WordDictionary(); 

	
	// Get all words that can be formed starting at this index
	public static String[] getWords(String text, int index) {
		ArrayList<String> words = new ArrayList<String>();
		for (int i = 0; i <= text.length() - index; i++) {
			String maybeWord = text.substring(index, index + i);
			if (dictionary.isWord(text.substring(index, index + i))) {
				words.add(maybeWord);
			}
		}

		return words.toArray(new String[0]);
	}

   //returns a reversed string
	public static String stackToReverseString(MyStack stack) {
		/* 
		* TODO 3
		*/
      String newString = "";
      MyStack tempStack = new MyStack();
      
      //moves things from original stack to new stack
      while(true){
         tempStack.push(stack.pop());
         if(stack.isEmpty()==true){
            break;
         }
      }
      
      //mvoes items from new stacks back to original stack and adds it to string
      while(true){
         stack.push(tempStack.pop());
         if(tempStack.isEmpty()==true){
            newString = newString + stack.peek();
            break;
         }
         else{
            newString = newString + stack.peek() + " ";
         }
      }
      
		return newString;
		/* 
		* TODO 3
		*/
	}

   //reverses the string an removes non alphabetical letters
	public static String reverseStringAndRemoveNonAlpha(String text) {
		/* 
		* TODO 4
		*/
      String newString = "";
      MyStack tempStack = new MyStack();
      
      //iterates through the string and pushes character from the string to the stack if they are alphabetic
      for(int i = 0; i < text.length(); i++){
         if(Character.isAlphabetic(text.charAt(i))==true){
            tempStack.push((Character)text.charAt(i));
         }
      }
      
      //moves things from stack to reconstruct the string in reverse
      while(true){
         newString = newString + tempStack.pop();
         if(tempStack.isEmpty()==true){
            break;
         }
      }
      
		return newString;
		/* 
		* TODO 4
		*/
	}



	// Returns true if the text is a palindrome, false if not.
	public static boolean isPalindrome(String text) {
		/* 
		* TODO 5: Implement "explorePalindrome"
		*/
      
      String newText = text.toLowerCase();
      MyStack tempStack = new MyStack();
      MyQueue tempQueue = new MyQueue();
      
      //adds characters to each stack and queue
      for(int i = 0; i<text.length();i++){
         if(Character.isAlphabetic(newText.charAt(i))==true){
            tempStack.push((Character)newText.charAt(i));
            tempQueue.enqueue((Character)newText.charAt(i));
         }
      }
      
      //pops and dequeues each character and checks if they are the same - if not, then return false
      boolean palindrome;
      while (true){
         if(tempStack.pop().equals(tempQueue.dequeue())){
            palindrome = true;
         }
         else{
            palindrome = false;
            break;
         }
         if(tempStack.isEmpty()==true){
            break;
         }
      }
      
		return palindrome;
		/* 
		* TODO 5: Implement "explorePalindrome"
		*/
	}

   //sees if the text has other palindromes
	public static void explorePalindrome(String text) {

	/* 
	* TODO 6: Implement "explorePalindrome" & helper function
	*/
		String newText = text.toLowerCase();
      String reverseText = reverseStringAndRemoveNonAlpha(newText);
      MyStack decomposition = new MyStack();
      int index = 0;
      
      decomposeText(text, reverseText, index, decomposition);
   }
   
   //iterates through the string and possible words and prints out if a palindrome is found 
   public static void decomposeText(String originalText, String textToDecompose, int index, MyStack decomposition){
      //if reaches end of string, means that a palindrome has been found and prints it out
      if(index == textToDecompose.length()){
         String printable = stackToReverseString(decomposition);
         System.out.println(originalText+ ": " + printable);
      }
      else{
         //finds possible words and pushes it to the stack
         String[] foundWords = getWords(textToDecompose, index);
         for(int i = 0; i < foundWords.length; i++){
            decomposition.push(foundWords[i]);
            int newIndex = index + foundWords[i].length();
            //recurses at the next index
            decomposeText(originalText, textToDecompose, newIndex, decomposition);
            
            //pops the word and moves to the next one 
            decomposition.pop();
         }
      }
   
	/* 
	* TODO 6
	*/

	}


	// This function looks at the arguments that are passed 
	// and decides whether to test palindromes or expand them
	public static void main(String[] args) throws IOException {

		if (args.length == 0) {
			System.out.println("ERROR: Remember to set the mode with an argument: 'test' or 'expand'");
		} else {
			String mode = args[0];

			// Default palindromes to use if none are provided
			String[] testPalindromes = {"A", "ABBA", "oh no an oboe", "salami?", "I'm alas, a salami"};
			if (args.length > 1)
				testPalindromes = Arrays.copyOfRange(args, 1, args.length);

			// Test whether the provided strings are palindromes
			if (mode.equals("test")) {

				for (int i = 0; i < testPalindromes.length; i++) {
					String text = testPalindromes[i];
					boolean result = isPalindrome(text);
					System.out.println("'" + text + "': " + result);
				}

			} else if (mode.equals("expand")) {
				for (int i = 0; i < testPalindromes.length; i++) {
					explorePalindrome(testPalindromes[i]);
				}	
			}
			else {
				System.out.println("unknown mode: " + mode);
			}
		}
	}
}