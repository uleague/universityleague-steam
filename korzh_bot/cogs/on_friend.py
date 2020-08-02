from steam.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Подробнее про бота")
    async def about(self, ctx):
        await ctx.send(
            """
Данный бот помогает делать киберспорт лучше. 

universityleague.ru
        """
        )


def setup(bot):
    bot.add_cog(Basic(bot))
