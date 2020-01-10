//Andrew Nguyen
//anguy224
//Program Assignment 3

import java.io.*;
import java.util.Scanner;

public class Sparse {
	public static void main(String[] args) throws IOException {
		Scanner input = null;
		PrintWriter output = null;
	    String line = null;
	    String[] token = null;
	    int lineNumber = 0;
	    
	    if(args.length < 2) {
	    	System.err.println("Usage: Sparse infile outfile");
	        System.exit(1);
	    }
	      
	    input = new Scanner(new File(args[0]));
	    output = new PrintWriter(new FileWriter(args[1]));
	    
	    int n = Integer.parseInt(input.next())+1;
		int a = Integer.parseInt(input.next());
		int b = Integer.parseInt(input.next());

		Matrix A = new Matrix(n);
		Matrix B = new Matrix(n);
		
		for(int i=0; i<a; i++)
		{
			int row = Integer.parseInt(input.next());
			int col = Integer.parseInt(input.next());
			double val = Double.parseDouble(input.next());
			A.changeEntry(row,col,val);
		}
		
		for(int i=0; i<b; i++)
		{
			int row2 = Integer.parseInt(input.next());
			int col2 = Integer.parseInt(input.next());
			double val2 = Double.parseDouble(input.next());
			B.changeEntry(row2,col2,val2);
		}

	    output.println("A has " + A.getNNZ() + " non-zero entries:");
	    output.println(A);
	      
	    output.println("B has " + B.getNNZ() + " non-zero entries:");
	    output.println(B);

	    output.println("(1.5)*A =");
	    output.println(A.scalarMult(1.5));

	    output.println("A+B =");
	    output.println(A.add(B));
	      
	    output.println("A+A =");
	    output.println(A.add(A));

	    output.println("B-A =");
	    output.println(B.sub(A));
	      
	    output.println("A-A =");
	    output.println(A.sub(A));
	      
	    output.println("Transpose(A) =");
	    output.println(A.transpose());
	      
	    output.println("A*B =");
	    output.println(A.mult(B));
	      
	    output.println("B*B =");
	    output.println(B.mult(B));
	      
	    input.close();
	    output.close();
	}

}
