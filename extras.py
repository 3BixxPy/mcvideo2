from os import makedirs, listdir, mkdir, path
import cv2
from numpy import arange
from datetime import timedelta

block_palette = {(108, 100, 92): "acacia_log",
                 (161, 84, 49): "acacia_planks",
                 (164, 124, 244): "amethyst_block",
                 (140, 140, 140): "andesite",
                 (100, 100, 100): "bedrock",
                 (188, 148, 92): "beehive",
                 (220, 220, 204): "birch_log",
                 (212, 199, 135): "birch_planks",
                 (52, 44, 52): "blackstone",
                 (12, 12, 20): "black_concrete",
                 (145, 34, 34): "black_glazed_terracotta",
                 (36, 20, 20): "black_terracotta",
                 (15, 16, 21): "black_wool",
                 (44, 44, 140): "blue_concrete",
                 (44, 44, 140): "blue_glazed_terracotta",
                 (108, 160, 252): "blue_ice",
                 (76, 60, 92): "blue_terracotta",
                 (49, 52, 152): "blue_wool",
                 (165, 136, 72): "bookshelf",
                 (229, 126, 189): "brain_coral_block",
                 (140, 108, 100): "bricks",
                 (100, 60, 36): "brown_concrete",
                 (28, 113, 131): "brown_glazed_terracotta",
                 (148, 116, 84): "brown_mushroom_block",
                 (76, 52, 36): "brown_terracotta",
                 (105, 65, 35): "brown_wool",
                 (148, 20, 148): "bubble_coral_block",
                 (220, 167, 238): "budding_amethyst",
                 (220, 220, 212): "calcite",
                 (216, 139, 32): "carved_pumpkin",
                 (143, 184, 164): "chain_command_block",
                 (38, 38, 38): "chiseled_deepslate",
                 (56, 28, 30): "chiseled_nether_bricks",
                 (60, 60, 68): "chiseled_polished_blackstone",
                 (236, 232, 224): "chiseled_quartz_block",
                 (162, 79, 15): "chiseled_red_sandstone",
                 (222, 214, 169): "chiseled_sandstone",
                 (124, 120, 124): "chiseled_stone_bricks",
                 (172, 172, 188): "clay",
                 (20, 20, 20): "coal_block",
                 (46, 46, 44): "coal_ore",
                 (112, 78, 54): "coarse_dirt",
                 (116, 116, 116): "cobbled_deepslate",
                 (97, 97, 97): "cobblestone",
                 (190, 126, 87): "command_block",
                 (196, 108, 76): "copper_block",
                 (122, 124, 123): "copper_ore",
                 (97, 97, 97): "cracked_deepslate_bricks",
                 (82, 82, 82): "cracked_deepslate_tiles",
                 (49, 25, 28): "cracked_nether_bricks",
                 (36, 26, 28): "cracked_polished_blackstone_bricks",
                 (99, 99, 99): "cracked_stone_bricks",
                 (121, 57, 57): "crimson_nylium",
                 (127, 60, 87): "crimson_planks",
                 (148, 18, 18): "crimson_stem",
                 (108, 6, 187): "crying_obsidian",
                 (180, 100, 68): "cut_copper",
                 (198, 108, 36): "cut_red_sandstone",
                 (222, 214, 168): "cut_sandstone",
                 (20, 124, 140): "cyan_concrete",
                 (40, 88, 100): "cyan_glazed_terracotta",
                 (244, 239, 239): "cyan_terracotta",
                 (20, 128, 140): "cyan_wool",
                 (60, 52, 28): "dark_oak_log",
                 (47, 28, 12): "dark_oak_planks",
                 (52, 84, 70): "dark_prismarine",
                 (132, 124, 116): "dead_brain_coral_block",
                 (157, 151, 143): "dead_bubble_coral_block",
                 (157, 150, 142): "dead_fire_coral_block",
                 (132, 124, 116): "dead_horn_coral_block",
                 (159, 154, 146): "dead_tube_coral_block",
                 (55, 55, 63): "deepslate",
                 (92, 92, 92): "deepslate_bricks",
                 (83, 83, 85): "deepslate_coal_ore",
                 (74, 79, 80): "deepslate_copper_ore",
                 (78, 81, 83): "deepslate_diamond_ore",
                 (75, 76, 78): "deepslate_emerald_ore",
                 (83, 73, 65): "deepslate_gold_ore",
                 (124, 124, 124): "deepslate_iron_ore",
                 (102, 102, 102): "deepslate_lapis_ore",
                 (83, 81, 84): "deepslate_redstone_ore",
                 (40, 40, 40): "deepslate_tiles",
                 (95, 243, 232): "diamond_block",
                 (122, 122, 122): "diamond_ore",
                 (225, 225, 225): "diorite",
                 (124, 84, 60): "dirt",
                 (148, 124, 100): "dripstone_block",
                 (97, 244, 150): "emerald_block",
                 (115, 118, 115): "emerald_ore",
                 (220, 228, 164): "end_stone",
                 (185, 177, 129): "end_stone_bricks",
                 (164, 116, 100): "exposed_copper",
                 (193, 134, 121): "exposed_cut_copper",
                 (148, 108, 76): "farmland",
                 (108, 60, 20): "farmland_moist",
                 (164, 36, 44): "fire_coral_block",
                 (41, 31, 31): "gilded_blackstone",
                 (252, 232, 76): "gold_block",
                 (122, 122, 122): "gold_ore",
                 (150, 102, 86): "granite",
                 (52, 60, 60): "gray_concrete",
                 (154, 154, 154): "gray_glazed_terracotta",
                 (60, 44, 36): "gray_terracotta",
                 (60, 68, 69): "gray_wool",
                 (76, 92, 36): "green_concrete",
                 (209, 209, 212): "green_glazed_terracotta",
                 (76, 84, 44): "green_terracotta",
                 (95, 127, 23): "green_wool",
                 (252, 214, 105): "honeycomb_block",
                 (212, 204, 60): "horn_coral_block",
                 (164, 196, 252): "ice",
                 (190, 190, 190): "iron_block",
                 (140, 140, 140): "iron_ore",
                 (200, 122, 21): "jack_o_lantern",
                 (82, 61, 23): "jungle_log",
                 (182, 131, 96): "jungle_planks",
                 (30, 67, 140): "lapis_block",
                 (131, 131, 131): "lapis_ore",
                 (135, 115, 107): "ancient_debris",
                 (139, 100, 58): "barrel",
                 (76, 76, 76): "basalt",
                 (105, 78, 53): "bee_nest",
                 (92, 93, 93): "blast_furnace",
                 (67, 46, 20): "cartography_table",
                 (129, 86, 37): "composter",
                 (46, 28, 16): "crafting_table",
                 (88, 17, 17): "crimson_nylium",
                 (198, 108, 36): "cut_red_sandstone",
                 (139, 139, 123): "dried_kelp_block",
                 (53, 51, 51): "furnace",
                 (157, 76, 40): "hay_block",
                 (168, 135, 87): "loom",
                 (164, 172, 28): "melon",
                 (59, 52, 48): "muddy_mangrove_roots",
                 (119, 89, 72): "mycelium",
                 (92, 54, 38): "note_block",
                 (92, 92, 92): "polished_basalt",
                 (102, 161, 160): "prismarine",
                 (95, 168, 160): "prismarine_bricks",
                 (228, 143, 34): "pumpkin",
                 (228, 36, 12): "redstone_block",
                 (54, 30, 21): "redstone_lamp",
                 (233, 41, 41): "redstone_ore",
                 (67, 69, 72): "reinforced_deepslate",
                 (106, 82, 180): "repeating_command_block",
                 (116, 196, 100): "slime_block",
                 (40, 31, 31): "smithing_table",
                 (70, 59, 44): "smoker",
                 (69, 69, 76): "smooth_basalt",
                 (119, 119, 119): "smooth_stone",
                 (92, 68, 60): "soul_sand",
                 (92, 68, 60): "soul_soil",
                 (116, 84, 44): "spruce_planks",
                 (114, 114, 114): "stone",
                 (124, 120, 124): "stone_bricks",
                 (177, 94, 60): "stripped_acacia_log",
                 (197, 176, 118): "stripped_birch_log",
                 (148, 60, 100): "stripped_crimson_stem",
                 (76, 60, 36): "stripped_dark_oak_log",
                 (172, 132, 84): "stripped_jungle_log",
                 (124, 52, 52): "stripped_mangrove_log",
                 (189, 152, 95): "stripped_oak_log",
                 (121, 92, 52): "stripped_spruce_log",
                 (63, 159, 151): "stripped_warped_stem",
                 (148, 92, 68): "terracotta",
                 (180, 20, 36): "tnt",
                 (87, 89, 79): "tuff",
                 (88, 41, 40): "warped_nylium",
                 (60, 135, 135): "warped_planks",
                 (68, 44, 92): "warped_stem",
                 (100, 167, 116): "weathered_copper",
                 (180, 188, 76): "wet_sponge",
                 (204, 212, 212): "white_concrete",
                 (36, 140, 196): "white_glazed_terracotta",
                 (212, 180, 164): "white_terracotta",
                 (219, 223, 224): "white_wool",
                 (236, 172, 20): "yellow_concrete",
                 (252, 238, 165): "yellow_glazed_terracotta",
                 (188, 132, 35): "yellow_terracotta",
                 (252, 214, 55): "yellow_wool",
                 }

