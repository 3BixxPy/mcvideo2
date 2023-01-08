import time
from PIL import Image
from colorthief import ColorThief
import os
import argparse
# this is a Dev tool used to collect all minecraft blocks using textures\blocks and get the dominant color, so it can be
# used later to represent pixels
# results are stored in your destination or current location as color_data.txt, Enjoy :D


# arguments
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser = argparse.ArgumentParser()
parser.add_argument("path", type=dir_path, help="add a path to your block textures")
parser.add_argument("--destination", type=dir_path, help="add a path to your block textures")
args = parser.parse_args()

#main
start_time = time.time()
total_blocks = 0
directory = args.path
for name in os.listdir(directory):
    # skip if mcmeta file
    if "mcmeta" in name.split("."):
        continue

    image_path = fr"{directory}\{name}"
    img = Image.open(image_path)
    img_x, img_y = img.size
    alpha = 255
    pix = img.load()
    for y in range(img_y):
        if alpha == 0:
            break

        for x in range(img_x):
            # checks for tuple
            if isinstance(pix[x, y], tuple):
                # checks for alpha channel
                if len(pix[x, y]) == 3:
                    alpha = 255
                # sets alpha value based on alpha channel
                if len(pix[x, y]) == 4:
                    alpha = pix[x, y][3]

            # if not a tuple then its an alpha pixel
            elif not isinstance(pix[x, y], tuple):
                if pix[x, y] == 0:
                    alpha = 0

            if alpha == 0:
                break

    # blacklisted subnames
    subnames = ["on", "front", "back", "side", "top", "side0", "side1", "side2", "side3", "side4",
                "outside", "inside", "bottom", "inner", "lit", "still"]
    has_subname = False

    # if no blank pixels were found
    if alpha != 0:
        # delete .png from the name
        name = name.replace(".png", "")

        # if subname in blacklisted subnames
        for subname in name.split("_"):
            if subname in subnames:
                has_subname = True
        if not has_subname:
            # gets the average color of a block
            color_thief = ColorThief(image_path)
            try:
                dominnant_color = color_thief.get_color(quality=1)
            except Exception as e:
                print(f"couldn't parse {name}")
                continue

            # prints to a txt file
            if args.destination:
                with open(fr"{args.destination}\color_data.txt", "a") as f:
                    f.write(f"{dominnant_color}: \"{name}\",\n")
            else:
                with open("color_data.txt", "a") as f:
                    f.write(f"{dominnant_color}: \"{name}\",\n")
            total_blocks += 1

print(f"final time: {round(time.time() - start_time, 2)}s, total blocks: {total_blocks}")
