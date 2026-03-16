# Contributing

## Development Rules

- 小さな変更でない限り、ブランチは切る
- コミットは小さく
- formatter をかける
- CI が成功していることを確認する
- mainブランチへのマージは必ず Pull Request 経由

## Branch naming
```
- feat/<機能名>
- fix/<不具合名>
- refactor/<内容>
- docs/<対象>-<内容>
- test/<内容>
- chore/<内容>
```

## Commit messages

Conventional Commits

```
<prefix>: <メッセージ>
```

| prefix   | 意味                 |
| -------- | ------------------ |
| feat     | 機能追加               |
| fix      | バグ修正               |
| refactor | リファクタリング           |
| style    | CSSや見た目の変更         |
| docs     | ドキュメント変更（READMEとか） |
| test     | 検証       |
| chore    | 細かい修正              |


## Coding Style

### Rules

- 目的のファイルを探しやすいファイル構成にする
- すべての関数・メソッドの引数・戻り値には型ヒントをつける
- docstring を書く 
- private変数には `_` をつける
- `@property` を適切に使う
- `inf` は小文字。値は2^61。グローバルに定義する

### Method Order

1. 特殊メソッド
2. publicメソッド
3. privateメソッド（ただし_build()や関連性の強いものは例外的）
4. @property
5. @staticmethod