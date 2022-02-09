import os
import requests
from bs4 import BeautifulSoup


# 图片防盗链，想要请求的话需要带上Referer
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
#     'Referer': 'https://www.dmzj.com/',
#     'Host': 'images.dmzj.com'
# }
# res = requests.get("https://images.dmzj.com/img/chapterpic/28739/110239/15560700290294.jpg", headers=headers)
# print(res.text)

# 写入以及执行的js文件名
JS_FILE_NAME = "dmzj.js"


# 获取指定网页内的js代码
def getJSCode(htmlUrl):
    res = requests.get(htmlUrl)
    bs = BeautifulSoup(res.text, "html.parser")
    content = str(bs.find("script")).split('<script type="text/javascript">')[1].split("</script>")[0]
    return content


# 将爬取到的js代码写入到指定文件中
def writeJS(code):
    code = code + """
        function getData(code) {
            pages = pages.replace(/\\n/g,"");
            pages = pages.replace(/\\r/g,"|");
            var info = eval("(" + pages + ")");
            var picArry = info['page_url'].split("|");
            var pic = [];
            for (let i = 0; i < picArry.length; i ++) {
                pic[i] = "https://images.dmzj.com/" + picArry[i];
            }
            return pic;
        }

        console.log(getData());
    """
    with open(JS_FILE_NAME, "w") as f:
        f.write(code)


# 调用node.js 执行js文件 并输出结果
def execJSFile(htmlUrl):
    writeJS(getJSCode(htmlUrl))
    result = os.popen('node ' + JS_FILE_NAME)
    print(result.read())


if __name__ == '__main__':
    execJSFile("https://www.dmzj.com/view/jinshangxiang/83369.html")
