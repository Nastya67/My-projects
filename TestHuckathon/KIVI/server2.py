import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import vk
import time
import Config

r = requests.get("https://api.ovva.tv/v2/ru/tvguide/1plus1")
data = json.loads(r.text)
print(data)

white= (255, 255, 255)
pic = Image.open('pic0.png')#Image.new('RGB', (1590, 400), white)
imgDrawer = ImageDraw.Draw(pic)
font = ImageFont.truetype('Arimo-Regular.ttf', 27)
font1 = ImageFont.truetype('Arimo-Regular.ttf', 20)
y = 0
x = 140

for film in data['data']['programs']:
    res = requests.get(film['image']['preview'])
    img = Image.open(BytesIO(res.content))
    img.thumbnail((70, 70),Image.ANTIALIAS)
    pic.paste(img, (x-80, 110+y*75))
    txt = film['title']
    if len(film['title']) > 27:
        txt = film['title'][:27]+"..."
    btime = str(time.gmtime(film['realtime_begin']).tm_hour)+":"+str(time.gmtime(film['realtime_begin']).tm_min)
    etime = str(time.gmtime(film['realtime_end']).tm_hour)+":"+str(time.gmtime(film['realtime_end']).tm_min)
    imgDrawer.text((x, 110+y*75), txt, font=font, fill=(255, 255, 255))
    imgDrawer.text((x, 140+y*75), btime+"-"+etime, font=font1)
    
    y+=1
    if 110+y*75 >=780:
        x += 500
        y = 0

pic.save("pic1.png")

pic.show()

session = vk.Session(access_token=Config.key)
api = vk.API(session)
img = {'photo': ('pic1.png', open(r'C:\Users\Hradi\Desktop\TestHuck\pic1.png', 'rb'))}
a = api.photos.getWallUploadServer(group_id=140448844)
url = a['upload_url']
response = requests.post(url, files=img)
ph = json.loads(response.text)
q = api.photos.saveWallPhoto(group_id=140448844, photo=ph['photo'], server=ph['server'], hash=ph['hash'] )
w = api.wall.post(owner_id=-140448844, attachments=q[0]['id'])
