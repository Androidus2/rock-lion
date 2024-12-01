import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from pytube import Playlist

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.isPlaying = False
        self.isPaused = False
        self.queue = []
        self.vc = None

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

    def PrepareVideo(self, item):
        """
        Prepare the video for playback
        """
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                #print(f"Extracted info: {info}")
            except Exception as e:
                print(f"Error extracting info: {e}")
                return False
        #return info['url']
        return {'title': info['title'], 'url': info['url']}

    def Search(self, playlist_url):
        """
        Search for a song or a playlist
        """
        if 'playlist' in playlist_url:
            # Retrieve URLs of videos from playlist
            playlist = Playlist(playlist_url)
            urls = []
            for url in playlist:
                urls.append(url)
            return urls
        else:
            # Return the URL of the video
            return [playlist_url]
    
    async def PlayNext(self, ctx):
        """
        Play the next song in the queue
        """
        print("In PlayNext")
        if len(self.queue) > 0:
            nextURL = self.queue[0]
            prepared = self.PrepareVideo(nextURL)
            music = prepared['url']
            title = prepared['title']
            #music = self.queue[0]
            if music is False:
                print("Error preparing the video")
                await ctx.send("There was an error preparing the video")
                return
            print(f"Playing music")
            self.isPlaying = True
            self.isPaused = False

            self.queue.pop(0)

            await ctx.send(f"Playing {title}")
            print("Starting to play")

            after_callback = lambda e: self.bot.loop.create_task(self.PlayNext(ctx))

            print(f"Audio source URL: {music}")
            print(f"FFmpeg options: {self.FFMPEG_OPTIONS}")

            try:
                audio_source = discord.FFmpegPCMAudio(music, **self.FFMPEG_OPTIONS)
            except Exception as e:
                print(f"Error creating FFmpegPCMAudio object: {e}")
                await ctx.send("There was an error playing the audio.")
                return

            print("Audio source object created successfully")

            if self.vc is None or not self.vc.is_connected():
                voice_channel = ctx.author.voice.channel
                if voice_channel is None:
                    await ctx.send("You are not connected to a voice channel")
                    return

                self.vc = await voice_channel.connect()
                await ctx.send("Bot has joined the voice channel")
                print("Bot has joined the voice channel")

            self.vc.play(audio_source, after=after_callback)
            print("Audio playback started")
        else:
            self.isPlaying = False
            self.isPaused = False
    
    async def PlayMusic(self, ctx):
        """
        Play music in the voice channel
        """
        if self.isPlaying:
            await ctx.send("Already playing a song")
            return
        
        if self.vc is None or not self.vc.is_connected():
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send("You are not connected to a voice channel")
                return

            self.vc = await voice_channel.connect()
            print("Bot has joined the voice channel")
            await ctx.send("Bot has joined the voice channel")
        
        await self.PlayNext(ctx)
    
    @commands.command(name='play', aliases=['p'], help='Play a song')
    async def Play(self, ctx, *, item):
        """
        Play a song
        """
        # if we are playing a song and it is paused and we say play without any arguments, then resume the song
        if self.isPlaying and self.isPaused and item == '':
            await self.Resume(ctx)
            return

        print(f"Playing {item}")
        song = self.Search(item)
        #print(f"Search result: {song}")
        if song is False:
            print("Error searching for the song")
            await ctx.send("Could not download the song. Incorrect format or unavailable.")
            return
        
        print(f"Adding a song to the queue")
        self.queue += song
        if 'playlist' in item:
            print(f"Adding {len(song)} songs to the queue")
            await ctx.send(f"Added {len(song)} songs to the queue")
        else:
            print(f"Adding a song to the queue")
            await ctx.send(f"Added a song to the queue")

        if not self.isPlaying:
            await self.PlayMusic(ctx)

    @commands.command(name='pause', help='Pause the current song')
    async def Pause(self, ctx):
        """
        Pause the current song
        """
        print("Pausing the song")
        if self.isPlaying and not self.isPaused:
            self.vc.pause()
            self.isPaused = True
            await ctx.send("Paused the song")
        else:
            await ctx.send("No song is playing")

    @commands.command(name='resume', help='Resume the current song')
    async def Resume(self, ctx):
        """
        Resume the current song
        """
        print("Resuming the song")
        if self.isPlaying and self.isPaused:
            self.vc.resume()
            self.isPaused = False
            await ctx.send("Resumed the song")
        else:
            await ctx.send("No song is paused")
    
    @commands.command(name='skip', aliases=['next'], help='Skip the current song')
    async def Skip(self, ctx):
        """
        Skip the current song
        """
        print("Skipping the song")
        if self.isPlaying:
            self.vc.stop()
            await ctx.send("Skipping the song")
            #await self.PlayNext(ctx)
        else:
            await ctx.send("No song is playing")

    @commands.command(name='stop', help='Stop the current song')
    async def Stop(self, ctx):
        """
        Stop the current song
        """
        print("Stopping the song")
        if self.isPlaying:
            self.vc.stop()
            self.isPlaying = False
            self.isPaused = False
            await ctx.send("Stopped the song")
        else:
            await ctx.send("No song is playing")

    @commands.command(name='queue', help='Show the queue')
    async def Queue(self, ctx):
        """
        Show the queue
        """
        print("Showing the queue")
        #queue = '```'
        #for i, music in enumerate(self.queue):
        #    queue += f'{i+1}. {music["title"]}\n'
        #queue += '```'
        #print(queue)
        print("Queue shown")
        await ctx.send(len(self.queue))
    
    @commands.command(name='leave', help='Leave the voice channel')
    async def Leave(self, ctx):
        """
        Leave the voice channel
        """
        print("Leaving the voice channel")
        if self.vc is not None:
            await self.vc.disconnect()
            self.vc = None
            self.isPlaying = False
            self.isPaused = False
            self.queue = []
            await ctx.send("Left the voice channel")
    
    @commands.command(name='clear', help='Clear the queue')
    async def Clear(self, ctx):
        """
        Clear the queue
        """
        print("Clearing the queue")
        self.queue = []
        await ctx.send("Cleared the queue")

    @commands.command(name='shuffle', help='Shuffle the queue')
    async def Shuffle(self, ctx):
        """
        Shuffle the queue
        """
        print("Shuffling the queue")
        import random
        random.shuffle(self.queue)
        await ctx.send("Shuffled the queue")