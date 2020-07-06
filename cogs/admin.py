from discord.ext import commands
import checks.identities
from checks.identities import is_owner
import discord

"""===IMPORTANT NOTE===

discord.py can read docstrings and extrapolate information from them, if you run this tutorial bot and execute the help
command you will see the ping command includes the brief from it's docstring. This would normally be fine but it breaks
Cog commands by making them unable to be found.

As such docstrings in Cogs will be written above the function.

"""


class AdminCog(commands.Cog, name="Admin"):
    """The Admin cog class

    This class extends commands.Cog which allows discord.py to read it and use it as intended. It will contain all of
    the commands of a given category. We can pass options into the class like with the decorators, these options are
    detailed under CogMeta:

    https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.CogMeta

    """
    def __init__(self):
        pass

    """The command group or super command

        A command group or super command. The decorator involves invoke_without_command as that extends to the use of
        sub commands, such that the super command is not run alongside a sub command.
        Checks are added with the @commands.check decorator
    """
    @commands.check(is_owner)
    @commands.group(name="admin_role", invoke_without_command=False)
    async def admin_role(self, ctx):
        # Check if role exists, if not add it and set owner as admin
        server = ctx.guild
        if not any("admin" == role.name for role in server.roles):
            """
            Important things to note when working with roles
            
            - Roles work in a hierarchy, a role would only be able to edit roles underneath it
              - This also means that a bot can't move a role above it
              - Thus the below snippet would only work if the bot's role was the first role
            - The edit function also has access to permissions, colour and mentions. Check the docs for more info
              - Do note there are two types of Permissions data classes
            """
            pos = len(server.roles) - 1
            role = await server.create_role(name="admin", reason="Auto created to fill admin cog methods")
            await role.edit(position=pos)
            await server.owner.add_roles(role, reason="Adding owner as admin")

    """A sub command of the admin_role group

        This is a sub command of the admin_role group, note that the decorator begins with the super command, but
        otherwise follows standard command decorator rules and nomenclature. Also note that the user param will act
        like a required argument. The type hinting on user will also attempt to convert the argument supplied into a
        discord.Member class, this requires the argument to be a user.
    """
    @admin_role.command(name="add")
    async def admin_role_add(self, ctx, user: discord.Member):
        # Add user to role
        old_user_roles = user.roles
        server_rolls = ctx.guild.roles
        role_admin = discord.utils.get(server_rolls, name="admin")
        new_user_rolls = old_user_roles
        new_user_rolls.append(role_admin)
        await user.edit(roles=new_user_rolls)
        await ctx.send(f"{user.display_name} added as an Admin!!")

    @admin_role.command(name="remove")
    async def admin_role_rem(self, ctx, user: discord.Member):
        # Remove user from a role
        old_user_roles = user.roles
        server_rolls = ctx.guild.roles
        role_admin = discord.utils.get(server_rolls, name="admin")
        new_user_rolls = old_user_roles
        if role_admin in new_user_rolls:
            new_user_rolls.remove(role_admin)
        await user.edit(roles=new_user_rolls)
        await ctx.send(f"{user.display_name} removed from admins, what a pleb!")

    """
        Command specific errors are created using the decorator @{command}.error, this is not error specific and any
        error can be picked up. In this instance we only account for two possible errors.
    """
    @admin_role.error
    async def admin_role_error(self, ctx, error):
        if isinstance(error, checks.identities.NotOwner):
            await ctx.channel.send("This is an owner only command")
        if isinstance(error, checks.identities.NotGuild):
            await ctx.channel.send("This is a private message, not a server")

    # Some basic checks can be added with a decorator, here's a list:
    # https://gist.github.com/Painezor/eb2519022cd2c907b56624105f94b190
    @commands.has_role("admin")
    @commands.command(name="purge")
    async def purge(self, ctx, n=5):
        await ctx.channel.purge(limit=n)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission")


def setup(bot):
    """The setup function load_extension searches for

    This function serves as a way to handle any init methods, protocols or parameters. This function should always end
    or at the very least contain bot.add_cog(Class)

    :param bot: The client that will connect to discord
    """
    bot.add_cog(AdminCog())
