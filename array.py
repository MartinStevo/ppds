from numba import cuda
import numpy as numpy


# print(cuda.gpus)


@cuda.jit
def my_kernel(io_array):
    # tx = cuda.threadIdx.x
    # ty = cuda.blockIdx.x
    # bw = cuda.blockDim.x
    # pos = tx + ty * bw
    pos = cuda.grid(1)

    if pos < io_array.size:
        io_array[pos] *= 2


data = numpy.ones(512)
threads_per_block = 32
blocks_per_grid = (data.size + (threads_per_block - 1))

my_kernel[blocks_per_grid, threads_per_block](data)

print(data)
