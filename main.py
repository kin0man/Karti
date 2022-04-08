from discord.ext import commands
from discord import File
import requests


def isfloat(str_):
    h = True
    for i in str_:
        if i not in '0123456789-.' or str_.count('.') > 1 or str_.count('-') > 1:
            h = False
    return h


bot = commands.Bot(command_prefix='-')
layer = 'map'
longitude = 47.25
lattitude = 56.1
traffic_mode = ''


def image_map():
    global longitude, lattitude, layer
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z=11&l={layer + traffic_mode}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

@bot.command(name='place')
async def Place(ctx, *args):
    global longitude, lattitude, layer, traffic_mode
    Isfloat = False
    Coords = False
    traffic_mode = ''
    if len(args) > 1 and isfloat(args[0]) and isfloat(args[1]):
        Isfloat = True
        if -180 <= float(args[0]) <= 180 and -85 <= float(args[1]) <= 85:
            longitude = float(args[0])
            lattitude = float(args[1])
            Coords = True
    elif not args:
        Isfloat = True
        Coords = True
    if Isfloat and Coords:
        await ctx.send('Вы здесь:')
        image_map()
        await ctx.send(file=File('map.png'))
    elif not Isfloat:
        await ctx.send('Введите долготу и широту')
    elif not Coords:
        await ctx.send('Долгота должна быть в диапозоне от -180 до 180, а широта - от -85 до 85')


@bot.command(name='layer')
async def Layer(ctx, change_layer=None):
    global layer
    list_layers = {'map': 'Схема', 'sat': 'Спутник', 'sat,skl': 'Гибрид'}
    try:
        await ctx.send(f'Слой был изменён с {list_layers[layer]} на {list_layers[change_layer]}')
        layer = change_layer
    except Exception:
        await ctx.send(f'Введите название слоя (map - схема; sat - спутник; sat,skl - гибрид)')


@bot.command(name='traffic')
async def Traffic(ctx, *args):
    global longitude, lattitude, layer, traffic_mode
    if layer == 'sat,skl':
        layer = 'sat'
    traffic_mode = ',trf,skl'
    if not args:
        image_map()
        await ctx.send(file=File('map.png'))
    else:
        await ctx.send('Кроме команды ничего писать не нужно')

bot.run('OTYwOTMyNTkzNzQwNjkzNTQ0.YkxoNw._GyCpz6bmLH4yC5y2Gy2EgcJkpQ')