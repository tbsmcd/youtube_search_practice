# youtube_search_practice
## 基本方針
- Google 製 client は使いません
- OAuth は不要なので API Key を使用します
- コマンドとしてパイプラインでつなぎやすい設計にします
    - 標準出力・標準エラー出力を使い分けます
    - API Key が存在しないときに対話的に入力を求めるのではなく、標準エラー出力を返します
    - API Key の保存にはサブコマンドを用意します
    - json 等での出力よりも、まずはテキストを優先しました

## 動作環境
付属の docker-compose で動作を確認しています。

起動
```bash
$ docker-compose up -d --build
```

コンテナに入る
```bash
$ docker-compose exec youtube_py bash
```

コマンドの実行
```bash
# python scripts/main.py search "エレファント"
https://www.youtube.com/watch?v=0melyLHqP-s 今宵の月のように/エレファントカシマシ
https://www.youtube.com/watch?v=tIe-kXTmj3E 椎名林檎と宮本浩次－獣ゆく細道
https://www.youtube.com/watch?v=0WZu7L7Hjds 悲しみの果て ≡ エレファントカシマシ
https://www.youtube.com/watch?v=cWHU2-WnZqc エレファントカシマシ - 「俺たちの明日」
https://www.youtube.com/watch?v=2XZvRqpqsnw エレファントカシマシ「ズレてる方がいい」
https://www.youtube.com/watch?v=AVPbDnPiYac 翳りゆく部屋　エレファントカシマシcover
https://www.youtube.com/watch?v=jHmpt5et9bk エレファントカシマシ - 笑顔の未来へ
https://www.youtube.com/watch?v=fa-MBPOeQbM エレファントカシマシ - 「桜の花、舞い上がる道を」
https://www.youtube.com/watch?v=3AjX6dkMWyE エレファントカシマシ「RAINBOW」
https://www.youtube.com/watch?v=Ms7Ec594Xz4 エレファントカシマシ / 俺たちの明日

```

## 使い方

まずは YouTube API Key を取得して、
```bash
# python scripts/main.py key [API_KEY]
```
を実行して Key を保存します。  
API Key が保存されていなかったり誤った Key が保存されている場合に検索を実行してもエラーメッセージで案内します。  
  
検索は
```bash
# python scripts/main.py search "音楽"
```
のように行います。デフォルトの検索件数は10件ですが、オプションで件数を指定することもできます。（1 <= num <= 50）
```bash
# python scripts/main.py search "音楽" --num 20
```

詳しくは help を参照して下さい。
```bash
# python scripts/main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  key     API Key を保存するサブコマンド。引数に API Key を入力して下さい。
  search  検索する場合のサブコマンド。引数にスペースが含まれる場合はダブルクォーテーションで囲って下さい
  
# python scripts/main.py search --help
Usage: main.py search [OPTIONS] KEYWORD

  検索する場合のサブコマンド。引数にスペースが含まれる場合はダブルクォーテーションで囲って下さい

Options:
  --num INTEGER RANGE  表示件数を入力して下さい。  [1<=x<=50]
  --help               Show this message and exit.

# python scripts/main.py key --help
Usage: main.py key [OPTIONS] KEY

  API Key を保存するサブコマンド。引数に API Key を指定して下さい。

Options:
  --help  Show this message and exit.
```