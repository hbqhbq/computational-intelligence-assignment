

import numpy as np

N = 15 # 遺伝子長
Pc = 0.30 # 交叉確率
Pm = 0.05 # 突然変異確率
N_GENERTATIONS = 100 # 世代数
POP_SIZE = 200 # 群の行列
X1_BOUND = [0, 15] # x1取値範囲
X2_BOUND = [0, 15] # x2取値範囲
X3_BOUND = [0, 15] # x3取値範囲


def F(x1, x2, x3):
    return 2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3;


def translateDNA(pop): # popは群行列を表し、行はバイナリ符号化で表されるDNA
                       # を表し、行列の行数は群の数である
    x1_pop = pop[:, :N]
    x2_pop = pop[:, N:-N]
    x3_pop = pop[:, -N:]
    x1 = x1_pop.dot(2 ** np.arange(N)[::-1]) / float(2 ** N - 1) * \
         (X1_BOUND[1] - X1_BOUND[0]) + X1_BOUND[0]
    x2 = x2_pop.dot(2 ** np.arange(N)[::-1]) / float(2 ** N - 1) * \
         (X2_BOUND[1] - X2_BOUND[0]) + X2_BOUND[0]
    x3 = x3_pop.dot(2 ** np.arange(N)[::-1]) / float(2 ** N - 1) * \
         (X3_BOUND[1] - X3_BOUND[0]) + X3_BOUND[0]
    return x1, x2, x3


def get_fitness(pop):
    x1, x2, x3 = translateDNA(pop)
    pred = F(x1, x2, x3)
    return -(pred - np.max(pred)) + 1e-3# 最小の適応度を減算するのは、適応度に負が生じるのを防ぐ
                               # ためfitnessの範囲は[0,np.max(pred)-np.min(pred)


def crossover(pop, rate=Pc):
    new_pop = []
    for father in pop:# 群れの中のすべての個体を巡り、その個体を父親とする
        child = father# 子供は父の遺伝子をもらう
        if np.random.rand() < rate:# 一定の確率で交差が発生する
            mother = pop[np.random.randint(POP_SIZE)]# もう一つの个体を母
                                                     # としてえらぶ
            cross_points = np.random.randint(low=0, high=N * 3)# ランダムに交差点
                                                               # を生成する
            child[cross_points:] = mother[cross_points:]# 子供は交差点の後ろにある
                                                        # 母の遺伝子をもらう
        mutation(child)# 子供ごとに一定の確率で変異が起こる。
        new_pop.append(child)
    return new_pop


def mutation(child, rate=Pm):
    if np.random.rand() < rate:# rateの確率で変異する
        mutate_point = np.random.randint(0, N * 3)# ランダムに実数を生成し、遺伝子を
                                                  # 変異させる位置を表す
        child[mutate_point] = child[mutate_point] ^ 1# 変異点のバイナリを反転しする


def select(pop, fitness):# 群を生成する
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE,
                           replace=True, p=(fitness) / (fitness.sum()))
    return pop[idx]


def print_pre(pop):
    fitness = get_fitness(pop)
    min_fitness = np.argmin(fitness)
    fit=round(fitness[min_fitness], 2)
    x1, x2, x3 = translateDNA(pop)
    y=F(x1[min_fitness], x2[min_fitness], x3[min_fitness])
    y1=round(y,2)
    print("2*x1*x1-3*x2*x2-4*x1+5*x2+x3=",y1)



if __name__ == '__main__':
    pop = np.random.randint(2, size=(POP_SIZE, N * 3))# 群を生成する
    print(pop)
    for i in range(N_GENERTATIONS):# 群は反復して進化するN_GENERATIONS代
        x1, x2, x3 = translateDNA(pop)
        pop = np.array(crossover(pop))# 交差変異を通して後代を生む
        fitness = get_fitness(pop)# 群の中の各個体を評価する
        pop = select(pop, fitness)# 新しいグループを作成する場合にする
        print("{:=^50}\n{}番目".format("", i + 1))
        print_pre(pop)

def get_fitness(pop):
    x, y = translateDNA(pop)
    pred = F(x, y)
    return -(pred - np.max(pred))


