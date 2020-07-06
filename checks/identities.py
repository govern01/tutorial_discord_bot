from discord.ext import commands
"""

Checks are little snippets of code that ensure the context of the message is able to run, whether it be permissions
roles or validating arguments (having an argument between x and y values for example).
Checks run before the code executes and act as a gate of sorts, a function won't even be touched unless the checks are
passed.

"""


# Error classes should extend the CheckFailure class in order to be handled, this is only if the error would occur in a
# check
class NotGuild(commands.CheckFailure):
    pass


class NotOwner(commands.CheckFailure):
    pass


# We changed the return False to raise errors as that way we can tell the user why the command didn't run
def is_owner(ctx):
    if ctx.guild is None:
        raise NotGuild("This aint a guild")
    author_id = ctx.author.id
    owner_id = ctx.guild.owner_id
    author_is_owner = author_id == owner_id
    if not author_is_owner:
        raise NotOwner("You aren't the guild owner")
    else:
        return author_is_owner
