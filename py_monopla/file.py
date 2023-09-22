from . import auth
import os
import urllib.request

SIPF_FILE_REQ_URL="https://file.sipf.iot.sakura.ad.jp/v1/files/"

def _request_file_url(file_id, auth, is_upload):
    req_url = SIPF_FILE_REQ_URL + file_id + "/"
    http_method = 'GET'
    if is_upload:
        http_method = 'PUT'
    #Basic認証ヘッダを生成
    basic_auth_header = {'Authorization': 'Basic ' + auth.basic_auth_value()}
    #URLをリクエスト
    try:
        req = urllib.request.Request(req_url, headers=basic_auth_header, method=http_method)
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        return -err.code
    
    url = body.decode('utf-8')
    return url

def request_file_upload_url(file_id, auth):
    return _request_file_url(file_id, auth, True)

def request_file_download_url(file_id, auth):
    return _request_file_url(file_id, auth, False)

def send_upload_complete(file_id, auth):
    req_url = SIPF_FILE_REQ_URL + file_id + "/complete/"
    #Basic認証ヘッダを生成
    basic_auth_header = {'Authorization': 'Basic ' + auth.basic_auth_value()}
    #URLをリクエスト
    try:
        req = urllib.request.Request(req_url, headers=basic_auth_header, method='PUT')
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        return -err.code
    return 0

def upload(file_path, file_id, auth):
    #ファイルを開く
    with open(file_path, 'rb') as f:
        #ファイルサイズを確認(100MB以下かどうか)
        sz_file = f.seek(0, os.SEEK_END)
        if sz_file > (100 * 1024 * 1024):
            return -1
        f.seek(0, 0)

        #アップロード先URLを取得
        up_url = request_file_upload_url(file_id, auth)
        if type(up_url) is int:
            return up_url

        #ファイルをアップロード
        req_headers = {'Content-Type': 'application/octed-stream', 'Content-Length': sz_file}
        try:
            req = urllib.request.Request(up_url, headers=req_headers, data=f, method='PUT')
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            return -err.code

        #送信完了通知
        ret = send_upload_complete(file_id, auth)

        return 0

def download(file_path, file_id, auth):
    #ダウンロードURLを取得
    dl_url = request_file_download_url(file_id, auth)
    if type(dl_url) is int:
        return dl_url

    #ダウンロード実行
    try:
        ret = urllib.request.urlretrieve(dl_url, filename=file_path)
    except urllib.error.HTTPError as err:
        return -err.code

    return 0

