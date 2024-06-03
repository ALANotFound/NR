#注释表示需要修改的地方或要点


#这是重采样函数，将.m4a和.mp3文件转换成16khz单声道.wave文件，文件的属性-详细信息-音频-比特率为256kbs是正常现象
#环境需要pyhub（pip install pydub即可）和ffmpig（到https://ffmpeg.org/download.html 下载，Windows系统下载https://github.com/BtbN/FFmpeg-Builds/releases中124mb的那一项并用英文路径配置环境）
import os
import subprocess
from pydub import AudioSegment
from pydub.utils import which

# 指定 ffmpeg 和 ffprobe 的路径
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# 包含音频文件的源文件夹路径
source_folders = {
    "高危人群": "/mntcephfs/lab_data/youjiajun/其他单位-已分类/高危人群",
    "健康人群": "/mntcephfs/lab_data/youjiajun/其他单位-已分类/健康人群",
    "确诊抑郁": "/mntcephfs/lab_data/youjiajun/其他单位-已分类/确诊抑郁"
}

output_root_folder = "/mntcephfs/lab_data/youjiajun/Tdata_重采样" # 输出文件根路径

# 确保输出根文件夹存在
if not os.path.exists(output_root_folder):
    os.makedirs(output_root_folder)

# 记录转换失败的文件
failed_files = []

for category, source_folder in source_folders.items():
    # 为每个类别创建一个单独的输出文件夹
    output_folder = os.path.join(output_root_folder, category)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith(('.wav', '.mp3', '.m4a', '.WAV')):
            source_file_path = os.path.join(source_folder, filename)
            try:
                print(f"Processing {source_file_path}")

                # 如果是 WAV 文件，尝试重新编码
                if filename.endswith('.WAV'):
                    temp_file_path = os.path.join(source_folder, f"temp_{filename}")
                    command = [
                        'ffmpeg',
                        '-i', source_file_path,
                        '-acodec', 'pcm_s16le',
                        '-ar', '16000',
                        '-ac', '1',
                        temp_file_path
                    ]
                    subprocess.run(command, check=True)
                    source_file_path = temp_file_path

                sound = AudioSegment.from_file(source_file_path)
                sound = sound.set_channels(1)
                sound = sound.set_frame_rate(16000)
                base_name = os.path.splitext(filename)[0]
                new_filename = f"{base_name}.wav"
                output_file_path = os.path.join(output_folder, new_filename)
                sound.export(output_file_path, format='wav', codec='pcm_s16le')
                print(f'Converted {filename} to {new_filename}')

                # 删除临时文件
                if filename.endswith('.WAV') and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            except Exception as e:
                print(f"Failed to convert {filename}: {e}")
                failed_files.append(source_file_path)
                break

# 检查是否有未转换的文件
if failed_files:
    print("The following files failed to convert:")
    for file in failed_files:
        print(file)
else:
    print('All files have been converted.')
