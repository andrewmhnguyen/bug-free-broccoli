//Andrew Nguyen
//anguy224
//Program Assignment 3

package pa3;

public class Matrix {
	private static class Entry{
		
		int col;
		double val;
		
		Entry(int col, double val){
			this.col = col;
			this.val = val;
		}
		
		public boolean equals(Object x) {
			boolean eq = false;
			if(x instanceof Entry) {
				Entry compare = (Entry) x;
				if (this.col == compare.col && this.val == compare.val) {
					eq = true;
				}
			}
			return eq;
		}
		
		public String toString() {
			return "(" + col + ")" + ", " + "(" + val + ")";
		}
	}

	//variables
	List[] row;
	
	// Constructor
	Matrix(int n) // Makes a new n x n zero Matrix. pre: n>=1
	{
		if (n<1) {
			throw new RuntimeException("Matrix Error: cannot construct matrix with a negative number");
		}
		
		row = new List[n+1];
		for(int i=1; i<n+1; i++) {
			row[i] = new List();
		}
		
	}
	
	int getSize() // Returns n, the number of rows and columns of this Matrix
	{
		return row.length;
	}
	
	int getNNZ() // Returns the number of non-zero entries in this Matrix
	{
		int NNZ = 0;
		for( int i=1; i<=this.getSize(); i++) {
			for( int j=0; j<this.row[i].length(); j++) {
				NNZ ++;
			}
		}
		return NNZ;
	}
	
	public boolean equals(Object x) // overrides Object's equals() method
	{
		if (x instanceof Matrix) {
			Matrix compare = (Matrix) x;
			if(this.getSize() != compare.getSize() || this.getNNZ() != compare.getNNZ()) {
				return false;
			}
			for ( int i=1; i<=this.getSize(); i++) {
				boolean check = this.row[i].equals(compare.row[i]);
				if( check == false) {
					return false;
				}
			}
			
		}
		return true;
	}
	
	
	// Manipulation procedures
	void makeZero() // sets this Matrix to the zero state
	{
		for (int i=1; i<=row.length; i++) {
			row[i] = new List();
		}
	}
	
	Matrix copy()// returns a new Matrix having the same entries as this Matrix
	{
		Matrix copy = new Matrix(this.getSize());
		for( int i=1; i<=this.getSize(); i++) {
			this.row[i].moveFront();
			for( int j=0; j<this.row[i].length(); j++) {
				copy.row[i].append(this.row[i].get());
				this.row[i].moveNext();
			}
		}
		
		return copy;
	}
	
	void changeEntry(int i, int j, double x)
	// changes ith row, jth column of this Matrix to x
	// pre: 1<=i<=getSize(), 1<=j<=getSize()
	{
		if( i<1 || i>this.getSize() || j<1 || j>this.getSize() ) {
			throw new RuntimeException ("Matrix Error: index out of range");
		}
		
		boolean match = false;
		this.row[i].moveFront();
		Entry newEntry = new Entry(j,x);
		
		
		while ( this.row[i].index() != -1) {
			Entry place = (Entry) this.row[i].get();
			match = (place.col == j);
			if (match == true) {
				if (x != 0) {
					place.val = x;
				}
				else {
					this.row[i].delete();
				}
			}
			this.row[i].moveNext();
		}
		
		if( match == false && x != 0) {
			this.row[i].moveFront();
			if (this.row[i].index() == -1) {
				this.row[i].append(newEntry);
			}
			else {
				while( ((Entry)this.row[i].get()).col < j) {
					this.row[i].moveNext();
					if ( this.row[i].index() == -1) {
						break;
					}
				}
				if ( this.row[i].index() == -1) {
					this.row[i].append(newEntry);
				}
				else {
					row[i].insertBefore(newEntry);
				}
			}
		}
	}
	Matrix scalarMult(double x)
	// returns a new Matrix that is the scalar product of this Matrix with x
	{
		Matrix newMatrix = new Matrix(this.getSize());
		for (int i=1; i<=this.getSize(); i++) {
			newMatrix.row[i].moveFront();
			while ( this.row[i].index() != -1) {
				Entry temp = (Entry) newMatrix.row[i].get();
				double newVal = x*temp.val;
				Entry newEntry = new Entry(temp.col, newVal);
				newMatrix.row[i].append(newEntry);
				this.row[i].moveNext();
			}
			
		}
		
		return newMatrix;
	}
	
