# MCVIDEO2 - NEW UPDATED WITH ALL BLOCKS = MORE COLORS
[Video](https://www.youtube.com/watch?v=KN-YvopMdOs)

![](https://i.imgur.com/AZUGe8f.png)


# Usage
**You don't need any python knowledge to use this**
- install python 
- first download by clicking the green "code" and selecting zip or use git
- cd to your extracted folder containing everything with `cd C:\downloads\example\mcvideo2` in Command Prompt and follow these next steps
- you will need to generate your video frames for that use `py mcvideo.py framegen C:\example\Video.mp4` now your frames should be located in videoname_frames \
**pro tip: if you want just an image just put your image in a folder and use that**
- for the main part of generating the minecraft video itself use this command `py mcvideo.py mcvideo C:\example\Video_Frames 80`
80 is for the resolution use anything above 1, but i dont recommend using something bigger than 100
  - OPTIONAL PARAMETERS: usage `py mcvideo.py mcvideo C:\example\Video_Frames 80 --resample bicubic --blocktypes falling`
    - --blocktypes - what blocks to include, glowing glass falling choose up to 3 `--blocktypes glowing glass`
    - --showframes - shows current frame, true or false `--showframes true`
    - --resample - can yield better results try one of these, nearest bicubic bilinear `--resample bicubic`
