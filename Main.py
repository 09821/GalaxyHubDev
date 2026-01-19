import discord
from discord import app_commands
from discord.ext import commands
import os

# Configurações
ADMIN_ID = 1451570927711158313
ALLOWED_SERVERS = [1458471374812090389, 1458234841370984663]

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Quando o bot fica online
@bot.event
async def on_ready():
    print('='*50)
    print(f'BOT ONLINE!')
    print(f'Nome: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print('='*50)
    
    await bot.change_presence(
        activity=discord.Game(name="Online 24/7 🟢"),
        status=discord.Status.online
    )
    
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comandos sincronizados')
    except Exception as e:
        print(f'Erro ao sincronizar: {e}')

# Verificação de servidor
def is_allowed_server():
    async def predicate(interaction: discord.Interaction):
        if interaction.guild_id not in ALLOWED_SERVERS:
            await interaction.response.send_message("❌ Bot não funciona neste servidor!", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

# Comando ping
@bot.tree.command(name="ping", description="Ver latência do bot")
@is_allowed_server()
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! {latency}ms")

# Comando teste (só admin)
@bot.tree.command(name="admin", description="Comando de admin")
@is_allowed_server()
async def admin_test(interaction: discord.Interaction):
    if interaction.user.id != ADMIN_ID:
        await interaction.response.send_message("❌ Você não é o admin!", ephemeral=True)
        return
    
    await interaction.response.send_message("✅ Você é o Admin Branzz!", ephemeral=True)

# Pega o token
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("❌ ERRO: Token não encontrado!")
    print("Adicione DISCORD_TOKEN nos Secrets do Replit!")
else:
    print("✅ Token encontrado, iniciando bot...")
    bot.run(TOKEN)
