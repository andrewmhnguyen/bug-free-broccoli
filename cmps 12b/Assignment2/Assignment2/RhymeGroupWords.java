public class RhymeGroupWords {
	private String rhymeGroup; // The pronunciation for a rhyme group 
	private ListInterface wordList; // The list of words that are in this rhyme group. 

	// To create a new RhymeGroupWords, pass in the pronunciation string for the rhyme group and a list implementing ListInterface.
	public RhymeGroupWords(String rg, ListInterface wl) {
		rhymeGroup = rg;
		wordList = wl; 
	}

	// Public accessor for the rhyme group string. 
	public String getRhymeGroup() {
		return rhymeGroup; 
	}

	// Public accessor for the list of words. 
	public ListInterface getWordList() {
		return wordList; 
	}
}