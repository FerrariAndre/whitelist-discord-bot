import os
import re
import discord
from dotenv import load_dotenv

#Carrengado variaveis de ambiente
load_dotenv()
token_bot = os.getenv("DISCORD_TOKEN")
channel_whitelist = int(os.getenv("WHITELIST_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
processed = set()


@client.event
async def on_ready():
    print(f'Logado como {client.user}')

@client.event
async def on_raw_reaction_add(payload):
    is_administrator = False
    channel = client.get_channel(payload.channel_id)
    if payload.member is None or payload.member.bot: return

    if channel is None or channel_whitelist != channel.id: return

    roles = payload.member.roles
    for role in roles:
        if role.permissions.administrator:
            is_administrator = True
            break

    if payload.emoji.name == "✅" and is_administrator:
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            print("Mensagem não encontrada")
            return
        except discord.Forbidden:
            print("Sem permissão")
            return
        except discord.HTTPException:
            print("Erro")
            return

        if message.author.bot: return

        if message.id in processed:
            print("Mensagem já processada")
            return

        nickname = message.content.strip()

        if not validate_nickname(nickname): return
        processed.add(message.id)
        print(f"Aprovação autorizada: nickname={nickname}, aprovador={payload.member.name}, idAprovador={payload.member.id}, idMensagem={message.id}")

def validate_nickname(nickname):
    result = re.fullmatch(r"[A-Za-z0-9_]{3,16}", nickname)

    if result is not None:
        print("Nickname válido.")
        return True
    else:
        print("Nickname inválido.")
        return False

def validate_token(token):
    if token:
        print("Token encontrado.")
        return True
    else:
        print("Token não encontrado")
        return False

if validate_token(token_bot):
    client.run(token_bot)