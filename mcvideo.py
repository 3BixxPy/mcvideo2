from os import listdir, path
from time import perf_counter
import cv2
from PIL import Image
from numpy import array, sqrt, amin, where, sum
from extras import block_palette, falling, transparent, glowing, generate_datapack, make_frames, calculate_average_time
import argparse


# checks existence of set path
def dir_path(string):
    if path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


# checks existence of set video
def video_path(string):
    if path.isfile(string):
        return string
    else:
        raise FileNotFoundError


class InvalidBlockTypes(Exception):
    pass


# checks existence of set block types
def block_types(string):
    if string in ["glowing", "transparent", "falling"]:
        return string
    else:
        print("invalid block type: use glowing transparent falling")
        raise InvalidBlockTypes


# checks existence of resampling filter
def resampling_filter(string):
    if string in ["nearest", "bicubic", "bilinear"]:
        return string
    else:
        print("invalid resampling filter: nearest bicubic bilinear")
        raise InvalidBlockTypes


# argument stuff

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")
mcvideo = subparser.add_parser("mcvideo")
framegen = subparser.add_parser("framegen")

mcvideo.add_argument("path", type=dir_path, help=r"path to your video frames, use: C:\example\Video_Frames")
mcvideo.add_argument("resolution", type=int, help="select your resolution, the recommended resolution is blow 100, "
                                                  "use: number")
mcvideo.add_argument("--blocktypes", nargs="+", type=block_types, help="chooses which blocks to include, use: glowing "
                                                                       "/ transparent / falling, you can use more than one")
mcvideo.add_argument("--showframes", type=bool, help="show current frame in window, use: true/false")
mcvideo.add_argument("--resample", type=resampling_filter, help="can yield better results try to play with this, "
                                                                "usage: nearest or bicubic or bilinear") 
framegen.add_argument("path", type=video_path, help=r"path to your video, use: C:\example\Video.mp4")
args = parser.parse_args()

# dont change duh
resolution = 0
directory = ""
show_frames = False
NEAREST = False
BICUBIC = False
BILINEAR = False
if args.command == "mcvideo":

    directory = args.path
    resolution = args.resolution

    if args.blocktypes:
        for argument in args.blocktypes:
            if argument == "glowing":
                block_palette.update(glowing)
            elif argument == "transparent":
                block_palette.update(transparent)
            elif argument == "falling":
                block_palette.update(falling)
    
    if args.resample:
        if args.resample == "nearest":
            NEAREST = True
        if args.resample == "bilinear":
            BILINEAR = True
        if args.resample == "bicubic":
            BICUBIC = True
                
    if args.showframes:
        show_frames = args.showframes

# if generating frames
elif args.command == "framegen":
    print("generating frames")
    make_frames(args.path)
    exit()

# convert block_palette dictionary to a list of lists
_ = list(block_palette.keys())
palette = []
for tup in _:
    r, g, b = tup
    palette.append([r, g, b])


# finds the closest rgb value
def closest(colors, color):
    colors = array(colors)
    color = array(color)
    distances = sqrt(sum((colors - color) ** 2, axis=1))
    index_of_smallest = where(distances == amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance.tolist()[0]


# resizes the image
def resize(im, new_width, im_x, im_y):
    ratio = im_y / im_x
    new_height = int(new_width * ratio)
    if NEAREST:
        result = im.resize((new_width, new_height), resample=Image.NEAREST)
    elif BICUBIC:
        result = im.resize((new_width, new_height), resample=Image.BICUBIC)
    else:
        result = im.resize((new_width, new_height), resample=Image.BILINEAR)
    return result


# generates a blank datapack in datapack_output
pack_name = generate_datapack()


# generates all the mcfunctions based on input
def generate_mcfunction(frame_, commands_, tick_command_):
    # frame_functions
    with open(fr"datapack_output\{pack_name}\mcvideo2_{pack_name}\data\mcvideo_stuff{pack_name}\functions\frame_functions\{frame_}.mcfunction",
              "w") as f:
        f.write(commands_)
        f.close()
    # tick2
    with open(fr"datapack_output\{pack_name}\mcvideo2_{pack_name}\data\mcvideo_stuff{pack_name}\functions\tick2.mcfunction", "a") as f:
        f.write(tick_command_)
        f.close()

process_times = []
# cache for each pixel command later used for detecting if the pixel changed, this saves space
commands_cache = []
# cache for each color pair, so it can find the closest color faster
cache_palette = {}

invalid_detected = False

for frame, name in enumerate(listdir(directory)):  
    if invalid_detected:
        invalid_detected = False
        frame += -1
        
    # try to open image
    try:
        image = Image.open(f"{directory}\{name}")
    except Exception as e:
        invalid_detected = True
        print("please add a correct path to your video frames")
        print(e)
        continue

    start = perf_counter()
    img_x, img_y = image.size
    resized_image = resize(image, resolution, img_x, img_y)
    img_x, img_y = resized_image.size
    pix = resized_image.load()
    commands = ""
    tick_command = ""
    pixel_count = 0

    # for every pixel in current image
    for y in range(img_y):
        for x in range(img_x):
            r, g, b, = pix[x, y]
            im_color = [r, g, b]
            im_color_cache = tuple(im_color)

            # if color pair isn't cached then use closest_color to find the closest color and cache it
            if tuple(im_color) not in cache_palette.keys():
                closest_color = tuple(closest(palette, im_color))
                im_closest_cache = tuple(closest_color)
                cache_palette.update({im_color_cache: im_closest_cache})
            # if in cache use that
            else:
                closest_color = cache_palette.get(im_color_cache)

            # if show frames update the pixels on current image for showing
            if show_frames:
                resized_image.putpixel((x, y), closest_color)

            # get block name from block_palette dictionary
            block_name = block_palette.get(closest_color)

            command = f"execute at @e[type=minecraft:armor_stand,tag=pos{pack_name}] run setblock ^{x} ^ ^{y} {block_name}\n"

            if frame >= 1:
                # if pixel has changed use command, else don't use command
                if commands_cache[pixel_count] != command:
                    commands_cache[pixel_count] = command
                    commands += command

            # append all the commands from the first frame to commands_cache
            else:
                commands_cache.append(command)
                commands += command
            pixel_count += 1

    # tick2 command used to initiate the frame
    tick_command = f"execute if score frame_count frame_count{pack_name} matches " \
                   f"{frame} run function mcvideo_stuff{pack_name}:frame_functions/{frame}\n"

    # generates mcfunctions for both tick2 and frame_functions
    generate_mcfunction(frame, commands, tick_command)

    # shows the current frame, ignore Cannot find reference 'imread' in '__init__.py'
    if show_frames:
        resized_image.save(fp="1.jpeg", format="jpeg")
        render_image = cv2.imread("1.jpeg")
        cv2.imshow(f"FRAME", cv2.resize(render_image, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
        cv2.setWindowTitle("FRAME", f"FRAME{frame}")
        cv2.waitKey(1)

    # estimate time
    process_times.append(round(perf_counter() - start, 2))
    average_time = calculate_average_time(process_times)
    time_remaining = round((sum(process_times) + len(listdir(directory)) - frame) * average_time, 2)

    space = " "
    pad = f" Frame {frame}/{len(listdir(directory))}: {round(perf_counter() - start, 2)}s"
    print(fr"{pad.ljust(20+4,space)}|   time remaining: {time_remaining}s")

print(f"\n exported to datapack_output as {pack_name} | {len(listdir(directory))}frames")
