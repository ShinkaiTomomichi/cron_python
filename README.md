# cron_python

cronにより定期的にpythonプログラムを実行します

## 内容

- get_videos_weekly_template.py

YoutubeDataAPIを利用して動画情報を取得するためのプログラムです
パスに適当な値を利用して利用してください

## sample cron

0 * * * * <pythonの絶対path> <programの絶対パス> > <logfileの絶対パス>

## 参考

- [cron の使い方（pythonスクリプト）](https://qiita.com/saira/items/76a5538a6b2556f6b339)
- [cronでPython3を定時実行する方法&注意すべき４つのポイント](https://tanuhack.com/cron/)
- [【macOS Catalina】crontab -e でOperation not permittedの解消方法](https://qiita.com/yumenomatayume/items/7fd6286bfb79acb222de)

## メモ

`crontab -e`で編集、`crontab -l`で確認できる

周期は分, 時, 日, 月, 曜日で設定する

`python`で実行するとdefaultの環境のpythonが実行されるので、適切なpathを選択する

ファイルアクセスを許可するためにセキュリティプライバシーから`/usr/sbin/cron`にフルディスクアクセスを許可する

バッテリーから定期的にスリープを解除して実行されるようにする

Quotaは以下を参照   

https://developers.google.com/youtube/v3/determine_quota_cost?hl=ja