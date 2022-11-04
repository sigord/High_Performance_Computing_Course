#include "matrix_pow.h"

void random_matrix(double *matrix, int N){
    unsigned int seed = (unsigned) time(NULL);

    for (int i = 0; i < N; ++i){
        for (int j = 0; j < N; ++j){
            matrix[i * N + j] = (i == j) ? 0 : rand_r(&seed) & 1;
        }
    }
}

void print_matrix (double *matrix, int N){
    for (int i = 0; i < N; ++i){
        for (int j = 0; j < N; ++j){
            printf("%.1lf ", matrix[i * N + j]);
        }
        printf("\n");
    }
    printf("\n");
}

void print_vector (double *vector, int N){
    for (int i = 0; i < N; ++i){
       printf("%.1lf ", vector[i]);   
    }
    printf("\n");
}

void mv_mult(double *matrix, double *vector, double *result, int N){
    #pragma omp parallel for
    for (int i = 0; i < N; ++i){
        for (int k = 0; k < N; ++k){
            result[i] += matrix[i * N + k] * vector[k];
        }
    }
}

void mm_mult(double * matrix1, double * matrix2, int N){
    double *result = (double *) malloc(N * N * sizeof(double));
    #pragma omp parallel for
    for (int i = 0; i < N; ++i){  
        for (int j = 0; j < N; ++j){
            for(int k = 0; k < N; ++k){
                result[i * N + j] = result[i * N + j] + matrix1[i * N + k] * matrix2[k * N + j];
            }
        }
    }
    memcpy(matrix1, result, N * N * sizeof(double));
    free(result);
}

void matrix_power(double *matrix, int N, int power){
    
    double *matrix_pow = (double *) malloc(N * N * sizeof(double));

    memcpy(matrix_pow, matrix, N * N * sizeof(double));
    
    power--;
    
    while (power > 0) {
        //if power is odd
        if (power & 1) {
            mm_mult(matrix, matrix_pow, N);
        }
        mm_mult(matrix_pow, matrix_pow, N);
        //power = power / 2
        power = power >> 1;
    }

    free(matrix_pow);
}