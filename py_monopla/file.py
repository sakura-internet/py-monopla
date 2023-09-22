import . from auth
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
    print(req_url)
    #Basic認証ヘッダを生成
    basic_auth_header = {'Authorization': 'Basic ' + auth.basic_auth_value()}
    #URLをリクエスト
    try:
        req = urllib.request.Request(req_url, headers=basic_auth_header, method='PUT')
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        return -err.code

def upload(file_path, file_id, auth):
    #ファイルを開く
    with open(file_path, 'rb') as f:
        #ファイルサイズを確認(100MB以下かどうか)
        sz_file = f.seek(0, os.SEEK_END)
        f.seek(0, 0)

        #アップロード先URLを取得
        up_url = request_file_upload_url(file_id, auth)

        #ファイルをアップロード
        req_headers = {'Content-Type': 'application/octed-stream', 'Content-Length': sz_file}
        try:
            req = urllib.request.Request(up_url, headers=req_headers, data=f, method='PUT')
            with urllib.request.urlopen(req) as res:
                body = res.read()
                print(body)
        except urllib.error.HTTPError as err:
            return -err.code

        #送信完了通知
        ret = send_upload_complete(file_id, auth)
        print(ret)

def download(file_path, file_id, auth):
    #ダウンロードURLを取得
    dl_url = request_file_download_url(file_id, auth)
    print(dl_url)

    #ダウンロード実行
    try:
        ret = urllib.request.urlretrieve(dl_url, filename=file_path)
    except urllib.error.HTTPError as err:
        return -err.code


if __name__ == "__main__":

    ai = auth.SipfAuth()
    ret = auth.get_auth_info(ai)

    #url_up = request_file_upload_url('py_sipf.txt', ai)
    #print(url_up)
    #url_down = request_file_download_url('sipf_file_sample.txt', ai)
    #print(url_down)

    #upload('file.py', 'file.py', ai)
    download('dl.txt', 'sipf_file_sample.txt', ai)
