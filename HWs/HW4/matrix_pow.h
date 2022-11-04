#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <time.h>

void random_matrix(double *matrix, int N);
void print_matrix (double *matrix, int N);
void print_vector (double *vector, int N);
void mv_mult(double *matrix, double *vector, double *result, int N);
void mm_mult(double *matrix1, double *matrix2, int N);
void matrix_power(double *matrix, int N, int power);