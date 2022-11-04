#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include "matrix_pow.h"

void naive_ranking(double *matrix, double *result, int N);
void pagerank(double *matrix, double *result, int N, double damping_factor, int max_iter);