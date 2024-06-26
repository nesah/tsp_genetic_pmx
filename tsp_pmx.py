import random
import math
import heapq
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


points2 = {
    'A': (2, 4),
    'B': (6, 5),
    'C': (10, 5),
    'D': (7, 8),
    'E': (4, 7),
    'F': (7, 4),
    'G': (11, 6),
    'H': (10, 8),
    'I': (9, 3),
    'J': (11, 4)
}


def time_travel(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'Traversal time: {t2}')
        # return t2
        return result

    return wrapper


# calculate distance between 2 points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# calculate total distance of route
def total_distance(route, point_set):
    total = 0
    for i in range(len(route) - 1):
        if route[i] in point_set and route[i + 1] in point_set:
            total += distance(point_set[route[i]], point_set[route[i + 1]])
        else:
            raise ValueError("Invalid route key found.")
    return total


def generate_initial_population(population_size, point_set):
    population = []

    while len(population) < population_size:
        route = list(point_set.keys())
        random.shuffle(route)

        # check if route already in population
        if route not in population:
            population.append(route)

    return population


route_index = 5
population = generate_initial_population(10, points2)
selected_route = population[route_index]

print("Selected Route:", selected_route)
print("Total Distance of Selected Route:", total_distance(selected_route, points2))


def swap(arr1, arr2, start, end):
    for i in range(start, end + 1):
        arr1[i], arr2[i] = arr2[i], arr1[i]


def crossover(p1, p2, start, end):
    c1 = p1
    c2 = p2

    swap(c1, c2, start, end)

    index1 = []
    index2 = []

    for i in range(len(c1)):
        if i in range(start, end + 1):
            continue
        for j in range(len(c1)):
            if (c1[j] == c1[i]) and (i != j):
                index1.append(i)

    for i in range(len(c2)):
        if i in range(start, end + 1):
            continue
        for j in range(len(c2)):
            if (c2[j] == c2[i]) and (i != j):
                index2.append(i)

    index2.reverse()
    # crossing
    for i in range(len(index1)):
        c1[index1[i]], c2[index2[i]] = c2[index2[i]], c1[index1[i]]

    return (c1, c2)


def mutation(array):
    mutationList = [array]
    for idx in enumerate(array):
        x = random.randrange(idx[0], len(array))
        array[idx[0]], array[x] = array[x], array[idx[0]]
        mutationList.append(array)
    return mutationList


def get_fitness(array, point_set):
    fitness = 0
    for i in range(len(array) - 1):
        fitness += distance(point_set[array[i]], point_set[array[i + 1]])
    return fitness


def animate_generation(set, points, fitness, is_repeat=False):

    fig, ax = plt.subplots()

    line, = ax.plot([], [], lw=1)
    generation_text = ax.text(0.01, 0.98, '', ha='left', va='top', transform=ax.transAxes, fontsize=8)
    fitness_text = ax.text(0.01, 0.95, '', ha='left', va='top', transform=ax.transAxes, fontsize=8)

    def init():
        plt.title('TSP Solution Timeline')

        plt.xlabel("x")
        plt.ylabel("y")

        # plt.plot(ax.get_xlim(), [0, 0], 'k--')
        # plt.plot([0, 0], ax.get_ylim(), 'k--')

        # plt.xlim(-12, 12), plt.ylim(-12, 12)

        x = [points[i][0] for i in set[0]]
        y = [points[i][1] for i in set[0]]
        plt.plot(x, y, 'co')

        for i in range(len(set[0]) - 1):
            plt.annotate(f"{set[0][i]}", (x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.1), fontsize=10)
            # plt.annotate(f"{i}", (x[i], y[i]), xytext=(x[i] + 0.1, y[i] + 0.1), fontsize=10)

        line.set_data([], [])
        return line,

    def animate(frame):
        x = [points[i][0] for i in set[frame] + [set[frame][0]]]
        y = [points[i][1] for i in set[frame] + [set[frame][0]]]

        generation_text.set_text(f"Generation: {frame}")
        fitness_text.set_text(f"Fitness: {fitness[frame]}")

        line.set_data(x, y)

        return line

    anim = FuncAnimation(fig, animate, frames=range(0, len(set), 20),
                         init_func=init, interval=1, repeat=is_repeat)

    plt.show()


