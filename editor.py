import os
import random
import cv2
import numpy as np
import asyncio
import edge_tts

try:
    # Try importing using the newer MoviePy v2.x structure
    from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
except ImportError:
    # Fallback to older MoviePy v1.x structure if needed
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def generate_voiceover(text, output_audio_path):
    voice_pool = [
        "en-IN-PrabhatNeural",  # Clear Indian English (Male)
        "en-IN-NeerjaNeural",   # Smooth Indian English (Female)
        "en-US-GuyNeural",      # Natural US English (Male)
        "en-US-AriaNeural",     # Natural US English (Female)
        "en-GB-RyanNeural",     # Professional UK English (Male)
        "en-GB-SoniaNeural"     # Professional UK English (Female)
        "en-IN-KavyaNeural",      # Female - Natural conversational tone, very popular
        "en-IN-AnanyaNeural",     # Female - Crisp, clear, friendly narrative tone
        "en-IN-MadhurNeural",     # Male   - Natural, casual tone, sounds like a product reviewer
    ]

    selected_voice = random.choice(voice_pool)
    print(f"🎙️ [Voiceover Engine] Selected voice asset: {selected_voice}")

    # 🚀 Step 1: Split text strictly at your custom '@' delimiter
    if "@" in text:
        hook, body = text.split("@", 1)
    elif "||" in text:
        hook, body = text.split("||", 1)
    elif "." in text:
        hook, body = text.split(".", 1)
    else:
        hook, body = text, ""

    hook = hook.strip()
    body = body.strip()

    # Fallback if there is no secondary text body segment
    if not body:
        async def render_single():
            communicate = edge_tts.Communicate(text, selected_voice, rate="-5%")
            await communicate.save(output_audio_path)
        asyncio.run(render_single())
        return True

    # Define paths for the temporary split audio files
    temp_hook_path = output_audio_path.replace(".mp3", "_hook_temp.mp3")
    temp_body_path = output_audio_path.replace(".mp3", "_body_temp.mp3")

    async def render_segments():
        # ⚡ Hook segment: Spoken with higher urgency (+10% speech rate)
        communicate_hook = edge_tts.Communicate(hook, selected_voice, rate="+20%", volume="+35%")
        await communicate_hook.save(temp_hook_path)

        # 🍃 Body segment: Spoken at a normal, smooth narrator pace (-6% speech rate)
        communicate_body = edge_tts.Communicate(body, selected_voice, rate="-6%")
        await communicate_body.save(temp_body_path)

    try:
        # Render the separate segments
        asyncio.run(render_segments())

        if os.path.exists(temp_hook_path) and os.path.exists(temp_body_path):
            hook_clip = AudioFileClip(temp_hook_path)
            body_clip = AudioFileClip(temp_body_path)

            # 🔊 Amplify the hook clip by 45% using moviepy's native audio effects
            hook_clip = hook_clip.volumex(1.45)

            # Stitch them back together sequentially
            from moviepy.editor import concatenate_audioclips
            final_audio = concatenate_audioclips([hook_clip, body_clip])
            final_audio.write_audiofile(output_audio_path, fps=44100, logger=None)

            # Close file handles to allow system cleanup
            hook_clip.close()
            body_clip.close()
            final_audio.close()

            # Remove temporary clip segments
            if os.path.exists(temp_hook_path): os.remove(temp_hook_path)
            if os.path.exists(temp_body_path): os.remove(temp_body_path)
            
            print(f"🎙️ Success: Combined audio using your custom '@' delimiter splits!")
            return True
        else:
            raise ValueError("Audio segment generation missing files.")

    except Exception as e:
        print(f"⚠️ Split rendering failed ({e}). Reverting to unified audio text layout...")
        async def fallback_main():
            clean_text = text.replace("@", "").replace("||", "")
            communicate = edge_tts.Communicate(clean_text, selected_voice, rate="-5%")
            await communicate.save(output_audio_path)
        try:
            asyncio.run(fallback_main())
            return True
        except Exception as final_err:
            print(f"❌ Critical Audio Breakdown: {final_err}")
            return False

