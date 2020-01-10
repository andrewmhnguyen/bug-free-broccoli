import java.io.*;
import java.util.*;
import java.util.Arrays;
import java.nio.file.Files;
import java.nio.file.Paths;



public class WordDictionary {
	HashSet<String> table;

	public boolean isWord(String word) {
		return table.contains(word);
	}

	public WordDictionary() {
		table = new HashSet<String>();
		String path = "allworks-frequency.txt";
		try {
			String[] lines = new String(Files.readAllBytes(Paths.get(path))).split("\\r?\\n");
			for (String line: lines) {
				int index = line.indexOf(":");
				String word = line.substring(0, index);
				table.add(word);

			}
			
		} catch(Exception ex) {
			System.out.println(ex);
		}	
	}
}