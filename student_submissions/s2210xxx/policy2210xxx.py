from policy import Policy
from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle, random, choice, choices
import time  # Ensure 'time' is imported
class GeneticPolicy(Policy):
  def __init__(self, populationSize = 300, penalty = 2, mutationRate = 0.1):
    # Student code here
    """
    Hàm khởi tạo lớp GeneticPolicy để triển khai thuật toán di truyền.

    Tham số:
    - populationSize (int): Số lượng cá thể (chromosome) trong quần thể.
    - penalty (float): Hệ số phạt áp dụng cho nhu cầu chưa được đáp ứng.
    - mutationRate (float): Xác suất xảy ra đột biến trong mỗi bước tiến hóa.
    """
    self.MAX_ITERATIONS = 2000 # Số vòng lặp tối đa cho thuật toán
    self.POPULATION_SIZE = populationSize
    self.stockLength = None  # Chiều dài của kho nguyên liệu
    self.stockWidth = None # Chiều rộng của kho nguyên liệu
    self.lengthArr = [] # Mảng chứa chiều dài của các mẫu
    self.widthArr = [] # Mảng chứa chiều rộng của các mẫu
    self.demandArr = [] # Mảng chứa số lượng yêu cầu các mẫu
    self.N = None # Số lượng mẫu
    self.penalty = penalty
    self.mutationRate = mutationRate

  # def generate_efficient_patterns(self):
  #   """
  #   Sinh ra các mẫu (pattern) khả thi dựa trên kích thước kho và nhu cầu.

  #   Kết quả:
  #   - Trả về danh sách các mẫu khả thi.
  #   """
  #   result = []
  #   # availableArr sẽ chứa số lượng mẫu đầu tiên có thể cắt từ kho, với chiềudài và chiều rộng
  #   availableArr = [min(floor(self.stockLength / self.lengthArr[0]),floor(self.stockWidth / self.widthArr[0]), self.demandArr[0])]

  #   # Sinh các mẫu khả thi cho từng loại mẫu.
  #   for n in range(1, self.N):
  #     # Tổng diện tích các mẫu trước đó đã sử dụng
  #     s = sum([availableArr[j] * self.lengthArr[j] for j in range(n)])
  #     availableArr.append(min(floor((self.stockLength - s) / self.lengthArr[n]), floor((self.stockWidth - s) / self.widthArr[n]), self.demandArr[n]))

  #     # Tiếp tục sinh các mẫu mới cho đến khi không thể thêm được nữa
  #     while True:
  #       result.append(availableArr) # Lưu mẫu hiện tại vào danh sách kết quả

  #       for j in range(self.N - 2, -1, -1):  # Tìm vị trí đầu tiên có thể giảm số lượng
  #         if availableArr[j] > 0:
  #           k = j
  #           break
  #         else:
  #           return result # Kết thúc nếu không thể giảm thêm

  #       # Tạo mẫu mới bằng cách giảm số lượng ở vị trí k
  #       availableArrNew = []
  #       for j in range(k):
  #         availableArrNew.append(availableArr[j])
  #       availableArrNew.append(availableArr[k] - 1)
  #       # Tính lại số lượng khả thi cho các mẫu phía sau
  #       for n in range(k + 1, self.N):
  #         s = sum([availableArrNew[j] * self.lengthArr[j] for j in range(n)])
  #         availableArrNew.append(min(floor((self.stockLength - s) / self.lengthArr[n]), floor((self.stockWidth - s) / self.widthArr[n]), self.demandArr[n]))
  #       availableArr = deepcopy(availableArrNew) # Cập nhật mẫu mới
  
  def generate_efficient_patterns(self):
    """
    Generate feasible cutting patterns based on stock dimensions and demands.
    
    Returns:
    - List of feasible patterns, where each pattern is a list of quantities for each item.
    """
    result = []
    availableArr = [min(
        floor(self.stockLength / self.lengthArr[0]) * floor(self.stockWidth / self.widthArr[0]),
        self.demandArr[0]
    )]

    for n in range(1, self.N):
        used_length = sum(availableArr[j] * self.lengthArr[j] for j in range(n))
        used_width = sum(availableArr[j] * self.widthArr[j] for j in range(n))
        availableArr.append(min(
            floor((self.stockLength - used_length) / self.lengthArr[n]) * 
            floor((self.stockWidth - used_width) / self.widthArr[n]),
            self.demandArr[n]
        ))

    while True:
        result.append(availableArr.copy())
        for j in range(len(availableArr) - 1, -1, -1):
            if availableArr[j] > 0:
                availableArr[j] -= 1
                for k in range(j + 1, self.N):
                    used_length = sum(availableArr[m] * self.lengthArr[m] for m in range(k))
                    used_width = sum(availableArr[m] * self.widthArr[m] for m in range(k))
                    availableArr[k] = min(
                        floor((self.stockLength - used_length) / self.lengthArr[k]) * 
                        floor((self.stockWidth - used_width) / self.widthArr[k]),
                        self.demandArr[k]
                    )
                break
        else:
            break
    return result
  
  # def generate_efficient_patterns(self):
        # result = []
        # A_arr = [min(floor(self.stock_length / self.l_arr[0]), floor(self.stock_width / self.w_arr[0]), self.d_arr[0])]
        # for n in range(1, self.N):
        #     s_length = sum([A_arr[j] * self.l_arr[j] for j in range(n)])
        #     s_width = sum([A_arr[j] * self.w_arr[j] for j in range(n)])
        #     A_arr.append(min(floor((self.stock_length - s_length) / self.l_arr[n]), 
        #                      floor((self.stock_width - s_width) / self.w_arr[n]), 
        #                      self.d_arr[n]))

        # while True:
        #     result.append(A_arr)
        #     for j in range(self.N - 2, -1, -1):
        #         if A_arr[j] > 0:
        #             k = j
        #             break
        #     else:
        #         return result

        #     A_arr_new = []
        #     for j in range(k):
        #         A_arr_new.append(A_arr[j])
        #     A_arr_new.append(A_arr[k] - 1)
        #     for n in range(k + 1, self.N):
        #         s_length = sum([A_arr_new[j] * self.l_arr[j] for j in range(n)])
        #         s_width = sum([A_arr_new[j] * self.w_arr[j] for j in range(n)])
        #         A_arr_new.append(min(floor((self.stock_length - s_length) / self.l_arr[n]), 
        #                              floor((self.stock_width - s_width) / self.w_arr[n]), 
        #                              self.d_arr[n]))
        #     A_arr = deepcopy(A_arr_new)


  def calculate_max_pattern_repetition(self, patternsArr):
      """
        Tính số lần tối đa mỗi mẫu (pattern) có thể được sử dụng.

        Tham số:
        - patternsArr: Danh sách các mẫu.

        Kết quả:
        - Trả về danh sách số lần tối đa mỗi mẫu có thể lặp lại.
        """
      result = [] # Danh sách lưu trữ số lần lặp tối đa cho từng mẫu
      for pattern in patternsArr:
            maxRep = 0
            for i in range(len(pattern)):
                if pattern[i] > 0:
                    # Tính số lần cần lặp để đáp ứng nhu cầu
                    neededRep = ceil(self.demandArr[i] / pattern[i])
                    if neededRep > maxRep:
                        maxRep = neededRep
            result.append(maxRep)
      return result


  def initialize_population(self, maxRepeatArr):
    """
    Khởi tạo quần thể ban đầu cho thuật toán di truyền.

    Tham số:
    - maxRepeatArr: Danh sách số lần tối đa mỗi mẫu có thể lặp lại.

    Kết quả:
    - Trả về danh sách quần thể ban đầu (mỗi cá thể là một chromosome).
    """
    initPopulation = [] # Danh sách lưu trữ quần thể
    pairs = list(zip(range(len(maxRepeatArr)), maxRepeatArr)) # Kết hợp mvà số lần lặp tối đa
    for i in range(self.POPULATION_SIZE):
        chromosome = [] # Mỗi cá thể là một chuỗi (chromosome)
        shuffle(pairs) # Xáo trộn thứ tự các mẫu
        for j in range(self.N):
            chromosome.append(pairs[j][0]) # Thêm chỉ số mẫu
            chromosome.append(randint(1, pairs[j][1])) # Thêm số lần lặp ngẫu nhiên
        initPopulation.append(chromosome)
    return initPopulation

  #Part 2(Ân)
  #Hàm fitness dánh giá mỗi cá thể
  # def evaluate_fitness(self, chromosome, patterns_arr):
  #   """
  #   Đánh giá độ phù hợp (fitness) của một cá thể (chromosome) dựa trên các mẫu cắt và yêu cầu.

  #   Tham số:
  #   - chromosome: Danh sách đại diện cho một cá thể (giải pháp), gồm các cặp (pattern_index, repetition).
  #   - patterns_arr: Danh sách các mẫu cắt khả thi, mỗi mẫu là danh sách số lượng từng loại nguyên liệu.

  #   Kết quả:
  #   - Giá trị fitness của cá thể, là tỷ lệ giữa diện tích yêu cầu và chi phí thực hiện (bao gồm phạt nếu không đáp ứng đủ yêu cầu).
  #   """
  #   P = self.penalty  # Hệ số phạt cho nhu cầu không được đáp ứng
  #   unsupplied_sum = 0  # Tổng diện tích nguyên liệu không được đáp ứng
  #   provided = [0] * self.N  # Danh sách lưu số lượng nguyên liệu đã cung cấp cho từng loại

  #   # Bước 1: Tính tổng số lượng nguyên liệu được cung cấp
  #   for i in range(0, len(chromosome), 2):  # Duyệt qua từng cặp (pattern_index, repetition)
  #       pattern_index = chromosome[i]  # Lấy chỉ số mẫu (pattern index)
  #       repetition = chromosome[i + 1]  # Lấy số lần lặp lại mẫu đó (repetition)
  #       pattern = patterns_arr[pattern_index]  # Lấy mẫu dựa trên chỉ số mẫu
  #       for j in range(len(pattern)):  # Duyệt qua từng loại nguyên liệu trong mẫu
  #           provided[j] += pattern[j] * repetition  # Cộng dồn số lượng nguyên liệu được cung cấp

  #  # Bước 2: Tính tổng diện tích nguyên liệu không được đáp ứng
  #   for i in range(self.N):  # Duyệt qua từng loại nguyên liệu
  #       unsupplied = self.demandArr[i] - provided[i]  # Tính số lượng chưa được cung cấp
  #       if unsupplied > 0:  # Nếu còn nguyên liệu chưa được đáp ứng
  #          unsupplied_sum += unsupplied * self.lengthArr[i] * self.widthArr[i]  # Tính diện tích chưa đáp ứng và cộng vào tổng

  #   # Bước 3: Tính tổng chiều dài vật liệu đã sử dụng từ kho
  #   used_length = self.stockLength * sum(
  #       chromosome[i + 1] for i in range(0, len(chromosome), 2)
  #   )  # Nhân tổng số lần lặp với chiều dài của kho vật liệu

  #   # Bước 4: Tính tổng diện tích yêu cầu
  #   total_demand_area = sum(self.lengthArr[i] * self.demandArr[i] for i in range(self.N))  # Diện tích cần cung cấp theo yêu cầu

  #   # Bước 5: Tính giá trị fitness
  #   fitness = total_demand_area / (used_length + P * unsupplied_sum)  # Tỷ lệ giữa diện tích yêu cầu và chi phí sử dụng nguyên liệu

  #   return fitness  # Trả về giá trị fitness
  
  def evaluate_fitness(self, chromosome, patterns_arr):
        P = self.penalty
        unsupplied_sum = 0
        l_provided = [0] * self.N
        w_provided = [0] * self.N
        for i in range(0, len(chromosome), 2):
            pattern = patterns_arr[chromosome[i]]
            for j in range(len(pattern)):
                l_provided[j] += pattern[j] * chromosome[i + 1]
                w_provided[j] += pattern[j] * chromosome[i + 1]
        for i in range(self.N):
            num_unsupplied_l = self.d_arr[i] - l_provided[i]
            num_unsupplied_w = self.d_arr[i] - w_provided[i]
            if num_unsupplied_l > 0 or num_unsupplied_w > 0:
                unsupplied_sum += (num_unsupplied_l * self.l_arr[i] + num_unsupplied_w * self.w_arr[i])
        x_sum = self.stock_length * sum(chromosome[i] for i in range(1, len(chromosome), 2))
        S = sum([self.l_arr[i] * self.w_arr[i] * self.d_arr[i] for i in range(self.N)])
        return S / (x_sum + P * unsupplied_sum)

  def run(self, population, patterns_arr, max_repeat_arr, problem_path, queue=None):
    start_time = time.time()
    best_results = []
    num_iters_same_result = 0
    last_result = float('inf')
    iter_count = self.MAX_ITERATIONS

    for count in range(self.MAX_ITERATIONS):
        # Stop if no improvement after 100 iterations
        if num_iters_same_result >= 100:
            iter_count = count
            break

        # Evaluate fitness for the population
        fitness_pairs = [(ch, self.evaluate_fitness(ch, patterns_arr)) for ch in population]
        fitness_pairs.sort(key=lambda x: x[1], reverse=True)

        # Preserve top 3 (elitism)
        next_generation = [fitness_pairs[0][0], fitness_pairs[1][0], fitness_pairs[2][0]]
        best_result_for_iter = fitness_pairs[0][1]
        best_results.append(best_result_for_iter)

        # Stop if perfect solution is found
        if best_result_for_iter == 1:
            iter_count = count
            break

        # Check convergence
        if abs(best_result_for_iter - last_result) < 1e-5:
            num_iters_same_result += 1
        else:
            num_iters_same_result = 0
        last_result = best_result_for_iter

        # Generate stocks for the current best solution
        stocks = []
        chosen_pattern = fitness_pairs[0][0]
        for i in range(0, len(chosen_pattern), 2):
            compact_pattern = patterns_arr[chosen_pattern[i]]
            actual_pattern = [
                self.lengthArr[j] for j in range(self.N) for _ in range(compact_pattern[j])
            ]
            repeat = chosen_pattern[i + 1]
            for _ in range(repeat):
                stocks.append(actual_pattern)

        # Communicate results through the queue (if applicable)
        if queue is not None:
            queue.put((self.stockLength, self.lengthArr, self.demandArr, stocks))

        # Create new generation
        for i in range(3, len(fitness_pairs), 2):
            parent1 = self.select_parents2(fitness_pairs)
            parent2 = self.select_parents2(fitness_pairs)

            # Generate offspring using crossover and mutation
            child1 = self.mutate(self.crossover(parent1, parent2), self.mutationRate, max_repeat_arr)
            child2 = self.mutate2(self.crossover(parent2, parent1), self.mutationRate, max_repeat_arr)

            # Add offspring to the next generation
            next_generation.append(child1)
            next_generation.append(child2)

        population = deepcopy(next_generation)

    # Final evaluation
    fitness_pairs = [(ch, self.evaluate_fitness(ch, patterns_arr)) for ch in population]
    fitness_pairs.sort(key=lambda x: x[1], reverse=True)
    end_time = time.time()

  #------------------------------------------------------------------------------------------------------------------------
  #Part 3(Duy Anh)
  #------------------------------------------------------------------------------------------------------------------------
  #CHON LOC CHA ME
  @staticmethod
  def select_parents1(population, fitness_scores):
    """
    Lựa chọn cha mẹ bằng phương pháp Roulette Wheel dựa trên điểm fitness.

    Tham số:
    - population: Quần thể hiện tại.
    - fitness_scores: Điểm fitness của các cá thể trong quần thể.

    Kết quả:
    - Trả về một cá thể được chọn làm cha/mẹ.
    """
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]

    # Tính xác suất tích lũy
    cumulative_probabilities = []
    cumulative_sum = 0
    for prob in probabilities:
        cumulative_sum += prob
        cumulative_probabilities.append(cumulative_sum)

    # Chọn cá thể dựa trên giá trị ngẫu nhiên
    random_value = random()
    for i, cumulative in enumerate(cumulative_probabilities):
        if random_value <= cumulative:
            return population[i]
  
  # @staticmethod
  # def select_parents(fitness_pairs):
  #       n = len(fitness_pairs)
  #       max_val1 = max_val2 = float('-inf')
  #       index1 = index2 = None
  #       for i in range(n):
  #           score = (n - i) * random()
  #           if score > max_val1:
  #               max_val1, max_val2 = score, max_val1
  #               index1, index2 = i, index1
  #           elif score > max_val2:
  #               max_val2 = score
  #               index2 = i
  #       return fitness_pairs[index1][0], fitness_pairs[index2][0]

  @staticmethod
  def select_parents2(population, fitness_scores, tournament_size = 5):
    """
    Lựa chọn cha mẹ bằng phương pháp Tournament.

    Tham số:
    - population: Quần thể hiện tại.
    - fitness_scores: Điểm fitness của các cá thể trong quần thể.
    - tournament_size: Kích thước nhóm trong tournament.

    Kết quả:
    - Trả về một cá thể được chọn làm cha/mẹ.
    """
    indices = choices(range(len(population)), k=tournament_size)
    tournament = [population[i] for i in indices]
    tournament_scores = [fitness_scores[i] for i in indices]

    # Tìm cá thể tốt nhất trong nhóm tournament
    best_index = tournament_scores.index(max(tournament_scores))
    return tournament[best_index]
  
  # @staticmethod
  # def select_parents2(fitness_pairs):
  #       n = len(fitness_pairs)
  #       probabilities_sum = n * (n + 1) / 2
  #       probabilities = [i / probabilities_sum for i in range(n + 1, 1, -1)]
  #       return choices([pair[0] for pair in fitness_pairs], weights=probabilities, k=2)

  @staticmethod
  def crossover(parent1, parent2):
    """
    Lai ghép hai cá thể để tạo ra một cá thể con mới.

    Tham số:
    - parent1: Cá thể cha.
    - parent2: Cá thể mẹ.

    Kết quả:
    - Trả về một cá thể con.
    """
    child = []
    for i in range(len(parent1)):
        # Chọn gen từ cha hoặc mẹ
        if random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child
  
  @staticmethod
