# py-monopla

`py-monopla` は、[さくらのモノプラットフォーム](https://iot.sakura.ad.jp/platform/)のデバイスアダプターに対するクライアントライブラリです。

## Install

GitHubからリポジトリをクローン

```
git clone https://github.com/sakura-internet/py-monopla.git
```

自己署名TLS証明書のインストール

```
cd py-monopla
sudo ./install_crt.sh
```

Pythonパッケージのインストール

```
pip install .
```

## Dependencies

Raspberry Pi 4 + Raspberry Pi OSをターゲットに開発しています。

本ライブラリの動作には以下の環境が必要です

* モノプラットフォームのプロジェクトに登録されたセキュアモバイルコネクトのSIM
* 上記SIMで接続できるLTEモデム

モノプラットフォームのデバイスアダプターはセキュアモバイルコネクト経由での接続のみ可能です。  
インターネット経由ではアクセスできません。


## Sample programs

`samples`ディレクトリにSIPF_OBJECTプロトコルによる送信/受信、SIPF_FILEプロトコルによるアップロード/ダウンロードのサンプルスクリプトがあります。

```
samples/
  +- file_download.py - SIPF_FILEプロトコルによるダウンロード
  +- file_upload.py   ‐ SIPF_FILEプロトコルによるアップロード
  +- object_rx.py     ‐ SIPF_OBJECTプロトコルによる受信
  +- object_tx.py     - SIPF_OBJECTプロトコルによる送信
```