def graph_generations(fitness):
    plt.title('Generation Timeline')

    plt.plot([i for i in range(len(fitness))], fitness)
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    plt.show()


@time_travel
def TSP(start, itr, point_set):
    parent1 = math.inf
    parent2 = math.inf
    fitness = []
    population = []
    all_generations = []
    all_fitness = []

    population = generate_initial_population(2, point_set)
    for i in population:
        i.remove(start)
        i.insert(0, start)
        i.append(start)

    # get fitness of each population
    for i in range(len(population)):
        heapq.heappush(fitness, (get_fitness(population[i], point_set), i))

    temp = heapq.heappop(fitness)
    parent1 = (temp[0], population[temp[1]])

    for m in range(itr):

        while True:
            # if len(fitness) > 0:
            temp = generate_initial_population(1, point_set)[0]
            temp.remove(start)
            temp.insert(0, start)
            temp.append(start)

            parent2 = (get_fitness(temp, point_set), temp)

            childs = crossover(parent1[1][1:len(parent1[1]) - 1], parent2[1][1:len(parent2[1]) - 1], 2, 6)

            mutations = mutation(childs[0]) + mutation(childs[1])
            random.shuffle(mutations)

            temp_child = (math.inf, 0)

            while (temp_child[0] >= parent1[0] + 0.05) or (temp_child[0] >= parent2[0] + 0.05):
                if len(mutations) <= 0:
                    break

                temp = mutations.pop()
                # apply start and end position
                temp.insert(0, start)
                temp.append(start)

                temp_child = (get_fitness(temp, point_set), temp)

            if len(mutations) <= 0:
                print(f"Gen #{m} current lowest path:{parent1[0]} ")
                all_generations.append(parent1[1])
                all_fitness.append(round(parent1[0], 3))
                break
            else:
                print(f"Gen #{m} current lowest path:{temp_child[0]} ")
                all_generations.append(temp_child[1])
                all_fitness.append(round(temp_child[0], 3))
                parent1 = temp_child
                break

    return all_generations, all_fitness

def TSP_2(start, itr, point_set):
    parent1 = math.inf
    parent2 = math.inf
    fitness = []
    population = []
    all_generations = []
    all_fitness = []

    population = generate_initial_population(2, point_set)
    for i in population:
        i.remove(start)
        i.insert(0, start)
        i.append(start)

    # get fitness of each population
    for i in range(len(population)):
        heapq.heappush(fitness, (get_fitness(population[i], point_set), i))

    temp = heapq.heappop(fitness)
    parent1 = (temp[0], population[temp[1]])

    for m in range(itr):

        while True:
            # if len(fitness) > 0:
            temp = generate_initial_population(1, point_set)[0]
            temp.remove(start)
            temp.insert(0, start)
            temp.append(start)

            parent2 = (get_fitness(temp, point_set), temp)

            childs = crossover(parent1[1][1:len(parent1[1]) - 1], parent2[1][1:len(parent2[1]) - 1], 2, 6)

            mutations = mutation(childs[0]) + mutation(childs[1])
            random.shuffle(mutations)

            temp_child = (math.inf, 0)

            while (temp_child[0] >= parent1[0] + 2) or (temp_child[0] >= parent2[0] + 2):
                if len(mutations) <= 0:
                    break

                temp = mutations.pop()
                # apply start and end position
                temp.insert(0, start)
                temp.append(start)

                temp_child = (get_fitness(temp, point_set), temp)

            if len(mutations) <= 0:
                pass
            else:
                print(f"Gen #{m} current lowest path:{temp_child[0]} ")
                all_generations.append(temp_child[1])
                all_fitness.append(round(temp_child[0], 3))
                parent1 = temp_child
                break

    return all_generations, all_fitness


gene_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
array1 = [2, 1, 3, 5, 4]
array2 = [2, 3, 4, 1, 5]

testGene = ['A', 'B', 'C', 'D']
testGene2 = ['A', 'D', 'C', 'B']

# start = int(input("Enter the starting index: "))
# end = int(input("Enter the ending index: "))

# crossover(testGene, testGene2, 2, 3)
# mutation(testGene)
# mutation(testGene2)

# print(get_fitness(testGene))

# test
ag, af = TSP('A', 5001, points2)
animate_generation(ag, points2, af, False)
graph_generations(af)
