import discord
from discord.ext import commands
cooldown = False

class mapper(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        import os
        global cooldown
        if message.author == self.client.user:
            return

        msg = str.lower(message.content).split(' ')
        idx = -1
        for string in msg:
            idx += 1
            if string == '':
                msg.pop(idx)
        # alternate_names = [['olc', 'loadcode', 'over_loadcode'], ['nihil', 'raiko', 'nhlx', 'raikozen'], ['rrtyui', 'ratatouille', 'rttyui'], ['bobbyperson', 'austin', 'austin12100', 'bobby']]

        alternate_names = []
        file_name = 'alternate_mapper_names.txt'
        file_read = open(file_name, 'r')
        lines = file_read.readlines()
        for line in lines:
            mapper_usernames = line.split(' ')
            for name in mapper_usernames:
                mapper_usernames[mapper_usernames.index(name)] = name.replace('*', ' ')
            mapper_usernames[-1] = mapper_usernames[-1].strip()
            alternate_names.append(mapper_usernames)
            # print(mapper_usernames)

        mapper_name = None
        if len(msg) == 2:
            mapper_name = msg[0]
        if len(msg) == 3:
            mapper_name = msg[0] + ' ' + msg[1]

        if not mapper_name is None and msg[-1] == 'pattern' and not cooldown:
            # print(mapper_name)
            for list in alternate_names:
                if mapper_name in list:
                    for name in list:
                        if name in os.listdir('mappers'):
                            mapper_name = name

            import random
            if mapper_name == 'random':
                mapper_name = random.choice(os.listdir('mappers'))

            if not mapper_name in os.listdir('mappers'):
                await message.channel.send(f'No patterns found from {mapper_name}. Use command \'mappers to see which mappers are supported.')
            elif os.listdir(f'mappers/{mapper_name}/') == []:
                await message.channel.send(f'No patterns found from {mapper_name} folder. olc killed this one.')
            else:
                cooldown = True

                # map rendering algorithm
                # map rendering algorithm
                # map rendering algorithm

                if True:
                    import PIL
                    from PIL import Image, ImageDraw, ImageFont
                    import math
                    import os

                    file_name = f'mappers/{mapper_name}/' + random.choice(os.listdir(f'mappers/{mapper_name}'))
                    print(os.listdir(f'mappers/{mapper_name}'))
                    NUMBER_OF_OBJECTS = random.randint(5,8)
                    POINT_SENSITIVITY = 5  # number of pixels between separate circles in slider rendering
                    STACK_DISTANCE = 3  # in pixels
                    SLIDERBORDER_WIDTH = 1  # applies on each side so it's multiplied by 2 when modifying stroke

                    fnt = ImageFont.truetype('Inter-Regular.ttf', 20)

                    def node_to_xy(list):  # converts nodes in osu format (ex. '100:100') to lists (ex. [100, 100])
                        idx = -1
                        for node in list:
                            idx += 1
                            node = node.split(':')
                            node[0] = int(node[0])
                            node[1] = int(node[1])
                            list[idx] = node

                    def get_angle(x0, y0, x1, y1):  # returns the angle between two points
                        return math.atan2(y1 - y0, x1 - x0)

                    def draw_sliderend(x, y, is_sliderbody):
                        if is_sliderbody:
                            draw.ellipse((x - cs_px + SLIDERBORDER_WIDTH, y - cs_px + SLIDERBORDER_WIDTH,
                                          x + cs_px - SLIDERBORDER_WIDTH, y + cs_px - SLIDERBORDER_WIDTH), fill='gray')
                        if not is_sliderbody:
                            draw.ellipse((x - cs_px, y - cs_px, x + cs_px, y + cs_px), fill='black')

                    def draw_hitcircle(x, y):
                        draw.ellipse((x - cs_px, y - cs_px, x + cs_px, y + cs_px), fill='white', outline='black')

                    def add_angle(x, y, dir, mag):
                        a = int(float(x) + float(mag) * math.cos(dir))
                        b = int(float(y) + float(mag) * math.sin(dir))
                        return [a, b]

                    def find_distance(x0, y0, x1, y1):
                        return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

                    # MAP INFO

                    enc = 'utf-8'
                    file_read = open(file_name, 'r', encoding=enc)
                    lines = file_read.readlines()

                    map_cs = -1.0  # negative because 0.0 is possible
                    info_title = ''
                    info_artist = ''
                    info_mapper = ''
                    for line in lines:
                        if 'CircleSize:' in line:
                            map_cs = float(line[line.index(':') + 1:-1])  # grab CS number
                            # EXAMPLE *** CircleSize:4.3
                        if 'Title:' in line:
                            info_title = line[line.index(':') + 1:].strip()
                        if 'Artist:' in line:
                            info_artist = line[line.index(':') + 1:].strip()
                        if 'Creator:' in line:
                            info_mapper = line[line.index(':') + 1:].strip()

                    if map_cs == -1.0:
                        print('CS of map not found')
                    else:
                        print(f'Circle size of map: {map_cs}')

                    # ** FINDING OBJECTS **

                    # finding line '[HitObjects]' that marks the start of the objects in the .osu file
                    objects_start_line = 0
                    for line in lines:
                        objects_start_line += 1
                        # print(f'im going {objects_start_line}')
                        if '[HitObjects]' in line:
                            break

                    print(f'Beginning line: {objects_start_line}')
                    print(f'Ending line: {len(lines)}')

                    # getting randomized object
                    def get_objects():

                        # randomizing
                        objects_rand_start = random.randint(objects_start_line + 1, len(lines) - NUMBER_OF_OBJECTS - 1)
                        objects = lines[int(objects_rand_start):int(objects_rand_start + NUMBER_OF_OBJECTS)]
                        print(objects)
                        if int(objects[-1].split(',')[2]) - int(objects[0].split(',')[2]) > 1000 * NUMBER_OF_OBJECTS:
                            get_objects()
                        return objects  # returns a list of the .osu data of each object

                    objects = get_objects()

                    # ** DRAWING OBJECTS **

                    objects_original = objects
                    objects.reverse()  # so that earlier objects render on top of later ones
                    map = Image.open('template.png')
                    draw = ImageDraw.Draw(map)

                    # bezier formula that i stole
                    def make_bezier(xys):
                        # xys should be a sequence of 2-tuples (Bezier control points)
                        n = len(xys)
                        combinations = pascal_row(n - 1)

                        def bezier(ts):
                            # This uses the generalized formula for bezier curves
                            # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
                            result = []
                            for t in ts:
                                tpowers = (t ** i for i in range(n))
                                upowers = reversed([(1 - t) ** i for i in range(n)])
                                coefs = [c * a * b for c, a, b in zip(combinations, tpowers, upowers)]
                                result.append(tuple(sum([coef * p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
                            return result

                        return bezier

                    def pascal_row(n, memo={}):
                        # This returns the nth row of Pascal's Triangle
                        if n in memo:
                            return memo[n]
                        result = [1]
                        x, numerator = 1, n
                        for denominator in range(1, n // 2 + 1):
                            # print(numerator,denominator,x)
                            x *= numerator
                            x /= denominator
                            result.append(x)
                            numerator -= 1
                        if n & 1 == 0:
                            # n is even
                            result.extend(reversed(result[:-1]))
                        else:
                            result.extend(reversed(result))
                        memo[n] = result
                        return result

                    previous_hitcircles = []
                    xys_full = []
                    for circle in objects:
                        stack = False
                        cs_px = int(math.floor((109 - 9 * map_cs) / 2.50))  # circle size in osu pixels
                        circle_x = int(circle.split(',')[
                                           0]) + 72  # "playfield" in template.png is 72px from the left and 48px from the right to mirror 4:3 resolution ingame
                        circle_y = int(circle.split(',')[1]) + 48
                        if [circle_x, circle_y] in previous_hitcircles:
                            circle_x -= STACK_DISTANCE
                            circle_y -= STACK_DISTANCE
                            stack = True
                        draw.ellipse((circle_x - cs_px, circle_y - cs_px, circle_x + cs_px, circle_y + cs_px), fill='white',
                                     outline='black')  # drawing circle with radius cs_px
                        previous_hitcircles.append([circle_x, circle_y])

                        if '|' in circle:  # indicates a slider
                            # filtering slider info
                            xys_full = circle.split(',')[5]
                            xys_full = xys_full.split('|')[1:]
                            # print(xys_full)

                            node_to_xy(xys_full)
                            # print(xys_full)

                            slider_length = float(circle.split(',')[7])

                            if 'L' in circle:  # linear slider
                                linear_x = xys_full[0][0] + 72  # xys_full for linear slider: [[x1, y1]]
                                linear_y = xys_full[0][1] + 48

                                if stack:
                                    linear_x -= STACK_DISTANCE
                                    linear_y -= STACK_DISTANCE
                                previous_hitcircles.append([linear_x, linear_y])

                                slider_angle = get_angle(circle_x, circle_y, linear_x,
                                                         linear_y)  # move slider_length at slider_angle
                                linear_x = add_angle(circle_x, circle_y, slider_angle, slider_length)[0]
                                linear_y = add_angle(circle_x, circle_y, slider_angle, slider_length)[1]
                                draw.line((circle_x, circle_y, linear_x, linear_y), fill='black',
                                          width=cs_px * 2)  # sliderborder
                                draw_sliderend(linear_x, linear_y, False)
                                draw.line((circle_x, circle_y, linear_x, linear_y), fill='gray',
                                          width=cs_px * 2 - SLIDERBORDER_WIDTH * 2)  # sliderbody
                                draw_sliderend(linear_x, linear_y, True)
                                draw_hitcircle(circle_x, circle_y)
                            if 'P' in circle:
                                # xys_full for perfect curve slider: [[x1, y1], [x2, y2]]
                                # if stack:
                                #     xys_full -= [[STACK_DISTANCE, STACK_DISTANCE], [STACK_DISTANCE, STACK_DISTANCE]]
                                a = [circle_x, circle_y]  # finding center of curve
                                b = [xys_full[0][0] + 72, xys_full[0][1] + 48]
                                c = [xys_full[1][0] + 72, xys_full[1][1] + 48]

                                aSq = (c[0] - b[0]) ** 2 + (c[1] - b[1]) ** 2
                                bSq = (c[0] - a[0]) ** 2 + (c[1] - a[1]) ** 2
                                cSq = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

                                s = aSq * (bSq + cSq - aSq)
                                t = bSq * (aSq + cSq - bSq)
                                u = cSq * (aSq + bSq - cSq)
                                sum_ = s + t + u

                                if sum_ != 0:
                                    center_x = (s * a[0] + t * b[0] + u * c[0]) / sum_
                                    center_y = (s * a[1] + t * b[1] + u * c[1]) / sum_

                                    radius = int(
                                        math.sqrt((center_x - circle_x) ** 2 + (center_y - circle_y) ** 2))  # pythagorean theorem
                                    # print(f'{center_x},{center_y},{radius}')
                                    # draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline='red') # ellipse curve guide

                                    dA = [a[0] - center_x, a[1] - center_y]
                                    dC = [c[0] - center_x, c[1] - center_y]

                                    thetaStart = math.atan2(dA[1], dA[0])
                                    thetaEnd = math.atan2(dC[1], dC[0])

                                    while thetaEnd < thetaStart:
                                        thetaEnd += 2 * math.pi

                                    dir = 1
                                    thetaRange = thetaEnd - thetaStart

                                    orthoAtoC = [c[0] - a[0], c[1] - a[1]]
                                    orthoAtoC = [orthoAtoC[1], -orthoAtoC[0]]

                                    bMinusA = [b[0] - a[0], b[1] - a[1]]

                                    # perfect_end = add_angle(center_x, center_y, thetaStart + thetaRange, radius)
                                    # draw_sliderend(perfect_end[0], perfect_end[1])

                                    if orthoAtoC[0] * bMinusA[0] + orthoAtoC[1] * bMinusA[1] < 0:
                                        dir = -dir
                                        thetaRange = 2 * math.pi - thetaRange

                                    amount_points = math.floor(slider_length / POINT_SENSITIVITY)

                                    for sliderbody_toggle in range(2):
                                        slider_length_drawn = 0
                                        curve_points = []
                                        for x in range(amount_points):
                                            fract = x / (amount_points - 1)
                                            theta = thetaStart + dir * fract * thetaRange
                                            draw_sliderend(center_x + radius * math.cos(theta), center_y + radius * math.sin(theta),
                                                           bool(sliderbody_toggle))

                                            curve_points.append(
                                                [center_x + radius * math.cos(theta), center_y + radius * math.sin(theta)])
                                            if len(curve_points) != 1:
                                                slider_length_drawn += find_distance(curve_points[-1][0], curve_points[-1][1],
                                                                                     curve_points[-2][0], curve_points[-2][1])
                                            if slider_length_drawn >= slider_length:
                                                previous_hitcircles.append([math.floor(center_x + radius * math.cos(theta)),
                                                                            math.floor(center_y + radius * math.sin(theta))])
                                                break

                                draw_hitcircle(circle_x, circle_y)
                            if 'B' in circle:
                                # xys_full for bezier slider: [[x1, y1], [x2, y2], [x3, y3], [x3, y3], [x4, y4]]
                                if stack:
                                    for coord in xys_full:
                                        xys_full[xys_full.index(coord)][0] -= STACK_DISTANCE
                                        xys_full[xys_full.index(coord)][1] -= STACK_DISTANCE
                                ts = [t / 99.0 for t in range(100)]  # 100 individual points per curved segment

                                for item in xys_full:  # add values for position correction
                                    item[0] = item[0]
                                    item[1] = item[1]

                                if not circle_x == xys_full[0][0] or not circle_y == xys_full[0][
                                    1]:  # fix red tick on first tick:
                                    xys_full.insert(0, [circle_x - 72, circle_y - 48])
                                if xys_full[-1] == xys_full[-2]:
                                    xys_full.pop()  # fix red tick at the end of slider

                                red_ticks = []  # get indexes of red ticks (duplicate ticks, where the second one is the index)
                                item_idx = -1
                                for item in xys_full:
                                    item_idx += 1
                                    if xys_full[item_idx] == xys_full[item_idx - 1]:
                                        red_ticks.append(item_idx)

                                for sliderbody_toggle in range(2):
                                    draw_idx = 0
                                    slider_length_drawn = 0
                                    for index in red_ticks:  # repeat for each segment
                                        xys = xys_full[
                                              draw_idx:index]  # sets xys to the start, bezier points, and end of segment
                                        draw_idx = index
                                        if len(xys) == 2:  # linear segments
                                            if sliderbody_toggle == 0:
                                                draw.line((xys[0][0] + 72, xys[0][1] + 48, xys[1][0] + 72, xys[1][1] + 48),
                                                          fill='black',
                                                          width=cs_px * 2)
                                            if sliderbody_toggle == 1:
                                                draw.line((xys[0][0] + 72, xys[0][1] + 48, xys[1][0] + 72, xys[1][1] + 48),
                                                          fill='gray',
                                                          width=cs_px * 2 - (SLIDERBORDER_WIDTH * 2 + 1))
                                            draw_sliderend(xys[1][0] + 72, xys[1][1] + 48, bool(sliderbody_toggle))
                                            slider_length_drawn += find_distance(xys[0][0], xys[0][1], xys[1][0], xys[1][1])
                                        if len(xys) > 2:  # bezier curves
                                            bezier = make_bezier(xys)
                                            points = bezier(ts)
                                            idx = -1
                                            for point in points:
                                                draw_sliderend(point[0] + 72, point[1] + 48, bool(sliderbody_toggle))
                                                a = points.index(point)
                                                if a + 1 < len(points):
                                                    slider_length_drawn += find_distance(point[0], point[1], points[a + 1][0],
                                                                                         points[a + 1][
                                                                                             1])  # gets distance between each point in bezier

                                    xys = xys_full[draw_idx:]
                                    # print(xys)
                                    if len(xys) == 2:  # linear segment
                                        slider_angle = get_angle(xys[0][0], xys[0][1], xys[1][0],
                                                                 xys[1][1])  # move slider_length at slider_angle
                                        sliderend_x_real = \
                                        add_angle(xys[0][0], xys[0][1], slider_angle, slider_length - slider_length_drawn)[
                                            0]  # sliderend x position adjusted for real length
                                        sliderend_y_real = \
                                        add_angle(xys[0][0], xys[0][1], slider_angle, slider_length - slider_length_drawn)[
                                            1]  # sliderend y position adjusted for real length
                                        xys[1][0] = sliderend_x_real
                                        xys[1][1] = sliderend_y_real
                                        if sliderbody_toggle == 0:
                                            draw.line((xys[0][0] + 72, xys[0][1] + 48, xys[1][0] + 72, xys[1][1] + 48),
                                                      fill='black',
                                                      width=cs_px * 2)
                                        if sliderbody_toggle == 1:
                                            draw.line((xys[0][0] + 72, xys[0][1] + 48, xys[1][0] + 72, xys[1][1] + 48),
                                                      fill='gray',
                                                      width=cs_px * 2 - SLIDERBORDER_WIDTH * 2)
                                        draw_sliderend(xys[1][0] + 72, xys[1][1] + 48, bool(sliderbody_toggle))
                                    if len(xys) > 2:  # bezier curve
                                        bezier = make_bezier(xys)
                                        points = bezier(ts)
                                        idx = -1
                                        for point in points:
                                            draw_sliderend(point[0] + 72, point[1] + 48, bool(sliderbody_toggle))
                                            a = points.index(point)
                                            if a + 1 < len(points):
                                                slider_length_drawn += find_distance(point[0], point[1], points[a + 1][0],
                                                                                     points[a + 1][
                                                                                         1])  # gets distance between each point in bezier
                                            if slider_length_drawn > slider_length:  # correct for slider being shorter than nodes imply
                                                previous_hitcircles.append([math.floor(point[0]), math.floor(point[1])])
                                                break

                                draw_hitcircle(circle_x, circle_y)
                                # print(f'LENGTH!: {slider_length_drawn} VS REAL LENGTH!: {slider_length}')

                        draw.text((circle_x, circle_y), str(NUMBER_OF_OBJECTS - objects.index(circle)), font=fnt, fill='black',
                                  anchor='mm')

                    # TIMESTAMP

                    timestamp_minute = math.floor(int(objects[-1].split(',')[2]) / 60000)
                    timestamp_second = math.floor(int(objects[-1].split(',')[2]) / 1000) % 60
                    timestamp_millisecond = int(objects[-1].split(',')[2]) % 1000

                    timestamp_second = str(timestamp_second)
                    timestamp_millisecond = str(timestamp_millisecond)
                    if len(timestamp_second) == 1:
                        timestamp_second = '0' + timestamp_second
                    if len(timestamp_millisecond) == 1:
                        timestamp_millisecond = '0' + timestamp_millisecond

                    timestamp = f'{timestamp_minute}:{timestamp_second}:{timestamp_millisecond}'

                    draw.text((10, 10), f'{timestamp} {info_artist} - {info_title} by {info_mapper}', font=fnt, fill='black')

                    print(f'{timestamp} {info_artist} - {info_title} by {info_mapper}')
                    map.save('map.png')
                    # map.show()

                    file_read.close()

                # map rendering algorithm
                # map rendering algorithm
                # map rendering algorithm

                file = discord.File("map.png")
                await message.channel.send(file=file, content="")
                cooldown = False



def setup(client):
    client.add_cog(mapper(client))