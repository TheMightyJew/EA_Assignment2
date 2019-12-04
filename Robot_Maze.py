import random
import numpy
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

first_row =  [0, 0, 0, 0, 0, 0, 0]
second_row = [1, 1, 0, 1, 1, 1, 0]
third_row =  [0, 1, 0, 1, 0, 1, 1]
fourth_row = [0, 1, 1, 1, 1, 1, 0]
fifth_row =  [0, 0, 0, 0, 0, 0, 0]
enter_state = (1, 0)
exit_state =  (2, 6)

first_row1 =  [1, 0, 1, 1, 1, 1, 1]
second_row1 = [1, 0, 0, 0, 0, 0, 1]
third_row1 =  [1, 0, 1, 1, 1, 0, 1]
fourth_row1 = [1, 0, 0, 0, 1, 0, 1]
fifth_row1 =  [1, 1, 1, 1, 1, 1, 1]
enter_state1 = (0, 0)
exit_state1 =  (0, 2)


assignment_maze = [first_row, second_row, third_row, fourth_row, fifth_row]
challenge_maze = [first_row1, second_row1, third_row1, fourth_row1, fifth_row1]

maze = assignment_maze

def move_up(point):
    new_point = (point[0]-1, point[1])
    if legal_point(new_point):
        return new_point
    else:
        return point


def move_down(point):
    new_point = (point[0]+1, point[1])
    if legal_point(new_point):
        return new_point
    else:
        return point


def move_right(point):
    new_point = (point[0], point[1]+1)
    if legal_point(new_point):
        return new_point
    else:
        return point


def move_left(point):
    new_point = (point[0], point[1]-1)
    if legal_point(new_point):
        return new_point
    else:
        return point


move_action_dict = {'up': move_up, 'down': move_down, 'right': move_right, 'left': move_left }
move_dict = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}


def legal_point(point):
    return in_map(point) and (not is_wall(point))


def get_random_point(cols_num, rows_num):
    random_row = random.randrange(rows_num)
    random_col = random.randrange(cols_num)
    return random_row, random_col


def number_of_blanks():
    count = 0
    for row in maze:
        count += sum(row)
    return count


def initiate_first_generation():
    path = []
    num_of_blanks = min(len(maze)*len(maze[0]), int(number_of_blanks()*1.5))
    for i in range(num_of_blanks-2):
        while True:
            random_action = random.randrange(4)
            if not (i > 0 and opposite_action(random_action, path[i-1])):
                break
        path.append(random_action)
    return path


def in_map(point):
    rows = len(maze)
    cols = len(maze[0])
    if point[0] < 0 or point[0] >= rows or point[1] < 0 or point[1] >= cols:
        return False
    else:
        return True


'''
def get_random_neighbor(rows, cols, point):
    while True:
        random_direction = random.randrange(4)
        if random_direction == 0:
            neighbor = (point[0]-1, point[1])
        elif random_direction == 1:
            neighbor = (point[0]+1, point[1])
        elif random_direction == 2:
            neighbor = (point[0], point[1]-1)
        elif random_direction == 3:
            neighbor = (point[0], point[1]+1)
        if (not in_map(rows, cols, neighbor)) or is_wall(neighbor):
            continue
        else:
            return neighbor
'''


def opposite_action(action, compare_action):
    if (action+compare_action) % 4 == 1:
        return True
    else:
        return False


def mut_shuffle(individual):
    '''
    random_index = random.randrange(len(individual)-2) + 1
    random_point = get_random_neighbor(len(maze), len(maze[0]), individual[random_index - 1])
    individual[random_index] = random_point
    return individual,
    '''
    random_index = random.randrange(len(individual))
    for i in range(random_index,len(individual)-1):
        individual[i] = individual[i+1]
    while True:
        random_action = random.randrange(4)
        if opposite_action(random_action, individual[len(individual)-2]):
            continue
        else:
            individual[len(individual)-1] = random_action
            return individual,
    '''
    while True:
        random_action = random.randrange(4)
        if random_action == individual[random_index]:
            continue
        elif random_index > 0 and opposite_action(random_action, individual[random_index - 1]):
            continue
        elif random_index < len(individual)-1 and opposite_action(random_action, individual[random_index + 1]):
            continue
        else:
            individual[random_index] = random_action
            return individual,
    '''

def get_manhattan_distance(first_point, second_point):
    heuristic_manhattan = 0
    for i in [0, 1]:
        heuristic_manhattan += abs(first_point[i] - second_point[i])
    return heuristic_manhattan


def are_neighbors(first_point, second_point):
    return get_manhattan_distance(first_point, second_point) == 1


def is_wall(point):
    ans = not maze[point[0]][point[1]]
    return ans


def real_path_length(path):
    stayed_at_goal = 1
    for i in range(len(path)-2, -1, -1):
        if path[i] == path[len(path)-1]:
            stayed_at_goal += 1
        else:
            break
    path_length = len(path)-stayed_at_goal
    return path_length


def calculate_neighbors_faults(path, path_length):
    faults_sum = 0
    for i in range(0, path_length):
        distance = get_manhattan_distance(path[i], path[i+1])
        if distance == 0:
            distance = 2
        distance = distance*2 + 1
        faults_sum += (distance+1)
    return faults_sum


def count_neighbors_faults(path, path_length):
    count = 0
    for i in range(0, path_length):
        if not are_neighbors(path[i], path[i+1]):
            count += 1
    return count


def count_wall_faults(path):
    count = 0
    for point in path:
        if is_wall(point):
            count += 1
    return count


def num_of_dups(path):
    dic ={}
    for loc in path:
        if loc in dic:
            dic[loc] = dic[loc]+1
        else:
            dic[loc] = 0
    sum = 0
    for key in dic:
        sum += dic[key]
    return sum


def eval_path(path):
    closed_list = []
    point = enter_state
    closed_list.append(point)
    count = 0
    for action in path:
        point = move_action_dict[move_dict[action]](point)
        if point in closed_list:
            count += number_of_blanks()
        else:
            closed_list.append(point)
        count += 1
        if point == exit_state:
            break
    grade = count + get_manhattan_distance(point, exit_state)
    return grade,


'''
grade = 0
path_length = real_path_length(path)
neighbors_faults = count_neighbors_faults(path, path_length)
wall_faults = count_wall_faults(path)
grade += path_length
num_of_blanks = number_of_blanks(maze)
grade += num_of_blanks * neighbors_faults
grade += num_of_blanks * wall_faults
dups = num_of_dups(path)
grade += dups
return grade,
'''


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("Initialization", initiate_first_generation)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.Initialization)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_path)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mut_shuffle)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select", tools.selRoulette)


def main():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Median", numpy.median)
    stats.register("Best", numpy.min)
    stats.register("Worst", numpy.max)

    start_time = time.time();

    algorithms.eaSimple(pop, toolbox, cxpb = 0.7, mutpb = 0.001, ngen=1000, stats=stats, halloffame=hof, verbose=True)

    elapsed_time = time.time() - start_time
    print('%.2f  seconds' % elapsed_time)
    print(hof)

    return pop, stats, hof


if __name__ == "__main__":
    main()