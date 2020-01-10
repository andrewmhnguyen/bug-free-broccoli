
import java.io.*;
import java.util.*;
import java.util.Random;

/*
* A rule is an object with alternating plaintext and symbols. This class is used to store the expansion on the righthand
* side of a rule. The starting symbol is also represented using a Rule object. The main thing you do with a Rule object 
* is expand any symbols that appear in it looking up the rule indexed by the symbol. 
*/

public class Rule {
  private static Random random;

  // The raw expansion string. It can include a mixture of text and symbols (hashtagged text)
  private String raw; 

  // Array with text and symbols as separate entries
  private String[] sections; 

  public static void setSeed(long seed) {
    System.out.println("Set seed " + seed);
    random = new Random(seed); // Create a new random number generator with the specified seed
  }

  public String expand(Hashtable<String, Rule[]> grammar) {

    String[] results = new String[sections.length];
    for(int i=0; i < sections.length; i++)
      if (i%2 == 0) {// even index - sections[i] is plain text
        results[i] = sections[i];
      }
      else { // odd index - need to recursively expand
        Rule[] expansions = grammar.get(sections[i]);  
        Rule selectedExpansion = expansions[random.nextInt(expansions.length)];
        results[i] = selectedExpansion.expand(grammar);
      }

      return String.join("", results);

  }

  public String toString() {
    return raw;
  }

  Rule(String raw) {
    this.raw = raw;
    sections = raw.split("#");
  }
}
