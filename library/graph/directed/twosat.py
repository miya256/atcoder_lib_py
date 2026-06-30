from library.graph.directed.scc_kosaraju import SCC


class TwoSAT:
    def __init__(self, n: int):
        self._n = n
        self._ans = [False] * n
        self._scc = SCC(2 * n)

    def add_clause(self, i: int, f: bool, j: int, g: bool) -> None:
        """
        (x_i is f) V (x_j is g) が真である必要があるという条件を追加
        x_iがf または x_jがg でないといけない

        例
        i か j のどちらか一方を選ばないといけない -> (i, True,  j, True)
        i と j を同時に選んではいけない          -> (i, False, j, False)
        i を選ばないといけない                  -> (i, True,  i, True)
        """
        assert 0 <= i < self._n
        assert 0 <= j < self._n
        self._scc.add_edge(2 * i + (0 if f else 1), 2 * j + (1 if g else 0))
        self._scc.add_edge(2 * j + (0 if g else 1), 2 * i + (1 if f else 0))

    def satisfiable(self) -> bool:
        """
        すべての条件を真にできるか
        奇数番の点はfalse側、偶数番目の点はtrue側
        2*i+1 -> 2*j に辺が張られてたら、iがfalseなら -> jはtrueでないといけないという意味

        なので、2*iと2*i+1が同じ連結成分に属している場合、
        iがfalseなら -> ... -> iがtrueなら -> ... -> iがfalseでないといけない となり、
        条件を満たせない
        """
        ids = [-1] * (2 * self._n)
        for i, scc in enumerate(self._scc.scc()):
            for v in scc:
                ids[v] = i

        for i in range(self._n):
            # 同じ連結成分なら条件を満たせない
            if ids[2 * i] == ids[2 * i + 1]:
                return False
            self._ans[i] = ids[2 * i] < ids[2 * i + 1]
        return True

    def answer(self) -> list[bool]:
        """
        答えの一つ
        辞書順とかにしたい場合は、vをFalseに固定して、条件を満たせるかってのを
        v=1~nについてやる。vをFalseに固定するのは、(v, False, v, False)を追加すればいい
        """
        return self._ans
