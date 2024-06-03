#注释表示需要修改的地方或要点
#这是调用模型的函数，需要环境为pytorch、modelscope（如果pip失败可以用清华的镜像）和librosa
import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


# 指定包含.wav文件的源文件夹路径
source_folders = {
    "高危人群": "/mntcephfs/lab_data/youjiajun/Tdata_重采样/高危人群",
    "健康人群": "/mntcephfs/lab_data/youjiajun/Tdata_重采样/健康人群",
    "确诊抑郁": "/mntcephfs/lab_data/youjiajun/Tdata_重采样/确诊抑郁"
}

# 输出文件夹的根路径
output_root_folder = "/mntcephfs/lab_data/youjiajun/Tdata_降噪"

# 确保输出根文件夹存在
if not os.path.exists(output_root_folder):
    os.makedirs(output_root_folder)

ans = pipeline(
Tasks.acoustic_noise_suppression,
model='damo/speech_frcrn_ans_cirm_16k'
)

for category, source_folder in source_folders.items():
    # 为每个类别创建一个单独的输出文件夹
    output_folder = os.path.join(output_root_folder, category)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith('.wav'):
            input_audio_path = os.path.join(source_folder, filename)
            base_name = os.path.splitext(filename)[0]
            output_audio_path = os.path.join(output_folder, f"{base_name}.wav")
            result = ans(input_audio_path, output_path=output_audio_path)
            print(f'去噪后的音频文件已保存到: {output_audio_path}')

print('所有文件的去噪处理已完成。')
