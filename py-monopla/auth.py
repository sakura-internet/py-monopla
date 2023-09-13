import urllib.request
import base64

class SipfAuth:
    user_name = None
    password = None

    def basic_auth_value(self):
        return base64.b64encode(("%s:%s" % (self.user_name, self.password)).encode()).decode()

def get_auth_info(auth):
    if not (type(auth) is SipfAuth):
        raise TypeError("auth is invalid type")

    #HTTPSで認証情報を取得
    try:
        req = urllib.request.Request("http://auth.sipf.iot.sakura.ad.jp/v0/session_key", method='POST')
        with urllib.request.urlopen(req) as res:
            body = res.read()
    except urllib.error.HTTPError as err:
        return -err.code

    #authに格納
    auth_value = body.decode('utf-8').split('\n')
    if len(auth_value) >= 2:
        auth.user_name = auth_value[0]
        auth.password = auth_value[1]
        return 0
    else:
        return -1

if __name__ == "__main__":
    auth = SipfAuth()

    try:
        ret = get_auth_info(auth)
        print("get_auth_info() ret=%d" % ret)
    except Exception as e:
        print(e)
    else:
        print("Username: %s, Password: %s" % (auth.user_name, auth.password))

