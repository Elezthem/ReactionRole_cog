import nextcord
from nextcord.ext import commands

class ReactionRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_role_data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Бот {self.bot.user} запущен')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        data = self.reaction_role_data.get(payload.message_id)
        if data and payload.emoji.name == data['emoji']:
            guild = nextcord.utils.get(self.bot.guilds, id=payload.guild_id)
            role = nextcord.utils.get(guild.roles, id=data['role_id'])

            if role is not None:
                member = guild.get_member(payload.user_id)
                await member.add_roles(role)
                print(f'Роль {role.name} выдана пользователю {member.name}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        data = self.reaction_role_data.get(payload.message_id)
        if data and payload.emoji.name == data['emoji']:
            guild = nextcord.utils.get(self.bot.guilds, id=payload.guild_id)
            role = nextcord.utils.get(guild.roles, id=data['role_id'])

            if role is not None:
                member = guild.get_member(payload.user_id)
                await member.remove_roles(role)
                print(f'Role {role.name} deleted from the user {member.name}')

    @commands.command()
    async def reactionrole(self, ctx, channel: nextcord.TextChannel, message_id: int, emoji, role: nextcord.Role):
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emoji)

        self.reaction_role_data[message.id] = {
            'emoji': emoji,
            'role_id': role.id
        }

        await ctx.send(f'Reaction {emoji} was added to the message with ID {message.id}. When pressed, the role will be given {role.name}.')

def setup(bot):
    bot.add_cog(ReactionRoleCog(bot))