def get_wrapped_lines(text, max_w, font, font_scale, thickness):
    """
    Utility function to break a long script down into perfectly sized visual lines.
    """
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        (text_w, _), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
        
        if text_w < max_w:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_word_by_word_subtitle(frame, line_text, center_x, bottom_y, frame_in_line, total_frames_for_line):
    """
    Renders subtitles word-by-word into a sentence block.
    As time progresses, more words from line_text seamlessly reveal themselves.
    The first word is highlighted in cyan/yellow, while subsequent visible words are clean white.
    """
    if not line_text:
        return

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1.3
    thickness = 3
    shadow_thickness = 9
    color_highlight = (0, 230, 255)  # Eye-catching neon yellow/cyan
    color_white = (255, 255, 255)
    color_black = (0, 0, 0)

    words = line_text.split()
    num_words = len(words)
    
    # Calculate ongoing step counts to reveal text progressively
    progress = frame_in_line / total_frames_for_line
    words_to_show = int(progress * num_words) + 1
    words_to_show = min(words_to_show, num_words)

    # Segment the current visible words subset
    visible_words = words[:words_to_show]
    first_word = visible_words[0].upper()
    remaining_visible = " ".join(visible_words[1:]).upper() if len(visible_words) > 1 else ""

    # Measure full text boundary constraints to anchor center position
    # This keeps spacing solid and stops words from jumping horizontally as they append
    full_first = words[0].upper()
    full_remaining = " ".join(words[1:]).upper() if len(words) > 1 else ""
    
    (w1_full, h1), _ = cv2.getTextSize(full_first, font, font_scale, thickness)
    if full_remaining:
        (w2_full, h2), _ = cv2.getTextSize(full_remaining, font, font_scale, thickness)
        (space_w, _), _ = cv2.getTextSize(" ", font, font_scale, thickness)
    else:
        w2_full, h2, space_w = 0, 0, 0

    total_w_full = w1_full + space_w + w2_full
    tx = center_x - (total_w_full // 2)
    ty = bottom_y + (max(h1, h2) // 2)

    # ---- Draw Highlighted First Word ----
    cv2.putText(frame, first_word, (tx, ty), font, font_scale, color_black, shadow_thickness, cv2.LINE_AA)
    cv2.putText(frame, first_word, (tx, ty), font, font_scale, color_highlight, thickness, cv2.LINE_AA)

    # ---- Draw Remaining Appending Words ----
    if remaining_visible:
        (w1_now, _), _ = cv2.getTextSize(full_first, font, font_scale, thickness)
        (s_w, _), _ = cv2.getTextSize(" ", font, font_scale, thickness)
        
        # Silhouette outline stroke
        cv2.putText(frame, remaining_visible, (tx + w1_now + s_w, ty), font, font_scale, color_black, shadow_thickness, cv2.LINE_AA)
        # Main body content core
        cv2.putText(frame, remaining_visible, (tx + w1_now + s_w, ty), font, font_scale, color_white, thickness, cv2.LINE_AA)

def draw_video_duration_line(frame, current_frame, total_frames):
    """
    Draws a sleek, modern, auto-advancing progress line 
    at the very top edge of the video frame container.
    """
    h, w, _ = frame.shape
    bar_height = 12
    
    progress_ratio = min(1.0, current_frame / max(1, total_frames))
    fill_width = int(w * progress_ratio)
    
    # 1. Base track overlay lane (Translucent matte backing)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_height), (35, 30, 32), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    
    # 2. Dynamic foreground load neon banner
    if fill_width > 0:
        cv2.rectangle(frame, (0, 0), (fill_width, bar_height), (0, 230, 255), -1, cv2.LINE_AA)

def get_rendered_scene_canvas(img, frame_in_image, total_image_frames):
    """
    Generates a scaled, blurred background canvas layered with a smooth 
    cinematic Ken Burns zooming foreground image layout.
    """
    orig_h, orig_w, _ = img.shape
    bg_canvas = cv2.resize(img, (1080, 1920))
    blurred_bg = cv2.GaussianBlur(bg_canvas, (151, 151), 0)
    black_tint = np.zeros_like(blurred_bg)
    canvas = cv2.addWeighted(blurred_bg, 0.65, black_tint, 0.35, 0)

    progress = frame_in_image / max(1, total_image_frames)
    zoom_factor = 1.0 + (progress * 0.05) 

    scale_ratio = min(1080 / orig_w, 1920 / orig_h)
    target_w = int(orig_w * scale_ratio * zoom_factor)
    target_h = int(orig_h * scale_ratio * zoom_factor)
    fg_resized = cv2.resize(img, (target_w, target_h))

    crop_x1 = max(0, (target_w - 1080) // 2)
    crop_y1 = max(0, (target_h - 1920) // 2)
    fg_cropped = fg_resized[crop_y1:crop_y1+1920, crop_x1:crop_x1+1080]

    fg_h, fg_w, _ = fg_cropped.shape
    start_y = (1080 - fg_w) // 2
    start_x = (1920 - fg_h) // 2
    
    canvas[start_x:start_x+fg_h, start_y:start_y+fg_w] = fg_cropped
    return canvas

def create_pro_video(image_paths, product_name, output_path, voice_text=None):
    print(f"🎬 [Editor] Launching Premium Word-by-Word Rendering Pipeline for: {product_name[:20]}...")
    
    valid_images = []
    thumbnail_img = None

    for idx, path in enumerate(image_paths):
        if os.path.exists(path):
            img = cv2.imread(path)
            if img is not None:
                if idx == 0 and os.path.basename(path).startswith("tn_"):
                    thumbnail_img = img
                else:
                    valid_images.append(img)

    if not valid_images and thumbnail_img is not None:
        valid_images.append(thumbnail_img)
    elif not valid_images:
        print("❌ [Editor Error] No valid product images found to compile.")
        return False

    temp_tts_path = output_path.replace(".mp4", "_voiceover.mp3")
    has_voice = False
    total_duration = 15  

    if voice_text and generate_voiceover(voice_text, temp_tts_path):
        try:
            temp_audio = AudioFileClip(temp_tts_path)
            total_duration = min(int(temp_audio.duration) + 1, 58) 
            temp_audio.close()
            has_voice = True
        except Exception as audio_prep_err:
            print(f"⚠️ Could not parse audio track dimensions: {audio_prep_err}")

    fps = 24
    outro_duration = 3  
    thumb_duration = 1.2 
    logo_filename = "SCIO_Logo.png"
    logo_path = os.path.join(os.getcwd(), logo_filename)
    logo_img = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED) if os.path.exists(logo_path) else None
    
    total_frames = total_duration * fps
    outro_frames = outro_duration * fps
    thumb_frames = int(thumb_duration * fps) if thumbnail_img is not None else 0
    product_frames = total_frames - outro_frames - thumb_frames
    
    if product_frames <= 0:  
        product_frames = total_frames
        outro_frames = 0
        thumb_frames = 0

    frames_per_image = product_frames // len(valid_images) if len(valid_images) > 0 else product_frames

    # Generate visual sentence line groups from narrative script
    subtitle_lines = []
    if voice_text:
        clean_script = ''.join(c for c in voice_text if c not in '()[]"-').strip()
        subtitle_lines = get_wrapped_lines(clean_script, 900, cv2.FONT_HERSHEY_SIMPLEX, 1.3, 3)
        
    if not subtitle_lines:
        subtitle_lines = ["Check Out This Amazing Deal!", "Link Is Available Below."]

    total_lines = len(subtitle_lines)
    frames_per_subtitle_line = max(1, product_frames // total_lines)

    temp_video_path = output_path.replace(".mp4", "_temp_render.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (1080, 1920))

    global_frame_counter = 0

    # ==========================================
    # PHASE A: WRITE THUMBNAIL HOOK FRAMES
    # ==========================================
    if thumb_frames > 0 and thumbnail_img is not None:
        print("🖼️ Rendering ultra-clean thumbnail hook sequence...")
        base_canvas = get_rendered_scene_canvas(thumbnail_img, 0, thumb_frames)
        # Display the first word of the first sentence as a hook text
        draw_word_by_word_subtitle(base_canvas, subtitle_lines[0], 1080 // 2, 1600, 0, thumb_frames)
        
        for _ in range(thumb_frames):
            frame_to_write = base_canvas.copy()
            draw_video_duration_line(frame_to_write, global_frame_counter, total_frames)
            out.write(frame_to_write)
            global_frame_counter += 1

    # ==========================================
    # PHASE B: MAIN SLIDESHOW LOOP (TRANSITIONS & APPENING SUBTITLES)
    # ==========================================
    print("🎞️ Rendering zoom sequences with seamless cross-fades and progress metrics...")
    transition_frames = 12  

    for f_idx in range(product_frames):
        img_idx = min(f_idx // frames_per_image, len(valid_images) - 1)
        frame_in_curr_img = f_idx % frames_per_image
        
        current_canvas = get_rendered_scene_canvas(valid_images[img_idx], frame_in_curr_img, frames_per_image)
        
        # Cross-Fade Image Transition Logic
        if frame_in_curr_img >= (frames_per_image - transition_frames):
            trans_progress = (frame_in_curr_img - (frames_per_image - transition_frames)) / transition_frames
            
            if img_idx < (len(valid_images) - 1):
                next_canvas = get_rendered_scene_canvas(valid_images[img_idx + 1], frame_in_curr_img - (frames_per_image - transition_frames), frames_per_image)
                current_canvas = cv2.addWeighted(current_canvas, 1.0 - trans_progress, next_canvas, trans_progress, 0)
            elif img_idx == (len(valid_images) - 1) and outro_frames > 0 and logo_img is not None:
                last_img = valid_images[-1].copy()
                bg_logo_canvas_preview = cv2.resize(last_img, (1080, 1920))
                bg_logo_canvas_preview = cv2.GaussianBlur(bg_logo_canvas_preview, (151, 151), 0)
                dark_matte = np.zeros_like(bg_logo_canvas_preview)
                bg_logo_canvas_preview = cv2.addWeighted(bg_logo_canvas_preview, 0.35, dark_matte, 0.65, 0)
                
                logo_h, logo_w = logo_img.shape[:2]
                logo_scale = 500 / logo_w
                new_logo_w = 500
                new_logo_h = int(logo_h * logo_scale)
                resized_logo = cv2.resize(logo_img, (new_logo_w, new_logo_h))
                logo_x_start = (1080 - new_logo_w) // 2
                logo_y_start = (1920 - new_logo_h) // 2
                
                if resized_logo.shape[2] == 4:  
                    alpha_ch = resized_logo[:, :, 3] / 255.0
                    for c in range(3):
                        bg_logo_canvas_preview[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w, c] = (
                            alpha_ch * resized_logo[:, :, c] +
                            (1.0 - alpha_ch) * bg_logo_canvas_preview[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w, c]
                        )
                else:  
                    bg_logo_canvas_preview[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w] = resized_logo
                
                current_canvas = cv2.addWeighted(current_canvas, 1.0 - trans_progress, bg_logo_canvas_preview, trans_progress, 0)

        # Calculate exact timeline position within the current block to trigger words step-by-step
        line_index = min(f_idx // frames_per_subtitle_line, total_lines - 1)
        frame_in_current_line = f_idx % frames_per_subtitle_line
        
        draw_word_by_word_subtitle(
            current_canvas, 
            subtitle_lines[line_index], 
            1080 // 2, 
            1600, 
            frame_in_current_line, 
            frames_per_subtitle_line
        )
        
        # Inject the advancing video progress bar
        draw_video_duration_line(current_canvas, global_frame_counter, total_frames)

        out.write(current_canvas)
        global_frame_counter += 1

    # ==========================================
    # PHASE C: BRAND OUTRO SEQUENCE
    # ==========================================
    if outro_frames > 0 and logo_img is not None:
        last_img = valid_images[-1].copy()
        bg_logo_canvas = cv2.resize(last_img, (1080, 1920))
        bg_logo_canvas = cv2.GaussianBlur(bg_logo_canvas, (151, 151), 0)
        dark_matte = np.zeros_like(bg_logo_canvas)
        bg_logo_canvas = cv2.addWeighted(bg_logo_canvas, 0.35, dark_matte, 0.65, 0) 

        logo_h, logo_w = logo_img.shape[:2]
        logo_scale = 500 / logo_w
        new_logo_w = 500
        new_logo_h = int(logo_h * logo_scale)
        resized_logo = cv2.resize(logo_img, (new_logo_w, new_logo_h))

        logo_x_start = (1080 - new_logo_w) // 2
        logo_y_start = (1920 - new_logo_h) // 2

        if resized_logo.shape[2] == 4:  
            alpha_channel = resized_logo[:, :, 3] / 255.0
            for c in range(3):
                bg_logo_canvas[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w, c] = (
                    alpha_channel * resized_logo[:, :, c] +
                    (1.0 - alpha_channel) * bg_logo_canvas[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w, c]
                )
        else:  
            bg_logo_canvas[logo_y_start:logo_y_start+new_logo_h, logo_x_start:logo_x_start+new_logo_w] = resized_logo

        sub_text = "Follow & Subscribe for More Deals!"
        sub_font = cv2.FONT_HERSHEY_SIMPLEX
        sub_scale = 1.1
        sub_thick = 3
        (s_w, s_h), _ = cv2.getTextSize(sub_text, sub_font, sub_scale, sub_thick)
        sub_x = (1080 - s_w) // 2
        sub_y = logo_y_start + new_logo_h + 100
        cv2.putText(bg_logo_canvas, sub_text, (sub_x, sub_y), sub_font, sub_scale, (255, 255, 255), sub_thick, cv2.LINE_AA)

        lib_logo_path = os.path.join(os.getcwd(), "LinkInBio_Logo.png")
        if os.path.exists(lib_logo_path):
            lib_logo = cv2.imread(lib_logo_path, cv2.IMREAD_UNCHANGED)
            if lib_logo is not None:
                target_lib_w = 700
                orig_lib_h, orig_lib_w = lib_logo.shape[:2]
                target_lib_h = int(orig_lib_h * (target_lib_w / orig_lib_w))
                resized_lib = cv2.resize(lib_logo, (target_lib_w, target_lib_h))
                lib_x_start = (1080 - target_lib_w) // 2
                lib_y_start = 150

                if resized_lib.shape[2] == 4:
                    alpha_channel = resized_lib[:, :, 3] / 255.0
                    for c in range(3):
                        bg_logo_canvas[lib_y_start:lib_y_start+target_lib_h, lib_x_start:lib_x_start+target_lib_w, c] = (
                            alpha_channel * resized_lib[:, :, c] +
                            (1.0 - alpha_channel) * bg_logo_canvas[lib_y_start:lib_y_start+target_lib_h, lib_x_start:lib_x_start+target_lib_w, c]
                        )
                else:
                    bg_logo_canvas[lib_y_start:lib_y_start+target_lib_h, lib_x_start:lib_x_start+target_lib_w] = resized_lib

        for _ in range(outro_frames):
            frame_to_write = bg_logo_canvas.copy()
            draw_video_duration_line(frame_to_write, global_frame_counter, total_frames)
            out.write(frame_to_write)
            global_frame_counter += 1

    out.release()

    # ==========================================
    # PHASE D: PRO STEREO AUDIO DUCKING COMPOSITE
    # ==========================================
    try:
        video_clip = VideoFileClip(temp_video_path)
        audio_layers = []

        if has_voice:
            voice_clip = AudioFileClip(temp_tts_path)
            audio_layers.append(voice_clip)

        bg_music_dir = os.path.join(os.getcwd(), "Background_Music")
        if os.path.exists(bg_music_dir):
            music_files = [os.path.join(bg_music_dir, f) for f in os.listdir(bg_music_dir) if f.lower().endswith('.mp3')]
            if music_files:
                selected_track = random.choice(music_files)
                print(f"🎵 Layering background audio track: {os.path.basename(selected_track)}")
                
                # Create a safe compatibility wrapper for slicing clips
                def safe_subclip(clip, start, end):
                    if hasattr(clip, "subclipped"):
                        return clip.subclipped(start, end)  # MoviePy v2.x (Cloud)
                    return clip.subclip(start, end)          # MoviePy v1.x (Local)

                # Fix: Properly instantiate the background audio clip before slicing it
                base_music = AudioFileClip(selected_track)
                bg_music_clip = safe_subclip(base_music, 0, video_clip.duration)
                
                if has_voice:
                    voice_cutoff_time = total_duration - outro_duration
                    duck_filter = lambda gf, t: gf(t) * np.where(t < voice_cutoff_time, 0.06, 0.18)[:, np.newaxis]
                    
                    if hasattr(bg_music_clip, "fl"):
                        bg_music_clip = bg_music_clip.fl(duck_filter)
                    else:
                        bg_music_clip = bg_music_clip.transform(duck_filter)
                else:
                    bg_music_clip = bg_music_clip.volumex(0.12) if hasattr(bg_music_clip, "volumex") else bg_music_clip.multiply_volume(0.12)
                    
                audio_layers.append(bg_music_clip)

        if audio_layers:
            final_audio_mix = CompositeAudioClip(audio_layers)
            # Adapt dynamically between MoviePy v1 (set_audio) and v2 (with_audio)
            if hasattr(video_clip, "with_audio"):
                final_output_clip = video_clip.with_audio(final_audio_mix)  # v2.x
            else:
                final_output_clip = video_clip.set_audio(final_audio_mix)   # v1.x
        else:
            final_output_clip = video_clip

        final_output_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate="5000k",
            audio_bitrate="128k",
            ffmpeg_params=[
                '-pix_fmt', 'yuv420p',
                '-profile:v', 'high',
                '-level', '4.0'
            ],
            logger=None,
            write_logfile=False
        )
        
        final_output_clip.close()
        video_clip.close()
        if has_voice: voice_clip.close()
        if os.path.exists(bg_music_dir) and music_files and 'bg_music_clip' in locals() and bg_music_clip is not None: 
            bg_music_clip.close()
        
        if os.path.exists(temp_video_path): os.remove(temp_video_path)
        if os.path.exists(temp_tts_path): os.remove(temp_tts_path)
            
        print(f"🎉 SUCCESS: Video rendered with premium rolling word subtitles! Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Video compilation pipeline failure: {e}")
        if os.path.exists(temp_video_path):
            try: os.remove(temp_video_path)
            except: pass
        if os.path.exists(temp_tts_path):
            try: os.remove(temp_tts_path)
            except: pass
        return False