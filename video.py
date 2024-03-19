from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import scroll
from PIL import Image
import os
import math

video_name = 'output_video.mp4'
supported_formats = [".jpeg", ".jpg", ".png", ".webp"]
scroll_params = {
    'x_speed': 0, 
    'y_speed': 50,
    'apply_to': 'mask'
}

def createVideo(imgFolderName, musicFileName = None, timePerImage = 3, resolution = "360p", fadeIn = False, crossFadeIn=False, fadeOut = False, crossFadeOut=False, fadeInOut = False, crossFadeInOut = False, scrollEff=False):
    images = [img for img in os.listdir(imgFolderName) if any(img.endswith(format) for format in supported_formats)]
    resized_image_paths = []
    clips = []
    
    if resolution == "360p":
        width, height = 640, 360
    elif resolution == "720p":
        width, height = 1280, 720
    elif resolution == "1080p":
        width, height = 1920, 1080
    elif resolution == "4k":
        width, height = 3840, 2160
    else:
        width, height = 640, 360   
    
    black_screen = ColorClip(size=(width, height), color=(0, 0, 0), duration=0.25)
        

    if(fadeIn):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(1).fadeout(0)
            clips.append(clip)
        
    elif(crossFadeIn):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(1).crossfadeout(0)
            clips.append(clip)
        
    elif(fadeOut):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(0).fadeout(1)
            clips.append(clip)
            
    elif(crossFadeOut):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(0).crossfadeout(1)
            clips.append(clip)
        
    elif(fadeInOut):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(0.5).fadeout(0.5)
            clips.append(clip)
            
        
    elif(crossFadeInOut):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(0.5).crossfadeout(0.5)
            clips.append(clip)
            
    elif(scrollEff):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip_scroll = clip.fx(scroll, **scroll_params)
            clips.append(clip_scroll)
            
    else:
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((width, height))
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clips.append(clip)
        

    final_clip = black_screen
        
    for clip in clips:
        final_clip = concatenate_videoclips([final_clip, clip])
        
    if musicFileName is not None:
        audio_clip = AudioFileClip(musicFileName)
        audio_duration = audio_clip.duration
        # print("Original audio duration:", audio_duration)

        video_duration = final_clip.duration
        # print("Video duration:", video_duration)

        repetitions = max(math.ceil(float(video_duration) / float(audio_duration)) + 1, 1)
        # print("Repetitions needed:", repetitions)

        audio_clips = [audio_clip] * repetitions
        concatenated_audio_clip = concatenate_audioclips(audio_clips)
        concatenated_audio_clip = concatenated_audio_clip.set_duration(video_duration)
        # print("Concatenated audio duration:", concatenated_audio_clip.duration)

        final_clip = final_clip.set_audio(concatenated_audio_clip)

    
    final_clip.write_videofile(video_name, fps = 1)

    for resized_img_path in resized_image_paths:
        os.remove(resized_img_path)

    print("Video created successfully!")

createVideo("./static/Images")
