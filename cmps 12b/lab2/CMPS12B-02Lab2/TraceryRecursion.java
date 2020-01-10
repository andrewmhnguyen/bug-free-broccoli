/* 
* START: TO DO: Import the packages you need to support your I/O operations.
*/
import java.util.Hashtable;
import java.io.*;

/*
* END: TO DO: Import the packages you need to support your I/O operations.
*/

public class TraceryRecursion {

	/*
	* START: TO DO: outputGrammar(Hashtable<String, Rule> grammar, PrintStream ps)
	* Change the code so everything that is currently output to the console using System.out.println is now output to the PrintStream
	* using the PrinStream.println() method.  
	*/
	public static void outputGrammar(Hashtable<String, Rule[]> grammar, PrintStream ps) {
		ps.println("\nGRAMMAR:");
		for ( String key : grammar.keySet() ) {
			String line = "";
			line += key + ": " + String.format("%1$" + (20 - key.length()) + "s", " ");
			for (Rule rule : grammar.get(key)) {
				line += "\"" + rule + "\"," ;
			}

			ps.println(line);
		}
	}
	/*
	* END: TO DO: changing outputGrammar to use a PrintStream
	*/


	// Given an InputStream, load the grammar at that InputStream
	public static Hashtable<String, Rule[]> loadGrammar(InputStream inStream) throws IOException{

		Hashtable<String, Rule[]> grammar = new Hashtable<String, Rule[]>();

		// TO DO: create a new BufferedReader based on inStream that you'll use to read the stream line by line (using readLine())

		/* 
		* START: TO DO: Make a loop that reads a new line from the BufferedReader line by line and adds it to the grammar
		*/
      InputStreamReader input1 = new InputStreamReader(inStream);
      BufferedReader buffer1 = new BufferedReader(input1);
      boolean a = false;
      while (a == false){
         String line = buffer1.readLine();
         
         if(line==null){
            break;
         }
         
			/* 
			* Put your code that takes each line and adds it to the grammar inside the loop. Below is the code from our solution for doing this,
			* but feel free to substitute this with the code from your own assignment. 
			*/ 
			String[] ruleString = line.split(":");
			String[] expansions = ruleString[1].split(",");
			Rule[] rules = new Rule[expansions.length];
			for(int i=0; i < expansions.length; i++) {
				rules[i] = new Rule(expansions[i]);
			}
			grammar.put(ruleString[0], rules); 

		/*
		* END: TO DO: Make a loop that reads a new line from the BufferedReader line by line and processes it.
		*/ 
      }
		return grammar;
	}


	/*
	* START: TO DO: public static InputStream getInputStream(String[] args)
	*/
   public static InputStream getInputStream(String[] args){
      int founder = 0;
      if(args.length>0){
         boolean found = false;
         int i = 0;
         for(; i < args.length; i++){
            if(args[i].equals("-in")){
               found = true;
               founder = i;
            }
         }
         
         if(found == true){
            FileInputStream newFile;
            try{
               newFile = new FileInputStream(args[founder+1]);
               return newFile;
            }
            catch( FileNotFoundException a){
               System.out.println("Input grammar file does not exist.");
            }
            return System.in;
         }
         else{
            return System.in;
         }
      }
      else{
         return System.in;
      }
   }
	/* 
	* END: TO DO: public static InputStream getInputStream(String[] args)
	*/


	/*
	* START: TO DO: public static PrintStream getOutputStream(String[] args)
	*/
   public static PrintStream getOutputStream(String[] args){
      int founder = 0;
      if(args.length>0){
         boolean found = false;
         int b = 0;
         for(; b < args.length; b++){
            if(args[b].equals("-out")){
               found = true;
               founder = b;
            }
         }
         if (found == true){
            PrintStream newFile;
            try{
               newFile = new PrintStream(args[founder+1]);
               return newFile;
            }
            catch( FileNotFoundException a){
               System.out.println("Output file can not be created.");
               return System.out;
            }
         }
         else{
            return System.out;
         }
      }
      else{
         return System.out;
      }
   }
   
	/* 
	* END: TO DO: public static PrintStream getOutputStream(String[] args)
	*/


	public static void main(String[] args) throws IOException{
		System.out.println("Running TraceryRecursion...");

		String startSymbol = "#origin#"; 

		int count = 10; 
		long seed = 1; 

		/*
		* START: TO DO: call getInputStream(args) and getOutputStream(args) to get the InputStream and PrintStream to use
		*/
      InputStream a = getInputStream(args);
      PrintStream b = getOutputStream(args);
      
      
		/*
		* END: TO DO: call getInputStream(args) and getOutputStream(args) to get the InputStream and PrintStream to use
		*/

		Rule.setSeed(seed); // Set the seed using a static method defined on Rule

		// To DO: comment this line back in to load the grammar into the Hashtable once you've set the inputStream you're using
		Hashtable<String, Rule[]> grammar = loadGrammar(a); 

		// TO DO: comment this line back in to print the loaded grammar. You'll need to set outStream correctly
		outputGrammar(grammar, b); 

		Rule rule = new Rule(startSymbol); // Create a new Rule object using the startSymbol
		// Expand the start symbol until there are no more symbols to expand. Do this 'count' number of times.
		for (int i = 0; i < count; i++) { 
			// TO DO: Change the line below so it prints to the correct PrintStream instead of always System.out
			b.println(rule.expand(grammar));
		}
      
	}
}

