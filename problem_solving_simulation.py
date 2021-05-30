import time
import pickle
import numpy as np
from src.problems.problem_definition import ProblemPPeaks
from src.utils.do_one_run import do_one_run


if __name__ == '__main__':

    SAVE_FILE_PATH = "drive/MyDrive/"
    FILE_NAME = "results_10000.pickle"
    W = np.array([
        2902, 5235, 357, 6058, 4846, 8280, 1295, 181, 3264,
        7285, 8806, 2344, 9203, 6806, 1511, 2172, 843, 4697,
        3348, 1866, 5800, 4094, 2751, 64, 7181, 9167, 5579,
        9461, 3393, 4602, 1796, 8174, 1691, 8854, 5902, 4864,
        5488, 1129, 1111, 7597, 5406, 2134, 7280, 6465, 4084,
        8564, 2593, 9954, 4731, 1347, 8984, 5057, 3429, 7635,
        1323, 1146, 5192, 6547, 343, 7584, 3765, 8660, 9318,
        5098, 5185, 9253, 4495, 892, 5080, 5297, 9275, 7515,
        9729, 6200, 2138, 5480, 860, 8295, 8327, 9629, 4212,
        3087, 5276, 9250, 1835, 9241, 1790, 1947, 8146, 8328,
        973, 1255, 9733, 4314, 6912, 8007, 8911, 6802, 5102,
        5451, 1026, 8029, 6628, 8121, 5509, 3603, 6094, 4447,
        683, 6996, 3304, 3130, 2314, 7788, 8689, 3253, 5920,
        3660, 2489, 8153, 2822, 6132, 7684, 3032, 9949, 59,
        6669, 6334
    ])
    C = 300500  # Target fitness
    GN = 128  # Gene number
    GL = 1  # Gene length
    POPSIZE = 32  # Population size
    PC = 0.95  # Crossover probability
    PM = 0.05  # Mutation probability (usually 1/(GN*GL))
    tf = C  # Target fitness being sought
    MAX_ITER = 10000  # Max iterations per algorithm
    ALPHA = 0.99  # Temperature reduction rate for SA
    TEMP = 10  # Starting temperature for SA
    NUM_SIMULATIONS = 100  # Number of simulations. 1 Simulation runs GA and SA for MAX_ITER iterations.
    problemSA = ProblemPPeaks(w=W)
    problemGA = ProblemPPeaks(w=W)
    problemSA.set_genen(GN)
    problemSA.set_genel(GL)
    problemSA.set_target_fitness(tf)
    problemGA.set_genen(GN)
    problemGA.set_genel(GL)
    problemGA.set_target_fitness(tf)

    iteration_results = {}
    start_time = time.time()
    for i in range(NUM_SIMULATIONS):
        iteration_results[i] = do_one_run(gn=GN, gl=GL, tf=tf, alpha=ALPHA, popsize=POPSIZE, pc=PC,
                                          pm=PM, temp=TEMP, w=W, iterations=MAX_ITER)
    print(f"Running SA and GA for {NUM_SIMULATIONS} simulations and {MAX_ITER} iterations took {time.time() - start_time} seconds.")

    with open(SAVE_FILE_PATH+FILE_NAME, "wb") as output_file:
        pickle.dump(iteration_results, output_file)
    with open(SAVE_FILE_PATH+FILE_NAME, "rb") as input_file:
        iteration_results = pickle.load(input_file)
