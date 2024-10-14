import os
import sys
import subprocess
import zipfile
import pickle
import numpy as np
import vedo
import ipywidgets as widgets
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import torch
from smplx import SMPL
from math import pi
import matplotlib.colors as mcolors
import cv2
import gdown

def clone_aistplusplus_api():
    repo_url = 'https://github.com/google/aistplusplus_api.git'
    repo_name = 'aistplusplus_api'

    if not os.path.exists(repo_name):
        print("Cloning aistplusplus_api repository...")
        subprocess.run(['git', 'clone', repo_url])
    else:
        print("aistplusplus_api repository already exists.")

def install_dependencies():
    # 升级 pip 和 setuptools
    subprocess.run(['pip', 'install', '--upgrade', 'pip', 'setuptools'])

    # 安装 AIST++ API 的依赖项
    requirements_path = os.path.join('aistplusplus_api', 'requirements.txt')
    subprocess.run(['pip', 'install', '-r', requirements_path])

    # 运行 setup.py 安装 AIST++ API
    setup_path = os.path.join('aistplusplus_api', 'setup.py')
    subprocess.run(['python', setup_path, 'install'])

    # 安装其他必要的包
    additional_packages = [
        'aniposelib',
        'smplx',
        'numpy',
        'chumpy',
        'vedo',
        'ipywidgets',
        'pyyaml',
        'pympi-ling',
        'pandas',
        'gdown',
        'pydrive',
        'torch',
        'matplotlib',
        'scipy',
        'opencv-python'
    ]
    subprocess.run(['pip', 'install'] + additional_packages)

def download_and_extract_aist_data():
    # AIST++ 运动数据的下载链接
    # 请替换为您实际需要的数据集链接
    motion_data_url = 'https://drive.google.com/uc?id=YOUR_MOTION_DATA_FILE_ID&export=download'
    
    # 使用 gdown 下载文件
    print("Downloading AIST++ motion data...")
    motion_data_zip = 'aist_plusplus_motions.zip'
    gdown.download(motion_data_url, motion_data_zip, quiet=False)

    # 解压缩下载的文件
    print("Extracting AIST++ motion data...")
    with zipfile.ZipFile(motion_data_zip, 'r') as zip_ref:
        zip_ref.extractall('.')

    # 删除下载的 zip 文件
    os.remove(motion_data_zip)
    print("AIST++ motion data is ready.")

def load_and_process_aist_data():
    # 将 aistplusplus_api 添加到路径中
    sys.path.append('aistplusplus_api')

    # 导入 AIST++ API
    import aistplusplus_api as aist

    # 设置 AIST++ 数据的路径
    AIST_DATA_PATH = './aist_plusplus_final'

    # 加载 AIST++ 数据库
    dataset = aist.AISTDataset(AIST_DATA_PATH)
aist_data = load_and_process_aist_data()
    