#   def mutate(chromosome, mutation_rate, max_repeat_arr): 
#     """
#     Thực hiện đột biến ngẫu nhiên trên một cá thể.

#     Tham số:
#     - chromosome: Cá thể cần đột biến.
#     - mutation_rate: Xác suất đột biến.
#     - max_repeat_arr: Giới hạn số lần lặp tối đa của từng mẫu.

#     Kết quả:
#     - Trả về cá thể sau khi đột biến.
#     """
#     mutated_chromosome = chromosome[:]
#     for i in range(0, len(chromosome), 2):  # Xét từng cặp (pattern_index, repetition)
#         if random() < mutation_rate and i + 1 < len(chromosome) :
#             # Thay đổi số lần lặp trong giới hạn
#             pattern_index = mutated_chromosome[i]
#             mutated_chromosome[i+1] = randint(1, max_repeat_arr[pattern_index])
#     return mutated_chromosome
  def mutate(chromosome, mutation_rate, max_repeat_arr):
    """
    Perform random mutation on a chromosome.

    Parameters:
    - chromosome (list): The chromosome to mutate.
    - mutation_rate (float): Probability of mutation for each gene.
    - max_repeat_arr (list): Maximum repetition limits for each pattern.

    Returns:
    - list: The mutated chromosome.
    """
    mutated_chromosome = chromosome[:]
    for i in range(0, len(chromosome), 2):  # Iterate over pattern indices
        if random() < mutation_rate:
            # Mutate the repetition count within limits
            pattern_index = mutated_chromosome[i]
            mutated_chromosome[i + 1] = randint(1, max_repeat_arr[pattern_index])
    return mutated_chromosome


  def mutate2(chromosome, mutation_rate, max_repeat_arr, patterns, other_chromosome=None):
    """
    Thực hiện đột biến ngẫu nhiên nâng cao, bao gồm thay đổi và kết hợp với cá thể khác.

    Tham số:
    - chromosome: Cá thể cần đột biến.
    - mutation_rate: Xác suất đột biến.
    - max_repeat_arr: Giới hạn số lần lặp tối đa của từng mẫu.
    - patterns: Danh sách các mẫu khả dụng.
    - other_chromosome: Một cá thể khác để kết hợp (nếu có).

    Kết quả:
    - Trả về cá thể sau khi đột biến.
    """
    mutated_chromosome = chromosome[:]
    for i in range(0, len(mutated_chromosome), 2):  # Xét từng cặp (pattern_index, repetition)
        if random() < mutation_rate:
            # Thay đổi số lần lặp hoặc kết hợp với cá thể khác (nếu được cung cấp)
            if other_chromosome and random() < 0.5:
                mutated_chromosome[i] = other_chromosome[i]
                mutated_chromosome[i + 1] = other_chromosome[i + 1]
            else:
                new_pattern_index = randint(0, len(patterns) - 1)
                mutated_chromosome[i] = new_pattern_index
                mutated_chromosome[i + 1] = randint(1, max_repeat_arr[new_pattern_index])
    return mutated_chromosome

