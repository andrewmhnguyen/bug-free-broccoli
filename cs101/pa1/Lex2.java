import java.io.*;
import java.util.Scanner;

public class Lex
{
   public static void main(String[] args) throws IOException
   {
      Scanner input = null;
      PrintWriter output = null;
      String line = null;
      String[] token = null;
      int lineNumber = -1;
      
      if (args.length != 2)
      {
         System.err.println("Usage: Lex infile outfile");
         System.exit(1);
      }
      input = new Scanner(new File(args[0]));
            
      int count = 0;
      while( input.hasNextLine() )
      {
         count++;
         input.nextLine();
      }
      
      input.close();
      input = null;
      
      List newList = new List();
      token = new String[count];
      input = new Scanner(new File(args[0]));
      output = new PrintWriter(new FileWriter(args[1]));

      while( input.hasNextLine() )
      {
         token[++lineNumber] = input.nextLine();
      }
      
      newList.append(0);
      
      for (int i = 1; i < token.length; i++)
      {
         String temp = token[i];
         int j = i -1;
         
         newList.moveBack();
         while (j>=0&&temp.compareTo(token[newList.get()])<=0)
         {
            --j;
            newList.movePrev();
         }
         
         if (newList.index() >= 0){
            newList.insertAfter(j);
         }
         else
         {
            newList.prepend(j);
         }
         
      }
      
      newList.moveFront();
      // Loop through List to print out all lines in the correct order
      while(newList.index() >= 0) {
         output.println(token[newList.get()]);
         newList.moveNext();
      }
      
      input.close();
      output.close();
   }



}