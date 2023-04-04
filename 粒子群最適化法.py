import random

def calculate(x1, x2, x3):  # 適応度
    return 2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3

class PSO:
    def __init__(self, c1=2, c2=2, w=2):
        self.w = w  # 慣性定数
        self.v0 = 0  # 探索個体の初速度
        self.v1 = 0
        self.v2 = 0
        self.x0 = random.randint(0, 15)  # 探索個体の位置
        self.x1 = random.randint(0, 15)
        self.x2 = random.randint(0, 15)
        self.y = calculate(self.x0, self.x1, self.x2)
        self.c1 = c1  # 学習係数
        self.c2 = c2
        self.p = [self.x0, self.x1, self.x2, self.y]  # 探索個体の最良位置

    def go(self, g):  # 探索関数
        # 計算速度
        self.v0 = self.w * self.v0 + self.c1 * random.random() * (g[0] - self.x0) + \
                  self.c2 * random.random() * (self.p[0] - self.x0)
        self.v1 = self.w * self.v1 + self.c1 * random.random() * (g[1] - self.x1) + \
                  self.c2 * random.random() * (self.p[1] - self.x1)
        self.v2 = self.w * self.v2 + self.c1 * random.random() * (g[2] - self.x2) + \
                  self.c2 * random.random() * (self.p[2] - self.x2)
        # 計算場所
        self.x0 = self.x0 + self.v0  # 限られた値の範囲
        if self.x0 > 15:
            self.x0 = 15
        elif self.x0 < 0:
            self.x0 = 0
        self.x1 = self.x1 + self.v1
        if self.x1 > 15:
            self.x1 = 15
        elif self.x1 < 0:
            self.x1 = 0
        self.x2 = self.x2 + self.v2
        if self.x2 > 15:
            self.x2 = 15
        elif self.x2 < 0:
            self.x2 = 0
        self.y = calculate(self.x0, self.x1, self.x2)  # 計算適応度

    def go_max(self, g):
        self.go(g)
        if self.y > self.p[3]:
            self.p = [self.x0, self.x1, self.x2, self.y]  # 自分の最適な位置を更新する

    def go_min(self, g):
        self.go(g)
        if self.y < self.p[3]:
            self.p = [self.x0, self.x1, self.x2, self.y]  # 自分の最適な位置を更新する

a = []
k = 0
best = []

for i in range(100):  # 初期粒子群を構造
    a.append(PSO())
    if a[k].y < a[i].y:
        k = i
best = a[k].p  # 最良解の値
for j in range(100):
    show = False
    for i in range(100):
        a[i].go_max(best)
        if a[i].y > best[3]:
            best = a[i].p
            show = True
    if show:
        print(best)
print("最大値:", best[3], )

a = []
k = 0
best = []

for i in range(100):
    a.append(PSO())
    if a[k].y > a[i].y:
        k = i
best = a[k].p
for j in range(100):
    show = False
    for i in range(100):
        a[i].go_min(best)
        if a[i].y < best[3]:
            best = a[i].p
            show = True
    if show:
        print(best)
print("最小値:", best[3], )
