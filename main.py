import requests
from datetime import datetime
import discord
from discord.ui import Button, View
import random
from arquivos import *
import asyncio
from time import sleep

# fazer a solicitação HTTP GET para a API
url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR&allowCountries=BR'
response = requests.get(url)
data = response.json()

# obter a data e hora atual
now = datetime.now()

jogos = []
notificacoes = []

channel_id = 1071946731358527581
token = os.getenv('TOKEN')

# iterar sobre os jogos na resposta da API
def buscarJogos():
    msg = []
    for game in data['data']['Catalog']['searchStore']['elements']:
        # verificar se o jogo tem promoções
        if game["promotions"] != None:
            if(len(game['promotions']['promotionalOffers']) > 0):
                # verificar se o jogo está atualmente disponível
                startDate = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate']
                endDate = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
                startDate = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S.%fZ')
                endDate = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S.%fZ')
                print(game['catalogNs']['mappings'][0]['pageSlug'])
                if startDate <= now and now <= endDate:
                    # verificar se o preço de desconto é igual ao preço original
                    originalPrice = game['price']['totalPrice']['fmtPrice']['originalPrice']
                    discountPrice = game['price']['totalPrice']['fmtPrice']['discountPrice']
                    if int(discountPrice) == 0:
                        # mostrar todas as informações do jogo
                        # print(f"Nome: {game['title']}")
                        # print(f"Preço original: {originalPrice}")
                        # print(f"Preço com desconto: {discountPrice}")
                        print(f"URL do jogo na Epic Games: https://www.epicgames.com/store/pt-BR/p/{game['catalogNs']['mappings'][0]['pageSlug']}")
                        # print(f"Data de início da oferta: {startDate}")
                        # print(f"Data final da oferta: {endDate}")
                        # print(f"Descrição do jogo: {game['description']}")
                        # print(f"Imagem template: {game['keyImages'][0]['url']}")
                        # print("--------------------------------------------------")
                        # adicionar informações do jogo à mensagem
                        # criar mensagem com as informações do jogo
                        titulo = game['title']
                        dataInicioOferta = startDate.strftime('%d/%m/%Y')
                        dataFinalOferta = endDate.strftime('%d/%m/%Y')
                        precoOriginal = originalPrice
                        precoDesconto = "R$ {:,.2f}".format(int(discountPrice)).replace(".", ",")
                        urlParaDownload = f"https://www.epicgames.com/store/pt-BR/p/{game['catalogNs']['mappings'][0]['pageSlug']}"
                        descricaoJogo = game['description']
                        imagemJogo = game['keyImages'][0]['url']
                        msg.append({
                            "titulo": titulo,
                            "dataInicioOferta": dataInicioOferta,
                            "dataFinalOferta": dataFinalOferta,
                            "precoOriginal": precoOriginal,
                            "precoDesconto": precoDesconto,
                            "urlParaDownload": urlParaDownload,
                            "descricaoJogo": descricaoJogo,
                            "imagemJogo": imagemJogo
                        })
    return msg

def montarMensagemJogo(jogo):
    mensagem = ""
    mensagem = f"**{jogo['titulo']}**\n\n"
    mensagem += f"📅 Data de início da oferta: {jogo['dataInicioOferta']}\n\n"
    mensagem += f"📅 Data final da oferta: {jogo['dataFinalOferta']}\n\n"
    mensagem += f"💰 Preço original: {jogo['precoOriginal']}\n\n"
    mensagem += f"💰 Preço com desconto: {jogo['precoDesconto']}\n\n"
    mensagem += f"🔗 URL do jogo na Epic Games: {jogo['urlParaDownload']}\n\n"
    mensagem += f"📝 Descrição do jogo:\n{jogo['descricaoJogo']} \n\n"
    return mensagem