#   def mutate2(chromosome, mutation_rate, max_repeat_arr, patterns, other_chromosome=None):
#     """
#     Perform advanced mutation, including optional crossover with another chromosome.

#     Parameters:
#     - chromosome (list): The chromosome to mutate.
#     - mutation_rate (float): Probability of mutation for each gene.
#     - max_repeat_arr (list): Maximum repetition limits for each pattern.
#     - patterns (list): Available patterns for mutation.
#     - other_chromosome (list, optional): Another chromosome for crossover (default: None).

#     Returns:
#     - list: The mutated chromosome.
#     """
#     mutated_chromosome = chromosome[:]
#     for i in range(0, len(mutated_chromosome), 2):  # Iterate over pattern indices
#         if random() < mutation_rate:
#             if other_chromosome and random() < 0.5:
#                 # Crossover: Inherit gene from the other chromosome
#                 mutated_chromosome[i] = other_chromosome[i]
#                 mutated_chromosome[i + 1] = other_chromosome[i + 1]
#             else:
#                 # Mutate pattern or repetition count
#                 new_pattern_index = randint(0, len(patterns) - 1)
#                 mutated_chromosome[i] = new_pattern_index
#                 mutated_chromosome[i + 1] = randint(1, max_repeat_arr[new_pattern_index])
#     return mutated_chromosome

  
  def select_new_population(self,population, fitness_scores, patterns_arr, mutation_rate, max_repeat_arr, selection_type="tournament"):
    """
    Tạo quần thể mới bằng cách chọn lọc, lai ghép và đột biến.

    Tham số:
    - population: Quần thể hiện tại.
    - fitness_scores: Điểm fitness của các cá thể trong quần thể.
    - patterns_arr: Danh sách các mẫu khả thi.
    - mutation_rate: Xác suất đột biến.
    - max_repeat_arr: Số lần lặp tối đa cho từng mẫu.
    - selection_type: Phương pháp chọn lọc ('tournament' hoặc 'roulette').

    Kết quả:
    - Trả về quần thể mới.
    """
    new_population = []
    for _ in range(len(population) // 2):  # Số cặp cha mẹ
        # Chọn cha mẹ
        if selection_type == "tournament":
            parent1 = self.select_parents1(population, fitness_scores)
            parent2 = self.select_parents1(population, fitness_scores)
        elif selection_type == "roulette":
            parent1 = self.select_parents2(population, fitness_scores)
            parent2 = self.select_parents2(population, fitness_scores)

        # Lai ghép
        child1 = self.crossover(parent1, parent2)
        child2 = self.crossover(parent2, parent1)

        # Đột biến
        child1 = self.mutate(child1, mutation_rate, max_repeat_arr)
        child2 = self.mutate(child2, mutation_rate, max_repeat_arr)

        # Thêm cá thể con vào quần thể mới
        new_population.extend([child1, child2])

    return new_population


  # def get_action(self, observation, info):
    # """
    # Genetic algorithm to decide the best action.
    # """
    # list_prods = observation["products"]
    # stocks = observation["stocks"]

    # # Default action
    # prod_size = [0, 0]
    # stock_idx = -1
    # pos_x, pos_y = 0, 0

    # # Iterate over products
    # for prod in list_prods:
    #     if prod["quantity"] > 0:
    #         prod_size = prod["size"]

    #         # Apply a genetic-like heuristic to find placement
    #         best_fitness = float("inf")
    #         best_action = None

    #         for i, stock in enumerate(stocks):
    #             stock_w, stock_h = self._get_stock_size_(stock)
    #             prod_w, prod_h = prod_size

    #             if stock_w < prod_w or stock_h < prod_h:
    #                 continue

    #             # Check all possible positions
    #             for x in range(stock_w - prod_w + 1):
    #                 for y in range(stock_h - prod_h + 1):
    #                     if self._can_place_(stock, (x, y), prod_size):
    #                         # Fitness function: Minimize unused area
    #                         unused_area = stock_w * stock_h - prod_w * prod_h
    #                         # fitness = unused_area + abs(stock_w - prod_w) + abs(stock_h - prod_h)
    #                         if unused_area < best_fitness:
    #                             best_fitness = unused_area
    #                             best_action = {"stock_idx": i, "size": prod_size, "position": (x, y)}

    #         if best_action:
    #             stock_idx = best_action["stock_idx"]
    #             pos_x, pos_y = best_action["position"]
    #             break

    # return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
  
  # def get_action(self, observation, info):
  #       list_prods = observation["products"]

  #       prod_size = [0, 0]
  #       stock_idx = -1
  #       pos_x, pos_y = 0, 0

  #       # Pick a product that has quality > 0
  #       for prod in list_prods:
  #           if prod["quantity"] > 0:
  #               prod_size = prod["size"]

  #               # Loop through all stocks
  #               for i, stock in enumerate(observation["stocks"]):
  #                   stock_w, stock_h = self._get_stock_size_(stock)
  #                   prod_w, prod_h = prod_size

  #                   if stock_w < prod_w or stock_h < prod_h:
  #                       continue

  #                   pos_x, pos_y = None, None
  #                   for x in range(stock_w - prod_w + 1):
  #                       for y in range(stock_h - prod_h + 1):
  #                           if self._can_place_(stock, (x, y), prod_size):
  #                               pos_x, pos_y = x, y
  #                               break
  #                       if pos_x is not None and pos_y is not None:
  #                           break

  #                   if pos_x is not None and pos_y is not None:
  #                       stock_idx = i
  #                       break

  #               if pos_x is not None and pos_y is not None:
  #                   break

  #       return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
  
  def get_action(self, observation, info):
    list_prods = observation["products"]
    prod_size = [0, 0]
    stock_idx = -1
    pos_x, pos_y = 0, 0

    for prod in list_prods:
        if prod["quantity"] > 0:
            prod_size = prod["size"]
            for i, stock in enumerate(observation["stocks"]):
                stock_w, stock_h = self._get_stock_size_(stock)
                if stock_w >= prod_size[0] and stock_h >= prod_size[1]:
                    for x in range(stock_w - prod_size[0] + 1):
                        for y in range(stock_h - prod_size[1] + 1):
                            if self._can_place_(stock, (x, y), prod_size):
                                stock_idx = i
                                pos_x, pos_y = x, y
                                break
                        if stock_idx != -1:
                            break
            if stock_idx != -1:
                break

    return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
    


  # Student code here
  # You can add more functions if needed


