from discord.ext import commands

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
    """
    @commands.group(name="admin_role", invoke_without_command=True)
    async def admin_role(self, ctx):
        await ctx.channel.send("Add/Remove an admin.")

    """A sub command of the admin_role group

        This is a sub command of the admin_role group, note that the decorator begins with the super command, but
        otherwise follows standard command decorator rules and nomenclature. Also note that the name param will act
        like a required argument.
    """
    @admin_role.command(name="add")
    async def role_add(self, ctx, name):
        await ctx.send(f"{name} added as an Admin!!")

    @admin_role.command(name="remove")
    async def role_rem(self, ctx, name):
        await ctx.send(f"{name} removed from admins, what a pleb!")


def setup(bot):
    """The setup function load_extension searches for

    This function serves as a way to handle any init methods, protocols or parameters. This function should always end
    or at the very least contain bot.add_cog(Class)

    :param bot: The client that will connect to discord
    """
    bot.add_cog(AdminCog())
