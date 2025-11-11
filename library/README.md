# アルゴリズムやデータ構造

## 背景
インターンの経験により、コードを整理したくなった。  
ファイルは1つずつ加えていく。コピーして書き直したら、元のファイルを消してよい。

## 要件
- 目的のファイルを探しやすいファイル構成
- すべての関数・メソッドの引数・戻り値には型ヒントをつける（Anyや関数型などはobjectがあるが、SegTreeなどはMonoidクラスとかを検討している）
- 上にpublicメソッドをまとめて、下のprivateメソッドを呼ぶだけにするような書き方はやめる
- その代わり、クラスの一番上にdocstringで、publicなメンバとメソッドをかく  
例
```python
class Class:
    """
    クラスの説明

    Attributes:
        n (int): サイズ
        op(x, y) (Callable[[Any, Any], Any]): 二項演算
        e (Any): 単位元

    Methods:
        prod(l: int, r: int) -> str: [l, r)の演算結果
    """

    def __init__(self):
```
- メソッドや関数にもdocstringをかく
- publicとprivateは意識する
- @propertyとかも使っていく

メソッドの順番
1. 特殊メソッド
2. publicメソッド
3. privateメソッド
（ただし_build()は例外的に__init__の下にかくとする）
（また、関連性の強いものはpublicのとこに書いてもよい）
4. @property
5. @staticmethod