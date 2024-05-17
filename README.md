# FFMPEG light weight video editor

FFMPEG is a super powerful tool, but I can't be asked to remember most of the commands.

This tool will help me use the FFMPEG library to quickly make some common video edits I use for clips. Since I use high quality recordings, I sometimes need to reduce the duration of the clip. If I find other uses for it, I'll add them in.

The tool will exist as a tkinter user interface with ttkbootstrap for theming and keeping the interface modern looking.

______

In order to use this tool, you MUST have ffmpeg installed and 'ffmpeg' as the environment variable call. 
If you don't have it in your environment variables, the tool will not work. 
I have no intention of bundling FFMPEG with this application, although it is possible. 

______

As of right now there are a few optimizations I'd make

1. Output the logs in a better way instead of obscuring it
2. Show processing percentages so the user can have an idea of how long it'll take to launch
3. Allow for different output types (GIF/MP4)

I'm open for recommendations! 