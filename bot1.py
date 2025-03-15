import disnake
from datetime import datetime
from disnake.ext import commands

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all(), test_guilds=[Айди сервера ДС])

CENSORED_WORDS = ["卐", "卐******", "ебанутый", "ёбанутый", "блять", "бля", "нахуй", "бл", "пошёл нахуй", "член", "мать", "отец", "маму", "бабушку", "бабушка", "дед", "ебать", "ёб", "хуй", "блятb", "похуй", "ботик пидор", "ботик чмо", "пидор", "xyй", "залупа", "залупень", "блядун", "бля", "мастурбатор", "иди нахуй2", "иди наху", "пися", "мамок ваших чпохан чпохан", "сучка смакай яйки"],
CENSORED_WORDS = ["https://t.me"] #Плохие слова, данная штучка будет использоватся в коде ниже


@bot.event
async def on_ready():
	print(f"Bot {bot.user} is ready to work!") #Отвечает за работу бота


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(Айди канала) #Канала в который будет вывадится сообщение

    embed = disnake.Embed(
        title=f"{member.name} присоединился к GitHub - Discord Server!", #Текс при входе человека на сервер
        description="\n",
        color=disnake.Color.red(),
        timestamp=datetime.now(),
    )

    await channel.send(embed=embed)


@bot.event
async def on_member_join(member): #Выдача роли при входе на сервер
    guild = member.guild
    role = guild.get_role(Айди роли)

    await member.add_roles(role)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(Айди канала) #Канала в который будет вывадится сообщение

    if channel: #Сообщение если канал будет не найден
        embed = disnake.Embed(title=f"{member.name} покинул сервер", description=f"\n", color=0xFF0000, timestamp=datetime.now())
        await channel.send(embed=embed)
    else:
        print("Канал не найден.")


@bot.event
async def on_message(message): #Когда участник будет писать плохое слово
    await bot.process_commands(message)

    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                embed = disnake.Embed(title="Цензура", description=f"{message.author.mention}, такие слова запрещены!", color=0xFF0000)
                await message.delete()
                await message.channel.send(embed=embed)
                return


@bot.event
async def on_command_error(ctx, error): #Когда у участника не будет прав на команды адм
	print(error)

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
	elif isinstance(error, commands.UserInputError):
		await ctx.send(embed=disnake.Embed(
			discription=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
		))


@bot.slash_command(usage="kick <@user> <reason=None>", description="Выгнать участника.") #Слеш-Команда чтобы выгнать участника с сервера
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил!"):
    await member.kick(reason=reason)
    
    embed = disnake.Embed(
        title=f"{member.name} был кикнут!",
        description=f"Причина: {reason}",
        color=disnake.Color.red(),
        timestamp=datetime.now(),
    )

    await ctx.send(embed=embed)


@bot.slash_command(usage="ban <@user> <time> <reason=None>", description="Заблокировать участника.") #Слеш-Команда чтобы забанить участника на сервера
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил!"):
    await member.ban(reason=reason)
    
    embed = disnake.Embed(
        title=f"{member.name} был заблокирован!",
        description=f"Причина: {reason}",
        color=disnake.Color.red(),
        timestamp=datetime.now(),
    )

    await ctx.send(embed=embed)


