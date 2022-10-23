#define ll long long
#include <omp.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdbool.h>
#include <string>


const unsigned int RADIUS = 1.0;

bool is_inside_circle(double x, double y, double radius)
{
    return (x * x + y * y) < radius;
}

double monte_carlo_method(ll N)
{
    ll i, incircle = 0;
    unsigned int seed, tid;
    double rand_x, rand_y;

    double start = omp_get_wtime();
    #pragma omp parallel private(i, tid, seed, rand_x, rand_y) reduction(+ : incircle)
    {
        tid = omp_get_thread_num();
        seed = tid * (unsigned int)time(NULL);

        #pragma omp for
        for (i = 0; i < N; ++i)
        {   
            rand_x = ((double)rand_r(&seed) / (double)RAND_MAX);
            rand_y = ((double)rand_r(&seed) / (double)RAND_MAX);
            incircle += is_inside_circle(rand_x, rand_y, RADIUS);
        }
        // printf("seed %d\n", seed);
    }
    double end = omp_get_wtime();
    printf("Time %f, points: %llu\n", end - start, N);
    return (double)(4.0 * incircle / N);
}

int main(int argc, char** argv)
{
    double estimated_pi;
    ll N = std::stoll(argv[1]);
    estimated_pi = monte_carlo_method(N);
    printf("Estimated Pi = %f\n", estimated_pi);
    printf("True Pi %f\n", M_PI);
    printf("Error = %f\n", fabs(estimated_pi - M_PI));
}
