wget https://people.sc.fsu.edu/~jburkardt/cpp_src/linpack_bench/linpack_bench.cpp
wget https://people.sc.fsu.edu/~jburkardt/cpp_src/linpack_bench/linpack_bench.sh

chmod +x linpack_bench.sh
./linpack_bench.sh
./a.out | tee linpack_benchmark_result.txt
rm linpack_bench.sh linpack_bench.cpp a.out
