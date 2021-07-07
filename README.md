# cron_python

cronにより定期的にpythonプログラムを実行します

## 内容

- sample.py

cron実行するためのサンプルコードです

- get_hololive_videos_weekly.py

YoutubeDataAPIを利用して動画情報を取得するためのコードです

## 参考

- [cron の使い方（pythonスクリプト）](https://qiita.com/saira/items/76a5538a6b2556f6b339)
- [cronでPython3を定時実行する方法&注意すべき４つのポイント](https://tanuhack.com/cron/)
- [【macOS Catalina】crontab -e でOperation not permittedの解消方法](https://qiita.com/yumenomatayume/items/7fd6286bfb79acb222de)

## メモ

分,時,日,月,曜日で設定

`python`で実行するとdefaultの環境のpythonが実行されるので注意

ディスクアクセスを許可するためにセキュリティプライバシーから`/usr/sbin/cron`にフルディスクアクセスを許可

バッテリーから定期的にスリープを解除して実行されるようにする