import discord
from discord.ext import commands
cooldown = False
ADMIN = ['over_loadcode#5428','Fisky#2013','`Ralkinson#0293','Pseudonym#1381']

class mapper(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog ready')

    @commands.command()
    async def name(self, ctx, argaction, argname, argnewname=None):

        if str(ctx.author) in ADMIN:

            # LISTING NAMES

            if argaction == 'list':

                file_read = open('alternate_mapper_names.txt', 'r')
                lines = file_read.readlines()

                names = ''
                for line in lines:
                    if argname in line.split(' '):
                        names = line

                if names == '':
                    await ctx.send(f'No names found for {argname}.')
                else:
                    await ctx.send(f'{names} Asterisks represent spaces.')

                file_read.close()

            if argaction == 'add':

                file_read = open('alternate_mapper_names.txt', 'r')
                lines = file_read.readlines()

                name_idx = 0
                for line in lines:
                    if argname in line.split(' '):
                        break
                    name_idx += 1

                if name_idx == len(lines): # name not in file

                    file_read.close()

                    file_read = open('alternate_mapper_names.txt', 'a')
                    file_read.write(f'\n{argname} {argnewname}')

                    await ctx.send(f'New assignment added for {argname} to {argnewname}.')

                else:

                    if argnewname not in lines[name_idx]:

                        file_read.close()

                        lines[name_idx] = lines[name_idx].strip()
                        lines[name_idx] += f' {argnewname}\n'

                        file_read = open('alternate_mapper_names.txt', 'w')

                        for item in lines:
                            file_read.write(item)

                        await ctx.send(f'Name {argnewname} added for {argname}.')

                    else:

                        await ctx.send(f'Name {argname} already has alternate name {argnewname}.')

def setup(client):
    client.add_cog(mapper(client))
