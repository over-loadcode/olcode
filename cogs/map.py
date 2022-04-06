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
    async def map(self, ctx, argaction, argname, argid):

        if str(ctx.author) in ADMIN:

            import os
            mapper_name = argname

            def get_map_ids(name, directory):
                map_ids = []
                for file in os.listdir(f'{directory}/{name}'):
                    file_read = open(f'{directory}/{name}/{file}', 'r', encoding='utf-8')
                    lines = file_read.readlines()

                    for line in lines:
                        if 'BeatmapID:' in line:
                            map_ids.append(line[line.index(':') + 1:].strip())  # map ID
                            # EXAMPLE *** BeatmapID:2398163
                    file_read.close()

                return map_ids

                # map_list = ''  # compiling into readable list
                # for id in map_ids:
                #     map_list += f'{id}, '
                # map_list = map_list[:-2]
                # return map_list

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
            map_id = argid
            mapper_ids = get_map_ids(mapper_name, 'mappers')

            # REMOVING MAPS

            if argaction == 'remove':

                print(mapper_ids)
                if map_id in mapper_ids:

                    import os
                    import shutil

                    mapper_directory = f'mappers/{mapper_name}'
                    print(os.listdir(mapper_directory))
                    map_filename = os.listdir(mapper_directory)[mapper_ids.index(map_id)]
                    if mapper_name not in os.listdir('mappers_deleted'):
                        os.mkdir(f'mappers_deleted/{mapper_name}')

                    shutil.copyfile(f'mappers/{mapper_name}/{map_filename}', f'mappers_deleted/{mapper_name}/{map_filename}')
                    os.remove(f'mappers/{mapper_name}/{map_filename}')
                    await ctx.send(f'Migrated ID {map_id}.')

                else:

                    await ctx.send(f'Map ID {map_id} not found for {mapper_name}.')

            # REVIVING MAPS

            elif argaction == 'revive':

                mapper_ids = get_map_ids(mapper_name, 'mappers_deleted')

                if map_id in mapper_ids:

                    import os
                    import shutil

                    mapper_directory = f'mappers_deleted/{mapper_name}'
                    map_filename = os.listdir(mapper_directory)[mapper_ids.index(map_id)]

                    shutil.copyfile(f'mappers_deleted/{mapper_name}/{map_filename}', f'mappers/{mapper_name}/{map_filename}')
                    os.remove(f'mappers_deleted/{mapper_name}/{map_filename}')
                    await ctx.send(f'Revived ID {map_id}.')

                else:

                    await ctx.send(f'Map ID {map_id} not found for {mapper_name}.')

            # ADDING MAPS

            elif argaction == 'add':

                if map_id in mapper_ids:

                    await ctx.send(f'ID {map_id} already exists for {mapper_name}.')

                elif mapper_name not in os.listdir('mappers'):

                    await ctx.send(f'Mapper {mapper_name} does not exist. Please create a directory with the command \'mapper add [name].')

                else:

                    url = f'https://osu.ppy.sh/osu/{map_id}'
                    filename = f'{map_id}.txt'
                    file_path = f'mappers/{mapper_name}/{map_id}.txt'

                    import requests
                    r = requests.get(url, stream=True)
                    if r.ok:
                        print("saving to", os.path.abspath(file_path))
                        with open(file_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024 * 8):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                                    os.fsync(f.fileno())
                    else:  # HTTP status code 4XX/5XX
                        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

                    file_read = open(file_path, 'r', encoding='utf-8')
                    lines = file_read.readlines()

                    map_artist = ''
                    map_title = ''
                    for line in lines:
                        if 'Artist:' in line:
                            map_artist = line[line.index(':') + 1:].strip()  # artist
                        if 'Title:' in line:
                            map_title = line[line.index(':') + 1:].strip()  # title
                    file_read.close()

                    await ctx.send(f'Map ID {map_id} added for {mapper_name}: {map_artist} - {map_title}')

            elif argaction == 'addseveral':

                map_id = argid

                if not ',' in map_id:

                    await ctx.send('The map IDs argument does not have a comma. Syntax: [id1],[id2],[id3]')

                else:

                    if mapper_name not in os.listdir('mappers'):

                        await ctx.send(f'Mapper {mapper_name} does not exist. Please create a directory with the command \'mapper add [name].')

                    else:

                        map_id = map_id.split(',')

                        for map in map_id:

                            if map in mapper_ids:

                                map_id.remove(map)

                            else:

                                url = f'https://osu.ppy.sh/osu/{map}'
                                filename = f'{map}.txt'
                                file_path = f'mappers/{mapper_name}/{map}.txt'

                                import requests
                                r = requests.get(url, stream=True)
                                if r.ok:
                                    print("saving to", os.path.abspath(file_path))
                                    with open(file_path, 'wb') as f:
                                        for chunk in r.iter_content(chunk_size=1024 * 8):
                                            if chunk:
                                                f.write(chunk)
                                                f.flush()
                                                os.fsync(f.fileno())
                                else:  # HTTP status code 4XX/5XX
                                    print("Download failed: status code {}\n{}".format(r.status_code, r.text))

                                file_read = open(file_path, 'r', encoding='utf-8')
                                lines = file_read.readlines()

                                map_artist = ''
                                map_title = ''
                                for line in lines:
                                    if 'Artist:' in line:
                                        map_artist = line[line.index(':') + 1:].strip()  # artist
                                    if 'Title:' in line:
                                        map_title = line[line.index(':') + 1:].strip()  # title
                                file_read.close()

                                await ctx.send(f'Map ID {map} added for {mapper_name}: {map_artist} - {map_title}')

def setup(client):
    client.add_cog(mapper(client))
