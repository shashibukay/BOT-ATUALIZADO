import discord
from discord.ext import commands

# Configuração do bot com as intenções necessárias
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True  # Adicionando a intenção necessária

bot = commands.Bot(command_prefix='/', intents=intents)

# Evento disparado quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Bot está online e pronto como {bot.user}!')

# Comando de ping para verificar a latência do bot
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! Latência: {round(bot.latency * 1000)}ms')

# Comando para mostrar o link da insígnia de desenvolvedor
@bot.command()
async def developer(ctx):
    await ctx.send("Para resgatar a insígnia de desenvolvedor do Discord, visite: https://discord.com/developers/active-developer")

# Comando para mostrar o perfil de um membro
@bot.command()
async def perfil(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Perfil de {member.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Nome:", value=member.display_name, inline=False)
    embed.add_field(name="Data de entrada no servidor:", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S UTC"), inline=False)
    
    roles = [role.mention for role in member.roles if role.name != "@everyone"]
    embed.add_field(name="Cargos:", value=", ".join(roles) if roles else "Nenhum cargo", inline=False)
    
    embed.set_footer(text=f"ID do Usuário: {member.id}")
    await ctx.send(embed=embed)

# Comando para mostrar informações do servidor (guild)
@bot.command()
async def infoserver(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Informações do Servidor: {guild.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)  # Ícone do servidor
    embed.add_field(name="ID do Servidor:", value=guild.id, inline=False)
    embed.add_field(name="Dono do Servidor:", value=guild.owner.mention, inline=False)
    embed.add_field(name="Criado em:", value=guild.created_at.strftime("%d/%m/%Y, %H:%M:%S UTC"), inline=False)
    embed.add_field(name="Membros:", value=guild.member_count, inline=False)
    embed.add_field(name="Canais de Texto:", value=len(guild.text_channels), inline=False)
    embed.add_field(name="Categorias:", value=len(guild.categories), inline=False)
    embed.add_field(name="Cargos:", value=len(guild.roles), inline=False)
    await ctx.send(embed=embed)

# Comando para mostrar o avatar de um membro
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member.display_name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# Comando para limpar mensagens (exemplo de comando útil)
@bot.command()
async def clear(ctx, amount=20):  # Limpa 20 mensagens por padrão
    await ctx.channel.purge(limit=amount + 1)  # +1 para incluir o comando usado na contagem
    await ctx.send(f"{amount} mensagens limpas!")

# Comando para banir membros do servidor
@bot.command()
@commands.has_permissions(ban_members=True)
async def banir(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        await ctx.send("Por favor, especifique o membro que deseja banir.")
        return
    
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} foi banido do servidor.")

    # Envia uma mensagem privada para o membro banido, informando o motivo
    if reason:
        await member.send(f"Você foi banido do servidor por: {reason}")
    else:
        await member.send("Você foi banido do servidor.")

# Comando de ajuda para mostrar todos os comandos disponíveis
@bot.command()
async def ajuda(ctx):
    help_embed = discord.Embed(title="Ajuda - Comandos Disponíveis", color=discord.Color.gold())
    help_embed.add_field(name="/ping", value="Verifica a latência do bot.")
    help_embed.add_field(name="/perfil [membro]", value="Mostra informações detalhadas de um membro.")
    help_embed.add_field(name="/avatar [membro]", value="Mostra imagem do perfil de um membro.")
    help_embed.add_field(name="/ajuda", value="Mostra esta mensagem de ajuda.")
    help_embed.add_field(name="/developer", value="Manda o link para ativar a insígnia de desenvolvedor.")
    help_embed.add_field(name="/clear [quantidade]", value="Limpa uma quantidade específica de mensagens (padrão: 20).")
    help_embed.add_field(name="/infoserver", value="Mostra informações sobre o servidor.")
    help_embed.add_field(name="/banir [membro] [motivo]", value="Bane um membro do servidor.")
    help_embed.add_field(name="/bomdia", value="Envia uma mensagem desejando bom dia!")
    help_embed.add_field(name="/boatarde", value="Envia uma mensagem desejando boa tarde!")
    help_embed.add_field(name="/boanoite", value="Envia uma mensagem desejando boa noite!")
    await ctx.send(embed=help_embed)

# Novo comando para enviar uma mensagem de bom dia
@bot.command()
async def bomdia(ctx):
    await ctx.send("Bom dia! Que seu dia seja incrível!")

# Novo comando para enviar uma mensagem de boa tarde
@bot.command()
async def boatarde(ctx):
    await ctx.send("Boa tarde!")

# Novo comando para enviar uma mensagem de boa noite
@bot.command()
async def boanoite(ctx):
    await ctx.send("Boa noite! Tenha bons sonhos!")

# Executando o bot com o token do Discord
bot.run('ADICIONE-O-TOKEN')