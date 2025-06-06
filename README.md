# vid2pdf

vid2pdf is a Python script that downloads a YouTube video, extracts unique frames, and compiles them into a PDF file.

## Requirements

- Python 3.6 or higher
- [pytube](https://pytube.io/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [Pillow](https://pillow.readthedocs.io/)
- [fpdf](https://pyfpdf.github.io/fpdf2/)

You can install the required packages using:

```
pip install -r requirements.txt
```

Or individually:

```
pip install pytube opencv-python pillow fpdf
```

## Usage

Run the script from the command line:

```
python vid2pdf.py "<YouTube_URL>" <output.pdf>
```

Replace `<YouTube_URL>` with the actual YouTube video link and `<output.pdf>` with your desired output filename.

**Example:**

```
python vid2pdf.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" output.pdf
```

## How it works

1. Downloads the YouTube video as an MP4 file.
2. Extracts unique frames (one per second, skipping duplicates).
3. Saves the frames as images and compiles them into a single PDF file.
4. Cleans up temporary files after completion.

## License

MIT License
