import random
from hoshino import R, CommandSession,Service,Privilege as Priv


sv=Service('bwthreat',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)




kximg = R.img('priconne/quick/kaixue.jpg').cqcode
zuoshushu=R.img('priconne/quick/zuoshushu.png').cqcode
five=R.img('priconne/quick/five.png').cqcode

@sv.on_command('kaixue', aliases=("迫害上课","迫害开学"), only_to_me=False)
async def kaixue(session: CommandSession):
    await session.send(f'“这是谁说的？我咋不知道？不要问我呀”\n{kximg}', at_sender=True)


@sv.on_command('wu',aliases=("迫害克罗爱",'迫害老五'))
async def wu(session: CommandSession):
    await session.send(f'“我想上头试试 强抽亚里沙”\n{five}', at_sender=True)

@sv.on_command('zss',aliases=("迫害左树树",'迫害佐树树','迫害seraph'))
async def zss(session: CommandSession):
    await session.send(f'“群里就我没亚里莎了”\n{zuoshushu}', at_sender=True)
