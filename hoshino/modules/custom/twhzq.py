import random
from hoshino import R, CommandSession,Service,Privilege as Priv


sv=Service('hzqthreat',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)


xiaobao_aliases = ('迫害奉孝', '迫害孝宝')
bbl_aliases = ('迫害bbl', '迫害芭芭拉')
xbimg1 = R.img('priconne/quick/xiaobao.png').cqcode
bblimg = R.img('priconne/quick/bbl.png').cqcode
xbimg2 = R.img('priconne/quick/xiaobao1.png').cqcode


@sv.on_command('xiaobao', aliases=xiaobao_aliases, only_to_me=False)
async def xiaobao(session: CommandSession):
    a = random.randint(1, 100)
    if a <= 50:
        await session.send(f'您又迫害孝宝了！孝宝要哭了\n{xbimg1}', at_sender=True)
    else:
        await session.send(f'您又迫害孝宝了！孝宝要哭了\n{xbimg2}', at_sender=True)


@sv.on_command('bbl', aliases=bbl_aliases, only_to_me=False)
async def bbl(session: CommandSession):
    await session.send(f'不要这样啊！你们不要再迫害bbl了呀！\n{bblimg}', at_sender=True)
