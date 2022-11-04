#include "pagerank.h"


void naive_ranking(double *matrix, double *result, int N){
    int total_links = 0;

    #pragma omp parallel for reduction(+:total_links)
    for(int i = 0; i < N; ++i){
        for(int j = 0;j < N; ++j){
            result[i] += matrix[j * N + i];
        }
        total_links += result[i];
    }

    #pragma omp parallel for
    for(int i = 0; i < N; ++i){
        result[i] = result[i]/total_links;
    }
}

void pagerank(double *matrix, double *pagerank_vector, int N,
              double damping_factor, int max_iter){
    
    double *fixed_matrix = (double *) malloc(N * N * sizeof(double));

    #pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        double num_outbound_links = 0;

        for (int j = 0; j < N; ++j) {
            num_outbound_links += matrix[i * N + j];
        }

        for (int j = 0; j < N; ++j) {
            fixed_matrix[j * N + i] = (num_outbound_links == 0) ? 1.0 / N : matrix[i * N + j] / num_outbound_links;
        }
    }
    
    double *prev_pagerank_vector = (double *) malloc(N * sizeof(double));

    #pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        prev_pagerank_vector[i] = 1.0 / N;
    }

    for (int i = 0; i < max_iter; ++i) {

        mv_mult(fixed_matrix, prev_pagerank_vector, pagerank_vector, N);

        for (int j = 0; j < N; ++j) {
            pagerank_vector[j] = damping_factor * pagerank_vector[j] + (1 - damping_factor) / N;
        }

        memcpy(prev_pagerank_vector, pagerank_vector, N * sizeof(double));
    }

    free(fixed_matrix);
    free(prev_pagerank_vector);
}