glass = {(22, 24, 29): "black_concrete_powder",
         (69, 71, 164): "blue_concrete_powder",
         (122, 83, 52): "brown_concrete_powder",
         (36, 147, 157): "cyan_concrete_powder",
         (76, 80, 83): "gray_concrete_powder",
         (94, 116, 46): "green_concrete_powder",
         (73, 179, 212): "light_blue_concrete_powder",
         (153, 153, 146): "light_gray_concrete_powder",
         (124, 188, 43): "lime_concrete_powder",
         (189, 80, 181): "magenta_concrete_powder",
         (226, 129, 29): "orange_concrete_powder",
         (227, 148, 178): "pink_concrete_powder",
         (130, 54, 176): "purple_concrete_powder",
         (177, 60, 52): "red_concrete_powder",
         (217, 220, 221): "white_concrete_powder",
         (233, 198, 53): "yellow_concrete_powder",
         (204, 108, 36): "red_sand",
         (129, 121, 119): "gravel",
         (220, 204, 164): "sand",
         }

falling = {(129, 121, 119): "gravel",
           (22, 24, 29): "black_concrete_powder",
           (233, 198, 53): "yellow_concrete_powder",
           (217, 220, 221): "white_concrete_powder",
           (76, 80, 83): "gray_concrete_powder",
           (94, 116, 46): "green_concrete_powder",
           (122, 83, 52): "brown_concrete_powder",
           (69, 71, 164): "blue_concrete_powder",
           (36, 147, 157): "cyan_concrete_powder",
           }

