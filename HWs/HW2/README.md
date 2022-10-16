- [x] 1. Реализовать классическое перемножение матриц и умножение матрицы на вектор на C/C++ с разным порядком циклов (25\%)
- [x] 2.  Разбейте на модули, со статической линковкой скомпилируйте текст, подготовьте Makefile, проверьте флаги -g,  -O3  (25\%)\\
- [x] 3. Измерьте времена исполнения для размеров $N = 500, 512, 1000, 1024, 2000, 2048$  (25\%)
	- [ ] В т.ч. проведите сравнение с виртуальной машиной, докером (опционально)

```bash
task 2, task 3
cd matmul
bash run_benchmark.sh
```
 
 OR

```bash
cat matmul/benchmark_result.txt
```

- [x] 4. И базовые скрипты баш  (25\%)
	- [x] 1. Organize FOR loop printing the even numbers only from 100 to 1000
	- [x] 2. Initialize the array of 10-20 elements and organize FOR loop printing the elements of array 
	- [x] 3. Compute 100 + 0.5 in bash 
	- [x] 4. Check if file ”Linux” exists in present directory. If yes, print message ”course”. If no, print message ”very easy” and create the ”Linux” file with text ”course is easy”.
- [x] 5. Бонус за линпак(+20\%)

```bash
cd linpack
./run_bench.sh
```

Результат

```txt
LINPACK_BENCH
C++ version

The LINPACK benchmark.
Language: C++
Datatype: Double precision
Matrix order N               = 1000
Leading matrix dimension LDA = 1001

	Norm. Resid      Resid           MACHEP         X[1]          X[N]

	6.49151     7.20701e-13     2.22045e-16               1               1

	Factor     Solve      Total     MFLOPS       Unit      Cray-Ratio

0.406421   0.001265   0.407686    1640.15  0.0012194    7.28011
```

- [ ] 6. Супербонус протестируйте алгоритм Штрассена   (+20\%)
