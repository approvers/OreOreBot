import requests
import lxml.html


def get_weather():
    url = "https://tenki.jp/forecast/3/11/4010/8201/"
    results = {
        "today":{},
        "tomorrow":{}
    }

    r = requests.get(url)
    html = lxml.html.fromstring(r.text)

    results["today"]["weather"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[1]/div[1]/div[1]/img')[0]\
            .attrib['alt']
    results["tomorrow"]["weather"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[2]/div[1]/div[1]/img')[0]\
            .attrib['alt']

    results["today"]["high"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[1]/div[1]/div[2]/dl/dd[1]/span[1]')[0]\
            .text
    results["tomorrow"]["high"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[2]/div[1]/div[2]/dl/dd[1]/span[1]')[0]\
            .text

    results["today"]["low"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[1]/div[1]/div[2]/dl/dd[3]/span[1]')[0]\
            .text
    results["tomorrow"]["low"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[2]/div[1]/div[2]/dl/dd[3]/span[1]')[0]\
            .text
    
    results["today"]["high_diff"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[1]/div[1]/div[2]/dl/dd[2]')[0]\
            .text
    results["tomorrow"]["high_diff"]= \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[2]/div[1]/div[2]/dl/dd[2]')[0]\
            .text

    results["today"]["low_diff"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[1]/div[1]/div[2]/dl/dd[4]')[0]\
            .text
    results["tomorrow"]["low_diff"] = \
        html.xpath('//*[@id="main-column"]/section/div[2]/section[2]/div[1]/div[2]/dl/dd[4]')[0]\
            .text
    return results


if __name__ == "__main__":
    print(get_weather())

