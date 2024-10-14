import os
import pickle
import gdown
import zipfile
import re


# 在 aist_data_loader.py 或 data_analyzer.py 中
from config_loader import config

output_path = config['data']['output_path']
window_length = config['analysis']['velocity_calculation']['window_length']

def download_and_extract_data(file_url, output_path):
    gdown.download(file_url, output_path, quiet=False, fuzzy=True)
    
    downloaded_files = os.listdir(output_path)
    downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_path, x)), reverse=True)
    file_name = downloaded_files[0]
    
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(os.path.join(output_path, file_name), 'r') as zip_ref:
            zip_ref.extractall(output_path)
    
    return file_name
download_video = download_and_extract_data ()

def get_motion_file_name(video_file_name):
    basename = os.path.splitext(video_file_name)[0]
    basename = os.path.splitext(basename)[0]
    
    match = re.match(r"^[a-zA-Z0-9_]+", basename)
    extracted_name = match.group(0) if match else basename
    
    new_filename = re.sub(r'_c\d{2}', '_cAll', extracted_name) + '.pkl'
    return new_filename
file_name = get_motion_file_name()

# 加载运动和关键点数据
def load_motion_data(motion_file_path, keypoints_file_path):
    with open(motion_file_path, 'rb') as f:
        motion_data = pickle.load(f)
    
    with open(keypoints_file_path, 'rb') as f:
        keypoints_data = pickle.load(f)
    
    return motion_data, keypoints_data
motion_data = load_motion_data ()