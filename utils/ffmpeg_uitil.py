from pathlib import Path

try:
    import ffmpeg
except ImportError:
    raise ImportError("You need to install ffmpeg-python or conda install conda-forge ffmpeg-python")


def convert_error_types(input_dir):
    folder_path = Path(input_dir)
    if not folder_path.exists():
        print("Folder is not exists. Please Download File with YouTube Video")
        raise SystemExit()

    if not any(folder_path.iterdir()):
        print("Folder is empty. Please Download File with YouTube Video")
        raise SystemExit()


def convert_mp4_to_wav(input_dir, output_dir):
    """
    Converts mp4 to wav must be installation python-ffmpeg
    """
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True)

    print("Converting mp4 to wav")

    for file in Path(input_dir).iterdir():
        file_path = f"./{file}"
        output_path = f"./{output_dir}/{file.stem}.wav"
        try:
            if (Path(output_path).exists()) or (Path(output_path).stat().st_size != 0):
                print(f"Converted file is exists: Skipping")
                continue
        except FileNotFoundError:
            try:
                ffmpeg.input(file_path).output(output_path, ac=1, f='wav').run(overwrite_output=True, quiet=True)
            except Exception as e:
                print(f"Video Error! {e}")

