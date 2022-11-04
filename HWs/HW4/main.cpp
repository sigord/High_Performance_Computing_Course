#include "matrix_pow.h"
#include "pagerank.h"

int main(int args, char *argv[]){
    int N = atoi(argv[1]);
    int power = atoi(argv[2]);
    printf("N = %d, power = %d\n", N, power);

    double *matrix = (double *) malloc(N * N * sizeof(double));
    random_matrix(matrix, N);
    printf("Generated adjacency matrix:\n");
    print_matrix(matrix, N);

    double *powered = (double *) malloc(N * N * sizeof(double));
    memcpy(powered, matrix, N * N * sizeof(double));    
    matrix_power(powered, N, power);
    printf("Matrix powered by %d:\n", power);
    print_matrix(powered, N);
    

    double *naive_ranking_result = (double *) malloc(N * sizeof(double));
    naive_ranking(matrix, naive_ranking_result, N);

    double *pagerank_result = (double *) malloc(N * sizeof(double));
    double damping_factor = 0.85;
    int num_iterations = 10;
    pagerank(matrix, pagerank_result, N, damping_factor, num_iterations);

    printf("Ranking results:\n");
    for (int i = 0; i < N; ++i) {
        printf("%2d: naive_ranking=%.4lf, pagerank=%.4lf\n",
               i, naive_ranking_result[i], pagerank_result[i]);
    }

    free(matrix);
    free(pagerank_result);
    free(naive_ranking_result);
    free(powered);
}