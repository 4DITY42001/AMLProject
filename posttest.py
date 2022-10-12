import requests
url = 'http://56812bf26b89.ngrok.io/uploader'
myobj = {'allface_arr': [1,2,3,4]}
x = requests.post(url, json=myobj)
print(x.text)
