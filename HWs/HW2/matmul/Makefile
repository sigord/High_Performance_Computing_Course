CC=g++
CFlAGS=-c -Wall
CCFLAGS=-std=c++17

SRC=$(wildcard *.cpp)
OBJ=$(patsubst %.cpp,%.o,$(SRC))
EXECUTABLE=matmul_benchmark

all: $(EXECUTABLE)

$(EXECUTABLE) : $(OBJ)
	$(CC) $(CCFLAGS) $(OBJ) -o $@

%.o:%.cpp
	$(CC) $(CFlAGS) $(CCFLAGS) $(OPTIMIZER) -c $< -o $@

run:
	./$(EXECUTABLE) $(N)

clean:
	rm -rf *.o $(EXECUTABLE)
