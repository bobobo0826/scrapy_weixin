tt="mp.weixin.qq.com/s?__biz=MzAxNDY2NzM1Mg==&mid=400837033&idx=5&sn=ebc214aaf99f119b3f4c98f093e97ef2&scene=27#wechat_redirect <html><head></head><body></body></html>"
if "https://mp.weixin.qq.comhttp//" or "<html><head></head><body></body></html>" in tt:
    print(1)
    a = tt.replace("https://mp.weixin.qq.comhttp//", "https://")
    if "#wechat_redirect" in a:
        b = a.replace("#wechat_redirect", "")
        true_url = b
    else:
        true_url = a
else:
    true_url = tt

print(true_url)