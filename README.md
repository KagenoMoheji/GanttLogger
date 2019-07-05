# ActiveTabGanttLogger
アクティブウィンドウログをガントチャートで出力する

## 流れ
1. プロセスログを取得
2. プロセスID(名前)，開始時刻を配列に
3. 遷移したらその時刻を終了時刻としても配列にし，直後のプロセスの開始時刻にもする
4. 終了アクションがあったら出力処理でガントチャートをプロセスID(名前)別に時系列に出力
5. 図の保存

## テスト環境
- OS
    - Windows10 64bit
    - MacOS Mojave10.14.5
- ブラウザ
    - Google Chrome75.0.3770.100
- Python
    - 3.7

## 名称やコマンドの改名
- 「ActiveTabGanttLogger」や`ganttlogger`は微妙
- アクティブウィンドウ遷移・マウス・キーボードを観測してガントチャート・折れ線・棒グラフを出力するし…
- タスクを監視…「PCTaskObserver」と`tskobsr`？
- ほかに良い名前無いかな…

## 仕様
- MouseObserver・KeyboardObserverの最低デルタtは1s．
    - 1s間の操作量ごとに取得

## 課題点
- モジュール選定
    - [x] `threading.Thread`か？`concurrent.futures.ThreadPoolExecutor`か？
        - てかマルチスレッドかマルチプロセスかもわからん
        - とりま`threading.Thread`でやるか，自前関数で外部からの操作ができるかもだし．  
        `concurrent.futures`のは詳しく調べられないからよくわからん．
        - [Pythonの並列・並行処理サンプルコードまとめ | Qiita](https://qiita.com/castaneai/items/9cc33817419896667f34)
        - `KeyboardObserver`クラスで`threading.Thread`を継承した`MyThread`クラスを使用することにして，その親である`Observer`クラスで`threading.Thread`と`MyThread`クラスが使えなかったのでそちらは`concurrent.futures`を簡単に使い，更にその親である`Alone`クラスでは`concurrent.futures`と`MyThread`クラスが使えなかったので`threading.Thread`を使う方針にした．
            - [pythonでのスレッド](http://nobunaga.hatenablog.jp/entry/2016/06/03/204450)
            - これを見るに，親子のスレッドで同じモジュールやそれを継承したサブクラスを使用することができないってことなのか？？？
    - [x] `numpy.append()/pop()`か？`collections.deque.append()/popleft()`か？`[].append()/pop(0)`か？
        - 読んだ感じでは`collections.deque`>`[]`>`numpy`かねぇ．
        - [Python キュー（queue）を使う（先入れ先出し）](https://pg-chain.com/python-queue)
        - [python と numpy の配列。追加や削除、ソートなど基本操作](http://ailaby.com/list_array/#id3_2)
        - [速度：Pythonの配列の末尾に要素追加 | Qiita](https://qiita.com/ykatsu111/items/be274f76d42f6b982ba4)
        - [Pythonでリスト（配列）の要素を削除するclear, pop, remove, del](https://note.nkmk.me/python-list-clear-pop-remove-del/#pop)
- [ ] Pythonの`exit()`と`sys.exit()`と`os._exit()`
    - 違いがわからんのでとりあえず全て`exit()`にしてる
- Chrome(ブラウザ)のタブ遷移の検出について
    - [ ] タブ遷移の検出にはページタイトルの相違によって行われている
        - もしページタイトルが全部同じWebサイトだったら遷移を検出できない可能性
        - ページタブごとのプロセスIDとか識別子はあるのか？
    - [x] URLの取得が難しそう
        - [アクティブタブとなったChromeのページURLを取得したい | teratail](https://teratail.com/questions/197377)に投げてあるが期待薄
        - タブバーのテキスト(上の項目にあるやつ．ページタイトル)で区別することに．
    - [ ] Googleドライブからドキュメントを開くなど外部アプリに飛ぶ際に、`Chrome(無題)`と出る。
        - これはログに書き出す前に除去しよう
- [ ] 仮想デスクトップ移動時の瞬間的なアクティブタブの検出について
    - 最低デルタt=1s未満ならLogに追加しない
    - というか勝手に検出してくれないから気にしなくても良さそう？
- [ ] スリープさせたら止まっちゃう
- [ ] 文字を消しているときのBack Space**長押し**の検出ができない．
    - これは今はやらず，そのうち実装しよう
    - pynputモジュールの`on_press`と`on_release`間の時間の取得になるだろうな．