	private static List addHelp(List P, List Q) 
	//computes two lists added together
	{
		List newList = new List();
		P.moveFront();
		Q.moveFront();
		while (P.index() != -1 || Q.index() != -1) {
			if (P.index() >= 0 && Q.index() == -1) {
				Entry newEntry = (Entry) P.get();
				newList.append(newEntry);
				P.moveNext();
			}
			else if (P.index() == -1 && Q.index() >= 0) {
				Entry newEntry = (Entry) Q.get();
				newList.append(newEntry);
				Q.moveNext();
			}
			else {
				Entry val1 = (Entry) P.get();
				Entry val2 = (Entry) Q.get();
				if(val1.col<val2.col) {
					Entry newEntry = new Entry(val1.col, val1.val);
					newList.append(newEntry);
					P.moveNext();
				}
				else if(val1.col>val2.col) {
					Entry newEntry = new Entry(val2.col, val2.val);
					newList.append(newEntry);
					Q.moveNext();
				}
				else {
					double newVal = val1.val + val2.val;
					int newCol = val1.col;
					newList.append(new Entry(newCol, newVal));
					P.moveNext();
					Q.moveNext();
				}
			}
		}
		return newList;
	}
	
	
	Matrix add(Matrix M)
	// returns a new Matrix that is the sum of this Matrix with M
	// pre: getSize()==M.getSize()
	{
		if (getSize()!=M.getSize()) {
			throw new RuntimeException ("Matrix Error: Matrices aren't the same size");
		}
		
		Matrix newMatrix = new Matrix(getSize());
		for ( int i=1; i<=this.getSize(); i++) {
			newMatrix.row[i] = addHelp(this.row[i], M.row[i]);
		}
		return newMatrix;
		
		
	}
	Matrix sub(Matrix M)
	// returns a new Matrix that is the difference of this Matrix with M
	// pre: getSize()==M.getSize()
	{
		if (getSize()!=M.getSize()) {
			throw new RuntimeException ("Matrix Error: Matrices aren't the same size");
		}
		
		Matrix newMatrix = new Matrix(getSize());
		M = M.scalarMult(-1);
		for ( int i=1; i<=this.getSize(); i++) {
			newMatrix.row[i] = addHelp(this.row[i], M.row[i]);
		}
		return newMatrix;
		
	}
	
	private static double dot(List P, List Q)
	// computes the dot product of 2 lists 
	{
		double dot = 0;
		P.moveFront();
		Q.moveFront();
		while (P.index() != -1 || Q.index() != -1) {
			Entry val1 = (Entry) P.get();
			Entry val2 = (Entry) Q.get();
			if (val1.col<val2.col) {
				P.moveNext();
			}
			else if (val1.col>val2.col) {
				Q.moveNext();
			}
			else {
				dot += val1.val*val2.val;
				P.moveNext();
				Q.moveNext();
			}
				
		}
		return dot;
	}
	
	Matrix transpose()
	// returns a new Matrix that is the transpose of this Matrix
	{
		Matrix newMatrix = new Matrix(this.getSize());
		for( int i=1; i<=this.getSize(); i++) {
			this.row[i].moveFront();
			while(row[i].index() != -1) {
				int newRow = ((Entry)this.row[i].get()).col;
				int newCol = i;
				double newVal = ((Entry)this.row[i].get()).val;
				newMatrix.changeEntry(newRow,newCol,newVal);
				this.row[i].moveNext();
			}
		}
		return newMatrix;
	}
	
	
	Matrix mult(Matrix M)
	// returns a new Matrix that is the product of this Matrix with M
	// pre: getSize()==M.getSize()
	{
		if (getSize()!=M.getSize()) {
			throw new RuntimeException ("Matrix Error: Matrices aren't the same size");
		}
		
		Matrix newMatrix = new Matrix(this.getSize());
		Matrix mul = M.transpose();
		
		for ( int i=1; i<=this.getSize(); i++) {
			for( int j=1; j<=this.getSize(); j++) {
				double newVal = dot (this.row[i],mul.row[i]);
				newMatrix.changeEntry(i, j, newVal);
			}
		}
		return newMatrix;
	}
 
	// Other functions
	public String toString() // overrides Object's toString() method
	{
		String toPrint = "";
		for (int i=1; i<=row.length; i++) {
			if ( row[i].length() > 0) {
				toPrint += (i + ": " + row[i] +"\n");
			}
		}
		return toPrint;
	}
	

}