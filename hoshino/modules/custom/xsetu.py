import random
from hoshino import R, CommandSession,Service,Privilege as Priv
from nonebot import MessageSegment
import requests
import re

rurl = 'http://api.h-loli.cc'

sv=Service('xsetu',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)


@sv.on_command('setu',aliases=('色图','涩图','瑟图'))
async def setu(session:CommandSession):
    r1 = requests.get(rurl+'/1.php')
    rtx = r1.text
    res = re.search("\"([^\"]*)\"", rtx).group(1)
    rres = rurl+'/'+res
    setuurl=MessageSegment.image(rres)
    await session.send(setuurl)
