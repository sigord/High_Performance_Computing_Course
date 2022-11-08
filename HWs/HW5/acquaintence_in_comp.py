"""
    Random greetings chain beetwen processors with synchronous MPI_SSend
"""
import random
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    name = f"My name processor {rank}"
    all_processors = list(range(size))
    
    print(f"I'm processor {rank}")
    
    if rank == 0:
        # first processor choose next random processor
        chain_history = [(name, rank)]
        dest = random.choice(all_processors[1:])
        comm.ssend(chain_history, dest=dest)
        print("and I'm stating this meeting")
    else:
        # all other processors get greetings from prev one and
        # send chain history to next random processor
        chain_history : list = comm.recv()
        print("and I received a message:")
        print(f"Hello processor {rank}. {chain_history[-1][0]}")
        
        chain_history.append((name, rank))
        used_processors = [rank for _, rank in chain_history]
        not_used_processors = list(set(all_processors) - set(used_processors))
        if len(not_used_processors) > 0:
            dest = random.choice(not_used_processors)
            comm.ssend(chain_history, dest=dest)
    
    MPI.Finalize()
            

if __name__ == "__main__":
    main()   

