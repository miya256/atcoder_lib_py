# アイデア

## Library Checker

yosupo さんのやつを CI に組み込む  
[online-judge-tools/verification-helper](https://online-judge-tools.github.io/verification-helper/README.ja.html)
というのがあるらしい

- 拡張子は.test.py とする

union_find.test.py
```python
# verification-helper: PROBLEM https://judge.yosupo.jp/problem/unionfind

from ..library.union_find import UnionFind

n,q = map(int,input().split())
...
```

## `error.md`

- index系のassert文などの書き方がバラバラなので、ルールを統一したい
- そのルールをかいておくmdをdocsにいれておく
- READMEに、docsの中のファイルへのリンクはる

## assert文

例えば、index系のassert文は、
```
assert -n <= i < n, f"i={i}, n={n}"
```
みたいな型に統一して、CIでチェック

どこにassertを書くのかとか、LLMを試してみてもいいのかもしれない