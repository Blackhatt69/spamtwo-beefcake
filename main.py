import re, os, asyncio, random, string, keep_alive
from discord.ext import commands, tasks

version = 'v2.7'

user_token = os.environ['user_token']
spam_id = os.environ['spam_id']
catch_id = os.environ['catch_id']

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary', 'r') as file:
    legendary_list = file.read()
with open('data/mythical', 'r') as file:
    mythical_list = file.read()
with open('data/level', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
client = commands.Bot(command_prefix='&')
intervals = [3.0, 2.2, 2.4, 2.6, 2.8]


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^' + hint_replaced + '$', pokemon_list,
                          re.MULTILINE)
    return solution


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    await channel.send(''.join(
        random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 7) *
        5))


@spam.before_loop
async def before_spam():
    await client.wait_until_ready()


spam.start()


@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')


@client.event
async def on_message(message):
    channel = client.get_channel(int(catch_id))
    if message.channel.id == int(catch_id):
        if message.author.id == poketwo:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    spam.cancel()
                    await asyncio.sleep(4)
                    await channel.send('<@716390085896962058> h')
                elif "Congratulations" in embed_title:
                    embed_content = message.embeds[0].description
                    if 'now level' in embed_content:
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100:
                            await channel.send(f".s {to_level}")
                            with open('data/level', 'r') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level', 'w') as fo:
                                fo.writelines(data[1:])
            else:
                content = message.content
                if 'The pokémon is ' in content:
                    if not len(solve(content)):
                        print('Pokemon not found.')
                    else:
                        for i in solve(content):
                            await asyncio.sleep(6)
                            await channel.send(f'<@716390085896962058> c {i}')
                    check = random.randint(1, 60)
                    if check == 1:
                        await asyncio.sleep(900)
                        spam.start()
                    else:
                        await asyncio.sleep(1)
                        spam.start()

                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!', '')
                    if 'seem unusual...' in content:
                        shiny += 1
                        print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    elif re.findall('^' + pokemon + '$', legendary_list,
                                    re.MULTILINE):
                        legendary += 1
                        print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    elif re.findall('^' + pokemon + '$', mythical_list,
                                    re.MULTILINE):
                        mythical += 1
                        print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                        print(
                            f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}'
                        )
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')
                elif 'human' in content:
                    spam.cancel()
                    print(
                        'Captcha detected; autocatcher paused. Press enter to restart, after solving captcha manually.'
                    )
                    input()
                    await channel.send('<@716390085896962058> h')
    if not message.author.bot:
        await client.process_commands(message)


@client.command()
async def say(ctx, *, args):
    await ctx.send(args)


print(
    f'Pokétwo Autocatcher {version}\nA free and open-source Pokétwo autocatcher Modified by BEEEFCAKE\nEvent Log:'
)
keep_alive.keep_alive()
client.run(f"{user_token}")