glowing = {(252, 172, 108): "shroomlight",
           (252, 236, 180): "ochre_froglight",
           (141, 186, 123): "verdant_froglight",
           (252, 244, 220): "glowstone",
           }


# missing sand


def generate_datapack():
    pack_name = 0
    if not path.isdir(r"datapack_output\1"):
        makedirs(r"datapack_output\1")
    else:
        for name in listdir(r"datapack_output"):
            pack_name = int(name)

    makedirs(fr"datapack_output\{pack_name + 1}\mcvideo2\data\minecraft\tags\functions")
    makedirs(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions")
    makedirs(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\frame_functions")

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\pack.mcmeta", "w") as f:
        f.write("""{
    "pack": {
        "pack_format": 10,
        "description": "\\u00A79by 3Bixx"
    }
}""")

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\minecraft\tags\functions\load.json", "w") as f:
        f.write("""{
    "values": [
        "mcvideo_stuff:load"
    ]
}""")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\minecraft\tags\functions\tick.json", "w") as f:
        f.write("""{
    "values": [
        "mcvideo_stuff:tick",
        "mcvideo_stuff:tick2"
    ]
}""")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\load.mcfunction", "w") as f:
        f.write("say loaded\n"
                "scoreboard objectives add fps_tick dummy\n"
                "scoreboard objectives add fps_count dummy\n"
                "scoreboard objectives add fps dummy\n"
                "scoreboard players set fps fps 1\n")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\pause_video.mcfunction",
              "w") as f:
        f.write("tag @e[tag=pos] remove run_fps")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\reset_video.mcfunction",
              "w") as f:
        f.write("tag @e[tag=pos] remove run_fps\n"
                "scoreboard players reset fps_count fps_count\n"
                "function mcvideo_stuff:frame_functions/0")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\start_video.mcfunction",
              "w") as f:
        f.write("function mcvideo_stuff:reset_video\n"
                "tag @e[tag=pos] add run_fps")
        f.close()
        
    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\set_pos.mcfunction",
              "w") as f:
        f.write("kill @e[tag=pos,type=armor_stand]\n"
                "execute at @s run summon minecraft:armor_stand ~ ~ ~ {Tags:[pos],NoGravity:1b}\n"
                "execute at @e[tag=pos,type=armor_stand] run tp @e[tag=pos,type=armor_stand] ~ ~ ~ -180 90")
        f.close()

    with open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\tick.mcfunction", "w") as f:
        f.write("execute if entity @e[tag=pos,tag=run_fps] run scoreboard players add fps_tick fps_tick 1\n"
                "execute if score fps_tick fps_tick >= fps fps run scoreboard players add fps_count fps_count 1\n"
                "execute if score fps_tick fps_tick >= fps fps run scoreboard players set fps_tick fps_tick 0\n")
        f.close()

    tick2 = open(fr"datapack_output\{pack_name + 1}\mcvideo2\data\mcvideo_stuff\functions\tick2.mcfunction", "w")
    tick2.close()

    return pack_name + 1


SAVING_FRAMES_PER_SECOND = 20


# I stole this code
def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05)
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def make_frames(video_file):
    filename, _ = path.splitext(video_file)
    filename += "_frames"
    # make a folder by the name of the video file
    if not path.isdir(filename):
        mkdir(filename)
    # read the video file
    try:
        cap = cv2.VideoCapture(video_file)
    except Exception as e:
        print(e)
        exit()
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration,
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1
