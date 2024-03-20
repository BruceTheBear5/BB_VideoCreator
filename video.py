from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, CompositeVideoClip, ColorClip
from moviepy.video.fx import fadein, fadeout
from PIL import Image, ImageOps
import os
import math
import shutil

video_name = './output_video.mp4'
supported_formats_images = [".jpeg", ".jpg", ".png", ".webp"]
scroll_params = {
    'x_speed': 0, 
    'y_speed': 50,
    'apply_to': 'mask'
}

def createVideo(imgFolderName, audioFolderName, userId, timePerImage = 3, resolution = "360p", tranistion = None):
    final_video_path = f'./static/output/user{userId}/'
    if not os.path.exists(imgFolderName):
        os.makedirs(imgFolderName)
    if not os.path.exists(audioFolderName):
        os.makedirs(audioFolderName)
    
    images = [img for img in os.listdir(imgFolderName) if any(img.endswith(format) for format in supported_formats_images)]
    images_with_times = [(img, os.path.getmtime(os.path.join(imgFolderName, img))) for img in images]
    sorted_images = sorted(images_with_times, key=lambda x: x[1])
    images = [filename for filename, _ in sorted_images]

    audios = [audio for audio in os.listdir(audioFolderName) if (audio.endswith(('.mp3', '.wav', '.aac', '.mpga')))]
    audios_with_times = [(audio, os.path.getmtime(os.path.join(audioFolderName, audio))) for audio in audios]
    sorted_audios = sorted(audios_with_times, key=lambda x: x[1])
    audios = [filename for filename, _ in sorted_audios]

    # print(audios)
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
        
    if(tranistion == "fadeIn"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(1).fadeout(0)
            clips.append(clip)
        
    elif(tranistion == "crossFadeIn"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(1).crossfadeout(0)
            clips.append(clip)
        
    elif(tranistion == "fadeOut"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(0).fadeout(1)
            clips.append(clip)
            
    elif(tranistion == "crossFadeOut"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(0).crossfadeout(1)
            clips.append(clip)
        
    elif(tranistion == "fadeInOut"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.fadein(1).fadeout(1)
            clips.append(clip)
            
        
    elif(tranistion == "crossFadeInOut"):
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clip = clip.crossfadein(1).crossfadeout(1)
            clips.append(clip)
            
    else:
        for image in images:
            img_path = os.path.join(imgFolderName, image)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = ImageOps.pad(img, (width, height), color="black")
            resized_img_path = os.path.join(imgFolderName, "resized_" + os.path.splitext(image)[0] + ".jpg") 
            img.save(resized_img_path)
            resized_image_paths.append(resized_img_path)
            clip = ImageSequenceClip([resized_img_path], fps = 1)
            clip = clip.set_duration(timePerImage)
            clips.append(clip)
        
    final_clip = black_screen
        
    for clip in clips:
        final_clip = concatenate_videoclips([final_clip, clip])
        
    if audios is not None:
        mainAudio = ''
        for audio in audios:
            audioReq = os.path.join(audioFolderName, os.path.splitext(audio)[0] + os.path.splitext(audio)[1]) 
            audio_clip = AudioFileClip(audioReq)
            if mainAudio == '':
                mainAudio = audio_clip
            else:
                mainAudioList = [mainAudio] + [audio_clip]
                mainAudio = concatenate_audioclips(mainAudioList)
        
        if mainAudio != '':
            audio_clip = mainAudio
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

    shutil.move(video_name, final_video_path + 'output_video.mp4')
    
    print("Video created successfully!")

if __name__ == "__main__":
    createVideo("./Selected", "./SelectedAudio", timePerImage= 10)
