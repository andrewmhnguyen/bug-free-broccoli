import java.io.*;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Paths;


public class TraceryRecursion {



	public static void saveFile(String fileName, String text) {
		try {
			Files.write(Paths.get(fileName), text.getBytes());
		} catch (IOException ex){
			ex.printStackTrace();
		}
	}

	public static void outputGrammar(Hashtable<String, Rule[]> grammar) {
		System.out.println("\nGRAMMAR:");
		for ( String key : grammar.keySet() ) {
			String line = "";
			line += key + ": " + String.format("%1$" + (20 - key.length()) + "s", " ");
			for (Rule rule : grammar.get(key)) {
				line += "\"" + rule + "\"," ;
			}

			System.out.println(line);
		}
	}

	// Given a path, load the grammar at that path
	public static Hashtable<String, Rule[]> loadGrammar(String path) {
		Hashtable<String, Rule[]> grammar = new Hashtable<String, Rule[]>();
		try {
			// Creating an array of strings, one for each line in the file
			String[] lines = new String(Files.readAllBytes(Paths.get(path))).split("\\r?\\n");
			
			// Print out the lines to verify that the file has been read
			for(String line : lines) 
				System.out.println(line);

			/*
			* START: TO DO #2
			*/
	      for(int i = 0; i < lines.length; i++){
            String[] lines2 = lines[i].split(":");
            String key = lines2[0];
            String[] lines3 = lines2[1].split(",");
            Rule[] rules = new Rule[lines3.length];
            for (int j = 0; j < rules.length; j++){
               rules[j] = new Rule(lines3[j]);
            }
            grammar.put(key, rules);
         }
			/*
			* END: TO DO #2
			*/

		}
		catch (IOException ex){
			ex.printStackTrace();
		}

		return grammar;
	}



	public static void main(String []args) throws IOException  {
		System.out.println("Running TraceryRecursion...");

		String grammarFile = "grammar-story.txt"; // The default grammar file to load if none is specified in the args

		// The default symbol to begin expanding if none is specified in the args. This argument has to be in quotes. 
		// So if you were specifying a grammar and a startSymbol named #start# the command to run your program would 
		// look like: java TraceryRecursion my-grammar.txt "#start#"
		String startSymbol = "#origin#"; 

		int count = 1; // The default number of times to expand the starting symbol if this is not specified in the args 
		long seed = System.currentTimeMillis() % 1000; // The default random seed if not specified in the args

		/*
		* START: TO DO #1
		*/
      if (args.length == 1){
         grammarFile = args[0];
      }
      else if (args.length == 2){
         grammarFile = args[0];
         startSymbol = args[1];
      }
      else if (args.length == 3){
         grammarFile = args[0];
         startSymbol = args[1];
         count = Integer.parseInt(args[2]);
      }
      else if (args.length == 4){
         grammarFile = args[0];
         startSymbol = args[1];
         count = Integer.parseInt(args[2]);
         seed = Long.parseLong(args[3]);
      }
		/*
		* END: TO DO #1
		*/

		System.out.printf("\twith grammar:'%s'\tstartsymbol:'%s' \tcount:%d\t seed:%d\n", grammarFile, startSymbol, count, seed);
		Rule.setSeed(seed); // Set the seed using a static method defined on Rule
		Hashtable<String, Rule[]>grammar = loadGrammar(grammarFile); // Load the grammar from the grammar file
		outputGrammar(grammar); // Print out the loaded grammar 

		Rule rule = new Rule(startSymbol); // Create a new Rule object using the startSymbol
		for (int i = 0; i < count; i++) { 
			// Expand the start symbol until there are no more symbols to expand. Do this 'count' number of times. 
			System.out.println(rule.expand(grammar));
		}
	}
}
