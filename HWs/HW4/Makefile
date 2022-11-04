CC=g++-12
CFLAGS=-c -Wall -O3 -fopenmp
CCFLAGS=-std=c++17

SRC=$(wildcard *.cpp)
OBJ=$(patsubst %.cpp,%.o,$(SRC))
EXECUTABLE=matrix_power

all: $(EXECUTABLE)

$(EXECUTABLE) : $(OBJ)
	$(CC) $(CCFLAGS) $(OBJ) -o $@

%.o:%.cpp
	$(CC) $(CFlAGS) $(CCFLAGS) -c $< -o $@

run:
	./$(EXECUTABLE) $(N) $(POWER)

clean:
	rm -rf *.o $(EXECUTABLE)