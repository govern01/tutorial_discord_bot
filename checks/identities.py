"""

Checks are little snippets of code that ensure the context of the message is able to run, whether it be permissions
roles or validating arguments (having an argument between x and y values for example).
Checks run before the code executes and act as a gate of sorts, a function won't even be touched unless the checks are
passed.

"""


def is_owner(ctx):
    if ctx.guild is None:
        return False
    author_id = ctx.author.id
    owner_id = ctx.guild.owner_id
    return author_id == owner_id
