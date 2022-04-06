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
    async def mapper(self, ctx, argaction, arg):

        import os
        mapper_name = arg.lower()

        def get_map_ids(name):
            map_ids = []
            for file in os.listdir(f'mappers/{name}'):
                file_read = open(f'mappers/{name}/{file}', 'r', encoding='utf-8')
                lines = file_read.readlines()

                for line in lines:
                    if 'BeatmapID:' in line:
                        map_ids.append(line[line.index(':') + 1:].strip())  # map ID
                        # EXAMPLE *** BeatmapID:2398163
                file_read.close()

            map_list = ''  # compiling into readable list
            for id in map_ids:
                map_list += f'{id}, '
            map_list = map_list[:-2]
            return map_list

        def get_correct_name(mapper_name):
            alternate_names = [] # getting alternate names
            file_name = 'alternate_mapper_names.txt'
            file_read = open(file_name, 'r')
            lines = file_read.readlines()
            for line in lines:
                mapper_usernames = line.split(' ')
                mapper_usernames[-1] = mapper_usernames[-1].strip()
                alternate_names.append(mapper_usernames)
                # print(mapper_usernames)

            for list in alternate_names: # substituting alternate mapper_name for directory mapper_name
                if mapper_name in list:
                    for name in list:
                        if name in os.listdir('mappers'):
                            mapper_name = name

            mapper_name = mapper_name.replace('*', ' ')
            return mapper_name

        mapper_name = get_correct_name(mapper_name)

        if str(ctx.author) in ADMIN: # PROTECTED !!!

            # ADDING MAPPERS

            if argaction == 'add':

                if mapper_name in os.listdir('mappers'):  # if mapper already exists in the directory

                    await ctx.send(f'That mapper already exists in the directory. Map IDs: {get_map_ids(mapper_name)}')

                else: # add directory

                    os.mkdir(f'mappers/{mapper_name}')
                    await ctx.send(f'Directory created for {mapper_name}.')

            # REMOVING MAPPERS

            elif argaction == 'remove':

                if mapper_name not in os.listdir('mappers'):  # if mapper doesn't exist in the directory

                    await ctx.send(f'That mapper does not exist in the directory.')

                else:

                    import shutil
                    map_ids = get_map_ids(mapper_name)
                    shutil.copytree(f'mappers/{mapper_name}', f'mappers_deleted/{mapper_name}')
                    shutil.rmtree(f'mappers/{mapper_name}')
                    await ctx.send(f'Migrated {map_ids}')

            # REVIVING MAPPERS

            elif argaction == 'revive':

                if mapper_name not in os.listdir('mappers_deleted'):  # if mapper doesn't exist in the directory

                    await ctx.send(f'That mapper does not exist in the deleted mappers directory.')

                else:

                    import shutil
                    shutil.copytree(f'mappers_deleted/{mapper_name}', f'mappers/{mapper_name}')
                    shutil.rmtree(f'mappers_deleted/{mapper_name}')
                    await ctx.send(f'Revived maps by {mapper_name}.')

        # LISTING MAPS

        if argaction == 'list':

            if mapper_name not in os.listdir('mappers'):

                await ctx.send(f'No maps found for {mapper_name}.')

            else:

                await ctx.send(f'Map IDs for {mapper_name}: {get_map_ids(mapper_name)}')

def setup(client):
    client.add_cog(mapper(client))
