"""
    Cellular automaton 
"""
import random
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd
from mpi4py import MPI
from typing import List
from argparse import ArgumentParser
from PIL import Image
from os.path import exists


ONE_EXPRESSION = "⬛️"
ZERO_EXPRESSION = "⬜️"
BORDERS = 2

DEFAULT_LEFT_BORDER = 0
DEFAULT_RIGHT_BORDER = 0

TAG_LEFT_TO_RIGHT = 0
TAG_RIGHT_TO_LEFT = 1

STAT_FILE_NAME = "ca_statistics.csv"

### Show result

def print_state(array : List[int]) -> None:
    print("".join([ONE_EXPRESSION if x else ZERO_EXPRESSION for x in array]))


def save_image(history : List[List[List[int]]], rule_id : int) -> None:
    line_history = [[elem for subarray in line for elem in subarray[1:-1]] for line in history][::-1]
    # old
    # plt.pcolormesh(line_history, cmap="binary")
    # ax = plt.gca()
    # ax.set_aspect('equal')
    # ax.set_xticks([])
    # ax.set_yticks([])
    # plt.savefig(f"ca_rules_images/cellular_automatom_rule{rule_id}.png", dpi = 300)
    # new
    pixels_bin = [elem for line in line_history for elem in line]
    im = Image.new("RGB", (len(line_history[0]), len(line_history)))
    pixels = [(255,255,255) if p == 1 else (0,0,0) for p in pixels_bin]
    im.putdata(pixels)
    im.save(f"ca_rules_images/cellular_automatom_rule{rule_id}.png")

def save_stat_image(df : pd.DataFrame) -> None:
    plt.plot(df.processors, df.time)
    plt.ylabel('Time in sec')
    plt.xlabel('Processors')
    plt.savefig('ca_mpi_stat_images/stat.png', dpi = 200)

### Core

def get_rule_pattern(rule_id : int) -> List[List[int]]:
    """
    Convert rule_id to binary and return all cases that
    correspond to one in new state.
    
    Example Rule 110
    pattern                    111 110 101 100 011 010 001 000
	new state (110 in binary)   0   1   1   0   1   1   1   0
    result                         110 101     011 010 001
    """
    binary_rule = "{0:08b}".format(rule_id)
    pattern = ["{0:03b}".format(i) 
               for i, v in enumerate(binary_rule[::-1]) if int(v) == 1]
    pattern = [list(map(int, x)) for x in pattern]
    return pattern

def update_state(array : List[int], 
                 pattern : List[List[int]]) -> List[int]:
    new_array = array.copy()
    for i in range(1, len(array) - 1):
        new_array[i] = int(array[i - 1 : i + 2] in pattern)
    return new_array

def start_automaton(epochs : int, array_len : int, 
                    rule_id : int, periodical : bool, 
                    verbose : bool, stat : bool) -> None:
    
    start_time = MPI.Wtime()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    if array_len % size != 0:
        if rank == 0:
            warnings.warn("Number of processors must be divisor of array length\n"
                            f"current size is {size} current length is {array_len}.\n"
                            "Now only one processor will be used.")
        size = 1
    
    # randomize array
    array_len_per_processor = array_len // size
    array = [random.choice([0, 1]) for _ in range(array_len_per_processor + BORDERS)]
    rule_pattern = get_rule_pattern(rule_id)
    
    if rank == 0:
        states_history = []
        
    # update state
    for _ in range(epochs):
        # get border values
        # print(rank)
        array = get_ghost_cells(array, comm, rank, size, periodical)
        # print initial state (array)
        full_array = comm.gather(array, root=0) if size > 1 else [array]
        if rank == 0:
            states_history.append(full_array)
            if verbose and not stat:
                print_state([elem for subarray in full_array for elem in subarray[1:-1]])
        # update state
        array = update_state(array, rule_pattern)
    
    # get last state results
    full_array = comm.gather(array, root=0) if size > 1 else [array]
    if rank == 0:
        end_time = MPI.Wtime()
        process_time = end_time - start_time
        states_history.append(full_array)
        
        # show last line and save image
        if verbose and not stat:
            print_state([elem for subarray in full_array for elem in subarray[1:-1]])
            print(f"Processors: {size}, Time: {process_time}")
            
            save_image(states_history, rule_id)
        
        # append line with stat to log file
        header = ['time', 'processors', 'arr_len', 'epochs', 'rule']
        data = [process_time, size, array_len, epochs, rule_id]
        if stat:
            if verbose:
                # save images with stat
                df = pd.read_csv(STAT_FILE_NAME)
                save_stat_image(df)
            else:
                # append data with stat to log file
                if exists(STAT_FILE_NAME):    
                    with open(STAT_FILE_NAME, mode='a', 
                            encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
                else:
                    with open(STAT_FILE_NAME, mode='w',
                            encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        writer.writerow(data)
      
    MPI.Finalize()

        
def get_ghost_cells(array : List[int], comm : MPI.Intracomm, 
                    rank : int, size : int, periodical : bool) -> List[int]:
    if size > 1:
        # right ghost border
        right_border = array[1] if periodical or 0 < rank else DEFAULT_RIGHT_BORDER
        comm.send(right_border, dest=(rank - 1) % size, tag=TAG_LEFT_TO_RIGHT)
        # left ghost border
        left_border = array[-2] if periodical or rank < (size - 1) else DEFAULT_LEFT_BORDER
        comm.send(left_border, dest=(rank + 1) % size, tag=TAG_RIGHT_TO_LEFT)
        # receive data
        array[-1] = comm.recv(tag=TAG_LEFT_TO_RIGHT)
        array[0] = comm.recv(tag=TAG_RIGHT_TO_LEFT)
    else:
        array[-1] = array[1] if periodical else DEFAULT_RIGHT_BORDER
        array[0] = array[-2] if periodical else DEFAULT_LEFT_BORDER
    return array

### Main

def setup_parser(parser: ArgumentParser) -> None:
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--rule", type=int, default=110)
    parser.add_argument("--periodical", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--stat", action="store_true", default=False)


def main() -> None:
    parser = ArgumentParser(
        prog="cellular_automaton",
        description="Cellular automaton implementation with MPI parallelism",
    )
    setup_parser(parser)

    arguments = parser.parse_args()

    start_automaton(
        epochs = arguments.epochs,
        array_len = arguments.size,
        rule_id = arguments.rule,
        periodical = arguments.periodical,
        verbose = arguments.verbose,
        stat = arguments.stat,
    )


if __name__ == "__main__":
    main()