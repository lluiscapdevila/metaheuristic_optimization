import time
from src.problems.problem_definition import ProblemPPeaks
from src.algorithms.simulated_annealing_algorithm import SimulatedAnnealing
from src.algorithms.genetic_algorithm import GeneticAlgorithm


def do_one_run(gn: int, gl: int, tf, alpha, popsize, pc, pm, temp, w: list, iterations: int = 10000):
    result_dict = {}
    problemSA = ProblemPPeaks(w=w)
    problemGA = ProblemPPeaks(w=w)
    problemSA.set_genen(gn)
    problemSA.set_genel(gl)
    problemSA.set_target_fitness(tf)
    problemGA.set_genen(gn)
    problemGA.set_genel(gl)
    problemGA.set_target_fitness(tf)
    sa = SimulatedAnnealing(gene_length=gl, gene_number=gn, temp=temp, problem=problemSA, iterations=iterations,
                            verbose=0, alpha=alpha)
    ga = GeneticAlgorithm(gene_length=gl, gene_number=gn, popsize=popsize, pc=pc, pm=pm, problem=problemGA)
    # Run Simulated Annealing
    sa.simulated_annealing()
    # Run Genetic Algorithm
    start_time = time.time()
    solution_list = []
    for i in range(iterations):
        ga.go_one_step()
        solution_list.append(ga.get_bestf())
        if problemGA.get_tf_known() & (ga.get_solution().get_fitness() >= problemGA.get_target_fitness()):
            print(f"Solution found for GA!! After {ga.problem.get_fitness_counter()} evaluations.")
            break

    result_dict['sa'] = {'iterations': sa.get_num_iterations(),
                         'best_score': sa.get_best_sol().get_fitness(),
                         'time_taken': sa.get_time_taken(),
                         'sol_history': [sol.get_fitness() for sol in sa.get_sol_history()]}
    result_dict['ga'] = {'iterations': ga.problem.get_fitness_counter(),
                         'best_score': ga.get_solution().get_fitness(),
                         'time_taken': time.time() - start_time,
                         'sol_history': [sol for sol in solution_list]}
    return result_dict
