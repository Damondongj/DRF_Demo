import requests
import json

url = "https://scl.chipslightai.com/api/exam/27/"
headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6", "Connection": "keep-alive",
           "Cookie": "csrftoken=p5y0WSEDCYdi0gaZ9MlemmrEF6rAj7z6pieDQlnwqEzLxGazMdakNZqNbdPlqBJf; ab.storage.deviceId.a9882122-ac6c-486a-bc3b-fab39ef624c5=%7B%22g%22%3A%223ae4815b-82dc-d49c-eea0-b8adec4a1300%22%2C%22c%22%3A1681883366448%2C%22l%22%3A1681883366448%7D",
           "Host": "scl.chipslightai.com", "Referer": "https://scl.chipslightai.com/",
           "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Sec-Fetch-Dest": "empty",
           "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
           "token": "eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFkbWluQHFxLmNvbSIsImV4cCI6MTY4MjQ4ODE2NH0.zhBTPb3eGxSV3XosOwAnOLG43puXp212rr1eD6AHUcM",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)

datas = json.loads(response.text)