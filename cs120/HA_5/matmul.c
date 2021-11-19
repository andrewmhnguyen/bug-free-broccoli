#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>

#define SIZE 1024

volatile __uint64_t A[SIZE][SIZE];
volatile __uint64_t B[SIZE][SIZE];
volatile __uint64_t C[SIZE][SIZE];
volatile __uint64_t D[SIZE][SIZE];
volatile __uint64_t E[SIZE][SIZE];
volatile __uint64_t F[SIZE][SIZE];

void init(volatile __uint64_t A[][SIZE], volatile __uint64_t B[][SIZE])
{
	int r, c;

	for (c = 0; c < SIZE; c++) {
		for (r = 0; r < SIZE; r++) {
			A[r][c] = rand();
			B[r][c] = rand();
		}
	}
}

int verify(volatile __uint64_t C[][SIZE], volatile __uint64_t D[][SIZE])
{
	int r, c;

	for (c = 0; c < SIZE; c++) {
		for (r = 0; r < SIZE; r++) {
			if (C[r][c] != D [r][c]) {
				printf("error!\n");
				return -1;
			}
			
		}
	}
	return 0;
}

void matmul(volatile __uint64_t A[][SIZE], volatile __uint64_t B[][SIZE])
{
	int rowA, colB, idx;

	for (rowA = 0; rowA < SIZE; rowA++) {
		for (colB = 0; colB < SIZE; colB++) {
			for (idx = 0; idx < SIZE; idx++) {
				C[rowA][colB] += A[rowA][idx] * B[idx][colB];
			}
		}
	}
}

//stores transpose of first into second, should be used to store transpose of B into F. 
void transpose(volatile __uint64_t A[][SIZE], volatile __uint64_t B[][SIZE]){ 
	int i, j;
	for (i = 0; i < SIZE; i++) {
		for (j = 0; j < SIZE; j++) {
			B[i][j] = A[j][i];
		}
	}
}

//create a new matmul that multiplies matrix for transposed matrix,
void matmulTranspose(volatile __uint64_t A[][SIZE], volatile __uint64_t B[][SIZE]){
	int rowA, rowB, idx;
	for(rowA=0;rowA<SIZE;rowA++){
		for (rowB = 0; rowB <SIZE; rowB++) {
			for(idx = 0; idx < SIZE; idx++) {
				D[rowA][rowB] += A[rowA][idx] * B[rowB][idx];
			}
		}
	}
}

//multiplies matrices using tiling and a transposed matrix
void matmulTile(volatile __uint64_t A[][SIZE], volatile __uint64_t B[][SIZE], int tile){
	int rowA, rowB, idx, a, b, c;
	for (rowA = 0; rowA < SIZE; rowA+=tile) {
		for (rowB = 0; rowB < SIZE; rowB+=tile) {
			for (idx = 0; idx < SIZE; idx+=tile) {
				for (a = rowA; a < rowA+tile; a++) {
				        for (b = rowB; b < rowB+tile; b++) {
						for (c = idx; c < idx+tile; c++) {
							E[a][b] += A[a][c] * B[b][c];
						}
					}
				}
			}
		}
	}
}

int main(int argc, char **argv)
{
	clock_t t;
	double time_taken;

	init(A, B);
	memset((__uint64_t**)C, 0, sizeof(__uint64_t) * SIZE * SIZE);
	
	t = clock();
	matmul(A, B);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("Matmul took %f seconds to execute \n", time_taken);


	transpose(B,F);
	t=clock();
	matmulTranspose(A,F);
	t=clock()-t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	printf("MatmulTranspose took %f seconds to execute \n", time_taken);

	verify(C,D);	

	t = clock();	
	matmulTile(A, F, 1);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	printf("MatmulTile(1) took %f seconds to execute \n", time_taken);
	verify(C,E);
	
	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 2);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(2) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 4);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(4) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 8);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(8) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 16);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(16) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 32);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(32) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 64);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds

	printf("MatmulTile(64) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 128);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(128) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 256);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(256) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 512);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(512) took %f seconds to execute \n", time_taken);
	verify(C,E);

	memset((__uint64_t**)E, 0, sizeof(__uint64_t) * SIZE * SIZE);
	t = clock();
	matmulTile(A, F, 1024);
	t = clock() - t;
	time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
	
	printf("MatmulTile(1024) took %f seconds to execute \n", time_taken);

	verify(C,E);
	
}
