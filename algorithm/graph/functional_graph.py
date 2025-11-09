#SCC必要
class FunctionalGraph(SCC):
    def __init__(self, n):
        super().__init__(n)
    
    def make_forest(self):
        #for size, *edges in forest: のようにできる
        forest = [] #forest[i]は、木iの[頂点数, 辺0, 辺1, ...]
        belong = [None] * self.n #vが(何番目の木, 何番目の頂点)か
        for scc in self.scc()[::-1]:
            if len(scc) > 1 or not self.graph[scc[0]]:
                for v in scc:
                    belong[v] = (len(forest), 0)
                forest.append([1])
            else:
                v = scc[0]
                nv = self.graph[v][0]
                tree_id, _ = belong[nv]
                belong[v] = (tree_id, forest[tree_id][0])

                forest[tree_id][0] += 1
                forest[tree_id].append((belong[v][1], belong[nv][1]))
        return forest, belong