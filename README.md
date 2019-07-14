# GanttLogger
アクティブウィンドウログをガントチャートで出力する

## 流れ
1. プロセスログを取得
2. プロセスID(名前)，開始時刻を配列に
3. 遷移したらその時刻を終了時刻としても配列にし，直後のプロセスの開始時刻にもする
4. 終了アクションがあったら出力処理でガントチャートをプロセスID(名前)別に時系列に出力
5. 図の保存
