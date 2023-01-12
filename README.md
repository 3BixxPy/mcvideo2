# MCVIDEO2 - NEW UPDATED WITH ALL BLOCKS 1.19 = MORE COLORS
[Video from older version](https://www.youtube.com/watch?v=KN-YvopMdOs)

![](https://i.imgur.com/AZUGe8f.png)


# Setup
**You don't need any python knowledge to use this**
- install python, watch this tutorial [here](https://www.youtube.com/watch?v=Kn1HF3oD19c)
- first download by clicking the green "<> code" and selecting zip or use git
- cd to your extracted folder containing everything with `cd C:\downloads\example\mcvideo2` in Command Prompt and follow these next steps
- then do `pip install -r requirements.txt`
- you will need to generate your video frames for that use `py mcvideo.py framegen C:\example\Video.mp4` now your frames should be located in videoname_frames \
**pro tip: if you want just an image just put your image in a folder and use that**
- for the main part of generating the minecraft video itself use this command `py mcvideo.py mcvideo C:\example\Video_Frames 80`
80 is for the resolution use anything above 1, but i dont recommend using something bigger than 100
  - OPTIONAL PARAMETERS: usage `py mcvideo.py mcvideo C:\example\Video_Frames 80 --resample bicubic --blocktypes falling`
    - --blocktypes - what blocks to include, glowing glass falling choose up to 3 `--blocktypes glowing glass`
    - --showframes - shows current frame, true or false `--showframes true`
    - --resample - can yield better results try one of these, nearest bicubic bilinear `--resample bicubic`
- and finally run, the datapack will be stored in datapack_output/number put whats inside in your datapacks folder
    
 # Usage
 
- in minecraft Reload the datapack ```/reload```
- you will need to set a position for the video with ```/function minecraft_video:set_pos```
- Then start the video with ```/function minecraft_video:start_video```
- Use ```/function minecraft_video:pause_video``` to pause and ```/function minecraft_video:reset_video``` to reset
- ```/execute at @e[tag=pos] run tp @e[tag=pos] ~ ~ ~ Xrot Yrot``` to rotate the video

# Test Video

- datapack_output\test video.rar
- extract this to your datapack folder


![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png) ![](https://i.imgur.com/kpiN2vE.png)