@bot.slash_command() #Слеш-Команда чтобы разбанить участника на сервера
async def unban(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = disnake.Embed(
            title="Пользователь разбанен",
            description=f"{user.mention} был успешно разбанен.",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed) #Участника нету на сервере
    except disnake.NotFound:
        embed = disnake.Embed(
            title="Ошибка",
            description="Пользователь не найден.",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed) #У вас нет прав для разбана
    except disnake.Forbidden:
        embed = disnake.Embed(
            title="Ошибка",
            description="У меня нет прав на разбан пользователя.",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)


 
@bot.slash_command(usage="mute <@user> <time> <reason=None>", description="Замутить участника.") #Слеш-Команда чтобы выдать участнику мут на сервера
async def mute(ctx, member: disnake.Member, *, reason=None):
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    
    await member.add_roles(muted_role, reason=reason)
    
    embed = disnake.Embed( #Выводит сообщение что участник успешно замучен
        title=f"{member.name} был замучен!",
        description=f"Причина: {reason}",
        color=disnake.Color.red(),
        timestamp=datetime.now(),
    )

    await ctx.send(embed=embed)

@bot.slash_command(usage="unmute <@user>", description="Размутить участника.") #Слеш-Команда чтобы снять мут с участника на сервере
async def unmute(ctx, member: disnake.Member):
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        return await ctx.send("Роль 'Muted' не найдена. Участник не замучен.")
    
    if muted_role not in member.roles: #Ну тут думаю понятно
        return await ctx.send("Участник не замучен.")
    
    await member.remove_roles(muted_role)
    
    embed = disnake.Embed( 
        title=f"{member.name} был размучен!",
        color=disnake.Color.green(),
        timestamp=datetime.now(),
    )

    await ctx.send(embed=embed)


@bot.slash_command(usage="clear <amount> [member]", description="Удалить сообщения участника.") #Слеш-Команда чтобы очисть чат на сервера
async def clear(ctx, value: int, member: disnake.Member = None):
    if value:
        if value > 0:
            if value > 1000:
                e_emb = disnake.Embed(title="Ошибка!", description="Число слишком большое! [Не более 1000]", color=disnake.Color.red())
                await ctx.send(content=f"{ctx.author.mention}", embed=e_emb, delete_after=15)
            else:
                if value < 1:
                    e_emb = disnake.Embed(title="Ошибка!", description="Число слишком низкое! [Не менее 1]", color=disnake.Color.red())
                    await ctx.send(content=f"{ctx.author.mention}", embed=e_emb, delete_after=15)
                else:
                    # Проверяем права участника
                    if ctx.author.guild_permissions.manage_messages:
                        if member is not None:
                            deleted = await ctx.channel.purge(limit=(value+1), check=lambda m: m.author == member)
                            s_emb = disnake.Embed(title="Успешно!", description=f"Вы очистили {value} сообщений у участника {member.mention}!", color=disnake.Color.green())
                            await ctx.send(content=f"{ctx.author.mention}", embed=s_emb, delete_after=15)
                        else:
                            deleted = await ctx.channel.purge(limit=(value+1))
                            s_emb = disnake.Embed(title="Успешно!", description=f"Вы очистили {value} сообщений!", color=disnake.Color.green())
                            await ctx.send(content=f"{ctx.author.mention}", embed=s_emb, delete_after=15)
                    else:
                        e_emb = disnake.Embed(title="Ошибка!", description="У вас нет прав на удаление сообщений!", color=disnake.Color.red())
                        await ctx.send(content=f"{ctx.author.mention}", embed=e_emb, delete_after=15)
        else:
            e_emb = disnake.Embed(title="Ошибка!", description="Вы не указали число сообщений для очистки!", color=disnake.Color.red())
            await ctx.send(content=f"{ctx.author.mention}", embed=e_emb, delete_after=15)
    else:
        e_emb = disnake.Embed(title="Ошибка!", description="Вы не указали число сообщений для очистки!", color=disnake.Color.red())
        await ctx.send(content=f"{ctx.author.mention}", embed=e_emb, delete_after=15)


@bot.slash_command(usage="ping", description="Узнать текущую задержку бота.") #Слеш-Команда чтобы узнать ваше соединение с сервером
async def ping(ctx):
    embed = Embed(title='Понг!', description=f'Задержка: {round(bot.latency * 1000)}ms', color=disnake.Color.green())
    await ctx.send(embed=embed)


@bot.command() #Слеш-Команда чтобы вы могли вывести правила от именни бота
async def send_embed(ctx): 
    embed = disnake.Embed(
        title='📜Правила сервера📜',
        description='📎**1.1**\n'
                    '```Каждый новый пользователь, автоматически соглашается с правилами данного сервера и правилами платформы Discord.```\n'
                    '📎**1.2**\n'
                    '```Незнание правил не освобождает от ответственности.**```\n'
                    '📎**1.3**\n'
                    '```Администрация сервера может заблокировать участника на ограниченный, либо же неограниченный срок в случае нарушения правил.```\n'
                    '📎**1.4  Флуд**\n'
                    '```- Запрещен флуд одинаковыми сообщениями более 3 раз. - Запрещено использованией команд в чат, исключением являются команды эмоций, но использовать их можно с ограничением 2 команды в минуту Наказание: Варн, при повторном нарушении мут от 1 дня.```'
                    '📎**1.5  Запрещено использование следующих ников**\n'
                    '```- Ники, носящие оскорбительный характер; - Ники, выдающие себя за администрацию.; Наказание: Смена ника администрацией, при повторном случае варн/мут```',
        color=disnake.Color.red()
    )
    await ctx.send(embed=embed)


bot.run("Токен бота из Discord Developet")