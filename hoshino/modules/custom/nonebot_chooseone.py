import random
from nonebot import get_bot

bot=get_bot()
@bot.on_message('group')
async def chooseone(ctx):
    message = ctx['raw_message']
    if message.startswith('选择'):
        msg=message[2:].split('还是')
        if len(msg)==1:
            await bot.send(ctx, '请发送“选择aa还是bb”')
            return
        a,b=msg
        if len(a)>15 or len(b)>15:
            await bot.send(ctx, '选项必须小于等于15个字符')
            return
        choices=[f'{a}',f'{b}','“我全都要”']
        final_choice=random.choice(choices)
        reply='您的选项是：\n1. {}\n2. {}\n您最终的选择是: {}'.format(a,b,final_choice)
        await bot.send(ctx, reply,at_sender=True)
