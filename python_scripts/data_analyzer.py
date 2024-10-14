import os
import gdown
import pickle
import zipfile
import numpy as np
import pandas as pd
import io
from matplotlib import pyplot as plt

# 加载配置
from config_loader import config
from aist_data_loader import download_video
from aist_data_loader import file_name 
from aist_data_loader import motion_data
from data_download import aist_data
output_path = config['data']['output_path']


# 分析数据
def analyze_motion_data(keypoints_data):
    keypoints = keypoints_data['keypoints3d']
    num_frames, num_joints, _ = keypoints.shape
    velocities = np.diff(keypoints, axis=0)

    avg_velocities = np.mean(velocities, axis=1)
    vertical_velocities = avg_velocities[:, 1]

    df = pd.DataFrame({
        'Frame': np.arange(len(vertical_velocities)),
        'Vertical_Velocity': vertical_velocities
    })

    # 生成直方图并保存为图片文件
    plt.figure(figsize=(10, 6))
    plt.hist(df['Vertical_Velocity'], bins=50, edgecolor='k', alpha=0.7)
    
    # 生成唯一的文件名，避免文件名冲突
    import uuid
    histogram_filename = f"histogram_{uuid.uuid4().hex}.png"
    histogram_filepath = os.path.join(output_path, histogram_filename)
    
    plt.savefig(histogram_filepath, format='png')
    plt.close()

    # 计算统计信息
    stats = {
        'Mean Vertical Velocity': df['Vertical_Velocity'].mean(),
        'Standard Deviation': df['Vertical_Velocity'].std(),
        'Minimum Vertical Velocity': df['Vertical_Velocity'].min(),
        'Maximum Vertical Velocity': df['Vertical_Velocity'].max(),
        'Quantiles': df['Vertical_Velocity'].quantile([0.25, 0.5, 0.75]).to_dict()
    }

    return {
        'statistics': stats,
        'histogram_path': histogram_filepath  # 返回图片文件的路径
    }

def process_data(file_url):
    # 下载并解压数据
    file_name = download_and_extract_data(file_url, output_path)
    motion_file_name = get_motion_file_name(file_name)

    # 构建文件路径
    motion_file_path = os.path.join(AIST_DATA_PATH, 'motions', motion_file_name)
    keypoints_file_path = os.path.join(AIST_DATA_PATH,'keypoints3d', motion_file_name)

    # 加载数据
    motion_data, keypoints_data = load_motion_data(motion_file_path, keypoints_file_path)

    # 分析数据
    result = analyze_motion_data(keypoints_data)
    return result