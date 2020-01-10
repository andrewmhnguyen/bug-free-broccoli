//Andrew Nguyen
//anguy224
//Program Assignment 1

import java.io.*;
import java.util.Scanner;

public class Lex
{
   public static void main(String[] args) throws IOException
   {
      Scanner input = null;
      PrintWriter output = null;
      String[] token = null;
      
      if (args.length!=2)
      {
         System.err.println("Usage: Lex infile outfile");
         System.exit(1);
      }
      
      input = new Scanner(new File(args[0]));
      
      int count = 0;
      while (input.hasNextLine())
      {
         count++;
         input.nextLine();
      }
      input.close();
      
      List newList = new List();
      token = new String[count];
      input = new Scanner(new File(args[0]));
      output = new PrintWriter(new FileWriter(args[1]));

      int count2 = -1;
      while (input.hasNextLine())
      {
         count2++;
         token[count2] = input.nextLine();
      }
      
      for (int i=0; i<token.length; i++)
      {
         String temp = token[i];
         
         int j = i-1;
         newList.moveBack();
         while (j>=0&&temp.compareTo(token[newList.get()])<=0)
         {
            j--;
            newList.movePrev();
         }
         
         if (newList.index() < 0){
            newList.prepend(i);
         }
         else
         {
            newList.insertAfter(i);
         }
      }
      
      newList.moveFront();
      while(newList.index()>=0) {
         output.println(token[newList.get()]);
         newList.moveNext();
      }
      
      input.close();
      output.close();
   }
}