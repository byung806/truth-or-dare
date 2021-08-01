import json

import discord
from random import choice
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Bulkadd(commands.Cog):
    '''
    Add a custom question in your server.
    Usage:
    `<prefix> add <truth | dare | wyr> <pg | pg13 | r> <question>`
    `<prefix> add wyr <pg | pg13 | r> <choice1>, <choice2>, ...` (2-5 choices)
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['multiadd', 'addmulti', 'multipleadd', 'addmultiple'])
    @commands.guild_only()
    async def bulkadd(self, ctx, question_type, category, *, questions):
        if ctx.author.id != 461345173314732052:
            return
        question_type = question_type.lower()
        category = category.lower()
        async with ctx.typing():
            if not category:
                default_category = json.load(open('data\\default_category.json', 'r'))
                if str(ctx.guild.id) in default_category:
                    category = default_category[str(ctx.guild.id)]
                else:
                    category = 'pg'

            questions = list(map(lambda x: x.lower().capitalize().replace(' u ', ' you '), questions.split('\n')))
            if question_type in ['truth', 't', 'truths']:
                location = 'data\\questions\\truths.json'
                data = json.load(open(location, 'r'))
                question_type = 'truth'
            elif question_type in ['dare', 'd', 'dares']:
                location = 'data\\questions\\dares.json'
                data = json.load(open(location, 'r'))
                question_type = 'dare'
            elif question_type in ['wyr', 'wouldyourather']:
                location = 'data\\questions\\wyrs.json'
                data = json.load(open(location, 'r'))
                question_type = 'wyr'

            if category in ['pg', 'pg13', 'r']:
                dupes = 0
                #if str(ctx.guild.id) in data:
                for question in questions:
                    if question in data[category]:
                        dupes += 1
                    else:
                        data[category].append(question)
                data[category] = list(set(data[category]))
            else:
                await send_embed(ctx, 'Invalid category', f'Use {await get_server_prefix(self.bot, ctx)}bulkadd '
                                                          f'<truth | dare | wyr> <pg | pg13 | r> <questions>'
                                                          f'\n(where each question is on a new line)')
                return

        json_data = json.dumps(data)
        f = open(location, 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, f'Added {len(questions)-dupes} {question_type} questions (Category: {category})',
                         f'{len(questions)-dupes} questions ({dupes} duplicates)'
                         f' were added to the list of {question_type} questions.')


    @bulkadd.error
    async def bulkadd_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await send_embed(ctx, 'Invalid usage', f'Use {await get_server_prefix(self.bot, ctx)}bulkadd '
                                                   f'<truth | dare | wyr> <pg | pg13 | r> <questions>'
                                                   f'\n(where each question is on a new line)')
        else:
            raise error

def setup(bot):
    bot.add_cog(Bulkadd(bot))