def criarEmbedJogo(jogo):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    cor = f"0x{r:02x}{g:02x}{b:02x}"
    color = int(cor, 16)
    embed = discord.Embed(title=jogo['titulo'], description=jogo['descricaoJogo'], color=int(cor, 16))
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="", value="**========JOGO GRATUITO PANOIZ, JA PEGA LA!!!========**", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="📅 Data de início da oferta:", value=jogo['dataInicioOferta'], inline=True)
    embed.add_field(name="📅 Data final da oferta:", value=jogo['dataFinalOferta'], inline=True)
    embed.add_field(name="💰 Preço original:", value=jogo['precoOriginal'], inline=True)
    embed.add_field(name="💰 Preço com desconto:", value=jogo['precoDesconto'], inline=True)
    embed.add_field(name="🔗 URL do jogo na Epic Games:", value=jogo['urlParaDownload'], inline=False)
    embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/HoxMAt12vkgiWp07T0KtAMsOw-4=/0x0:1200x800/920x613/filters:focal(504x304:696x496):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/63375210/fortnite_logo.0.png")
    embed.set_footer(text="Criado por Mauricio", icon_url="https://cdn.discordapp.com/avatars/427934386059476993/3baf9c5166a4f273d9d83e01982f8d6e.webp")
    embed.set_image(url=jogo['imagemJogo'])
    return embed

def criarBotoesJogo(jogo):
    button = Button(style=discord.ButtonStyle.green, label="Clique aqui para pegar o jogo!", url=jogo['urlParaDownload'])
    view = View()
    view.add_item(button)
    return view

async def enviarMsgDiscord(client, jogos):
    # obter o canal onde a mensagem será enviada
    titulosSalvos = []
    jogosAprovados = []
    for guild in client.guilds:
        for canal in [g.id for g in guild.text_channels if g.name == "geral"]:
            channel = client.get_channel(canal)
            for jogo in jogos:
                if(verificarExistenciaNotificacao(jogo) == False):
                    if jogo['titulo'] not in titulosSalvos:
                        titulosSalvos.append(jogo['titulo'])
                        jogosAprovados.append(jogo)
                        gruposNotficados = ", ".join([c.name for c in client.guilds])
                        print(f"Jogo {jogo['titulo']} notificado nos grupos {gruposNotficados}")
                    # enviar a mensagem para o canal
                    mencionados = " ".join([m.mention for m in channel.members if m.name != "Jogos Epic"])
                    mensagem_com_mencao = f"{mencionados}\n"
                    embed = criarEmbedJogo(jogo)
                    botoes = criarBotoesJogo(jogo)
                    # msg = await channel.send(content=mensagem_com_mencao, embed=embed, view=botoes)

                    # adicionar reações
                    # await msg.add_reaction('🔥')
                    # await msg.add_reaction('👊')
                    # await msg.add_reaction('❤️')

            # APAGAR MENSAGENS DO BOT
            # await channel.purge(limit=2, check=lambda message: message.author == client.user)
    if(len(jogosAprovados) > 0):
        salvarDadosNotificacaoLista(jogosAprovados, notificacoes)
    else:
        print('Nenhum jogo para notificar! :(')

async def principal(client, nmrBusca):
    print(f"\n\nBusca - {nmrBusca}")
    print('Busacando Jogos na Epic Games')
    jogos = buscarJogos()
    await enviarMsgDiscord(client, jogos)


def verificarExistenciaNotificacao(jogo):
    achou = False
    for n in notificacoes:
        if n['titulo'] == jogo['titulo'] and n['dataInicioOferta'] == jogo['dataInicioOferta'] and n['dataFinalOferta'] == jogo['dataFinalOferta']:
            achou = True
    return achou

def teste():
    intents = discord.Intents.default()  # habilita as intenções padrão (todas exceto as privadas)
    intents.members = True  # habilita a intenção de membros
    client = discord.Client(intents=intents)  # passa as intenções ao criar o objeto Client

    @client.event
    async def on_ready():
        print('Bot está online!')
        channel = client.get_channel(1071946731358527581)
        with open('C:/Users/Mauricio/Downloads/c-cca63b2c92773d54e61c5b4d17695bd2-8.mp3', 'rb') as f:
            audio = discord.File(f)
            await channel.send(file=audio)
    
    client.run(token)

async def agendador(client, nmrBusca):
    while True:
        nmrBusca += 1
        asyncio.create_task(principal(client, nmrBusca))
        await asyncio.sleep(60*60*6) # espera por 1 minuto

def bot():
    intents = discord.Intents.default()  # habilita as intenções padrão (todas exceto as privadas)
    intents.members = True  # habilita a intenção de membros
    client = discord.Client(intents=intents)  # passa as intenções ao criar o objeto Client
    nmrBusca = 0

    @client.event
    async def on_ready():
        print('Bot está online!')
        await agendador(client, nmrBusca)
    client.run(token)

notificacoes = buscarDadosNotificacoesCadastrados()
bot()
# teste()
