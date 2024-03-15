from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, CompositeVideoClip, ColorClip
from PIL import Image
import os

video_name = 'output_video.mp4'
width, height = 640, 480 
supported_formats = [".jpeg", ".jpg", ".png", ".webp"]

def createVideo(imgFolderName, musicFileName, fps):
    images = [img for img in os.listdir(imgFolderName) if any(img.endswith(format) for format in supported_formats)]
    resized_image_paths = []
    clips = []
    black_screen = ColorClip(size=(width, height), color=(0, 0, 0), duration=0.25)

    for image in images:
        img_path = os.path.join(imgFolderName, image)
        img = Image.open(img_path)
        img = img.convert('RGB')
        img = img.resize((width, height))
        resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
        img.save(resized_img_path)
        resized_image_paths.append(resized_img_path)
        clip = ImageSequenceClip([resized_img_path], fps=fps)
        clip = clip.set_duration(2)
        clip = clip.fadein(1).fadeout(0)
        clips.append(clip)

    final_clip = black_screen
    for clip in clips:
        final_clip = concatenate_videoclips([final_clip, clip])

    audio_clip = AudioFileClip(musicFileName)
    audio_duration = audio_clip.duration
    video_duration = final_clip.duration
    repetitions = min(int(video_duration / audio_duration) + 1, 1)
    audio_clips = [audio_clip] * repetitions
    concatenated_audio_clip = concatenate_audioclips(audio_clips)
    concatenated_audio_clip = concatenated_audio_clip.set_duration(video_duration)
    final_clip = final_clip.set_audio(concatenated_audio_clip)
    
    final_clip.write_videofile(video_name, fps=fps)

    for resized_img_path in resized_image_paths:
        os.remove(resized_img_path)

    print("Video created successfully!")

createVideo("./static/Images", "./try.mp3", 4)
