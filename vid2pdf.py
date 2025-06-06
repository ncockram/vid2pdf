import os
import sys
import hashlib
from pytube import YouTube
import cv2
from PIL import Image
from fpdf import FPDF

def download_youtube_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_path = stream.download(output_path=output_path)
    return video_path

def extract_unique_frames(video_path, frame_interval=1):
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    unique_hashes = set()
    unique_frames = []
    prev_hash = None
    for sec in range(0, int(duration)):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        success, image = vidcap.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', image)
        img_bytes = buffer.tobytes()
        md5_hash = hashlib.md5(img_bytes).hexdigest()
        if md5_hash == prev_hash:
            continue
        if md5_hash not in unique_hashes:
            unique_hashes.add(md5_hash)
            unique_frames.append(img_bytes)
        prev_hash = md5_hash
    vidcap.release()
    return unique_frames

def save_frames_to_pdf(frames, output_pdf):
    pdf = FPDF()
    for img_bytes in frames:
        with open('temp.jpg', 'wb') as f:
            f.write(img_bytes)
        img = Image.open('temp.jpg')
        img = img.convert('RGB')
        img.save('temp.jpg')
        pdf.add_page()
        pdf.image('temp.jpg', x=10, y=10, w=190)
    if os.path.exists('temp.jpg'):
        os.remove('temp.jpg')
    pdf.output(output_pdf, "F")

def main():
    if len(sys.argv) != 3:
        print("Usage: python vid2pdf.py <YouTube_URL> <output.pdf>")
        sys.exit(1)
    url = sys.argv[1]
    output_pdf = sys.argv[2]
    print("Downloading video...")
    video_path = download_youtube_video(url, ".")
    print("Extracting unique frames...")
    frames = extract_unique_frames(video_path)
    print(f"{len(frames)} unique frames extracted.")
    print("Generating PDF...")
    save_frames_to_pdf(frames, output_pdf)
    print(f"PDF saved as {output_pdf}")
    os.remove(video_path)

if __name__ == "__main__":
    main()
