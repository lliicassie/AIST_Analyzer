import os
import sys
import subprocess
import zipfile
import pickle
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gdown
import uuid
import shutil
class AISTDataProcessor:
    def __init__(self, output_path):
        self.output_path = output_path
        self.aist_data_path = os.path.join(output_path, 'aist_plusplus_final')
        self.video_path = os.path.join(output_path, 'videos')
        os.makedirs(self.video_path, exist_ok=True)

    def setup_environment(self):
        print("设置环境...")
        self.clone_aistplusplus_api()
        self.install_dependencies()
      #  self.fix_chumpy_compatibility()
        print("环境设置完成。")

    # ... (其他方法保持不变)
        '''

    def fix_chumpy_compatibility(self):
        print("修复 chumpy 兼容性...")
        chumpy_init_file = '/opt/anaconda3/lib/python3.11/site-packages/chumpy/__init__.py'
        
        if not os.path.exists(chumpy_init_file):
            print(f"警告：找不到 chumpy __init__.py 文件：{chumpy_init_file}")
            print("尝试查找 chumpy 安装位置...")
            try:
                import chumpy
                chumpy_init_file = os.path.join(os.path.dirname(chumpy.__file__), '__init__.py')
                print(f"找到 chumpy __init__.py 文件：{chumpy_init_file}")
            except ImportError:
                print("无法导入 chumpy。请确保它已正确安装。")
                return

        with fileinput.FileInput(chumpy_init_file, inplace=True) as file:
            for line in file:
                line = line.replace('from numpy import bool, int, float, complex, object, unicode, str, nan, inf',
                                    'from numpy import bool_, int_, float_, complex_, object_, str_, nan, inf')
                line = line.replace('np.bool', 'np.bool_')
                line = line.replace('np.int', 'np.int_')
                line = line.replace('np.float', 'np.float_')
                line = line.replace('np.complex', 'np.complex_')
                line = line.replace('np.object', 'np.object_')
                line = line.replace('np.str', 'np.str_')
                print(line, end='')
        
        print("chumpy 兼容性修复完成。")
        '''
    def clone_aistplusplus_api(self):
        repo_url = 'https://github.com/google/aistplusplus_api.git'
        repo_name = 'aistplusplus_api'
        
        if not os.path.exists(repo_name):
            print("克隆 aistplusplus_api 仓库...")
            subprocess.run(['git', 'clone', repo_url])
        else:
            print("aistplusplus_api 仓库已存在。")

    def install_dependencies(self):
        subprocess.run(['pip', 'install', '--upgrade', 'pip', 'setuptools'])
        
        requirements_path = os.path.join('aistplusplus_api', 'requirements.txt')
        subprocess.run(['pip', 'install', '-r', requirements_path])
        
        setup_path = os.path.join('aistplusplus_api', 'setup.py')
        subprocess.run(['python', setup_path, 'install'])
        
        additional_packages = [
            'aniposelib', 'smplx', 'numpy', 'chumpy', 'vedo', 'ipywidgets',
            'pyyaml', 'pympi-ling', 'pandas', 'gdown', 'pydrive', 'torch',
            'matplotlib', 'scipy', 'opencv-python'
        ]
        subprocess.run(['pip', 'install'] + additional_packages)

    def download_and_extract_data(self, file_url):
        print("检查是否已经存在 AIST++ 动作数据...")
        motion_data_zip = 'aist_motion.zip'
        extracted_folder = os.path.join(self.output_path, 'aist_plusplus_final')  # 假设这是解压后的文件夹

        # 检查解压后的文件夹是否存在
        if os.path.exists(extracted_folder):
            print("AIST++ 动作数据已存在，跳过下载和解压。")
            return

        print("下载 AIST++ 动作数据...")
        gdown.download(file_url, os.path.join(self.output_path, motion_data_zip), quiet=False)

        print("解压 AIST++ 动作数据...")
        with zipfile.ZipFile(os.path.join(self.output_path, motion_data_zip), 'r') as zip_ref:
            zip_ref.extractall(self.output_path)

        os.remove(os.path.join(self.output_path, motion_data_zip))
        print("AIST++ 动作数据准备就绪。")
    def load_motion_data(self, motion_file_path, keypoints_file_path):
        try:
            with open(motion_file_path, 'rb') as f:
                motion_data = pickle.load(f)
            
            with open(keypoints_file_path, 'rb') as f:
                keypoints_data = pickle.load(f)
            
            return motion_data, keypoints_data
        except FileNotFoundError:
            print(f"错误：未找到文件 {motion_file_path} 或 {keypoints_file_path}")
            return None, None
        except pickle.UnpicklingError:
            print(f"错误：无法解析文件 {motion_file_path} 或 {keypoints_file_path}")
            return None, None

    def analyze_motion_data(self, keypoints_data):
        if keypoints_data is None:
            return None

        keypoints = keypoints_data['keypoints3d']
        velocities = np.diff(keypoints, axis=0)
        avg_velocities = np.mean(velocities, axis=1)
        vertical_velocities = avg_velocities[:, 1]
        
        df = pd.DataFrame({
            'Frame': np.arange(len(vertical_velocities)),
            'Vertical_Velocity': vertical_velocities
        })
        
        plt.figure(figsize=(10, 6))
        plt.hist(df['Vertical_Velocity'], bins=50, edgecolor='k', alpha=0.7)
        plt.title("Vertical_Velocity_Distribution")
        plt.xlabel("Vertical_Velocity")
        plt.ylabel("Frequency")
        histogram_filename = f"histogram_{uuid.uuid4().hex}.png"
        histogram_filepath = os.path.join(self.output_path, histogram_filename)
        plt.savefig(histogram_filepath, format='png')
        plt.close()
        
        stats = {
            'Mean': df['Vertical_Velocity'].mean(),
            'Standard': df['Vertical_Velocity'].std(),
            'min': df['Vertical_Velocity'].min(),
            'max': df['Vertical_Velocity'].max(),
            'quantile': df['Vertical_Velocity'].quantile([0.25, 0.5, 0.75]).to_dict()
        }
        
        return {
            'mean_velocity': np.mean(vertical_velocities),
            'std_velocity': np.std(vertical_velocities),
            'min_velocity': np.min(vertical_velocities),
            'max_velocity': np.max(vertical_velocities),
            'quantiles': np.quantile(vertical_velocities, [0.25, 0.5, 0.75]),
            'vertical_velocities': vertical_velocities  # 保存原始数据用于绘图
        }

    def generate_histogram(self, vertical_velocities):
        plt.figure(figsize=(10, 6))
        plt.hist(vertical_velocities, bins=50, edgecolor='k', alpha=0.7)
        plt.title("Vertical Velocity Distribution")
        plt.xlabel("Vertical Velocity")
        plt.ylabel("Frequency")
        histogram_path = os.path.join(self.output_path, f"histogram_{uuid.uuid4().hex}.png")
        plt.savefig(histogram_path)
        plt.close()
        return histogram_path


    def get_motion_file_name(self, video_file_name):
        basename = os.path.splitext(os.path.basename(video_file_name))[0]
        match = re.match(r"^[a-zA-Z0-9_]+", basename)
        extracted_name = match.group(0) if match else basename
        new_filename = re.sub(r'_c\d{2}', '_cAll', extracted_name) + '.pkl'
        return new_filename

    def download_video(self, video_url):
        print("下载 AIST++ 视频数据...")

        # 首先尝试下载到临时位置
        temp_file_path = gdown.download(video_url, output=None, quiet=False, fuzzy=True)

        if temp_file_path is None:
            print("下载失败，无法获取视频文件。")
            return None

        video_file_name = os.path.basename(temp_file_path)
        video_file_path = os.path.join(self.video_path, video_file_name)
        
        if not os.path.exists(video_file_path):
            # 如果目标位置不存在文件，移动临时文件到目标位置
            shutil.move(temp_file_path, video_file_path)
            print(f"视频已下载并移动到: {video_file_path}")
        else:
            # 如果目标位置已存在文件，删除临时文件
            os.remove(temp_file_path)
            print(f"视频已存在: {video_file_path}")
        
        return video_file_name

    def process_data(self, video_url, motion_data_url):
        # 下载视频
        video_file_path = self.download_video(video_url)
        video_filename = self.get_motion_file_name(video_file_path)
        
        # 下载和处理动作数据
        self.download_and_extract_data(motion_data_url)
        motion_file_name = self.get_motion_file_name(video_filename)
        
        motion_file_path = os.path.join(self.aist_data_path, 'motions', motion_file_name)
        keypoints_file_path = os.path.join(self.aist_data_path, 'keypoints3d', motion_file_name)
        
        motion_data, keypoints_data = self.load_motion_data(motion_file_path, keypoints_file_path)
        if motion_data is None or keypoints_data is None:
            return None

        result = {
            'statistics': self.analyze_motion_data(keypoints_data),
            'file_paths': {
                'video': video_file_path,
                'motion_data': motion_file_path,
                'keypoints_data': keypoints_file_path,
            }
        }

        # 生成并保存直方图
        histogram_path = self.generate_histogram(result['statistics']['vertical_velocities'])
        result['file_paths']['histogram'] = histogram_path
        result['video_path'] = video_file_path

        return result
 
    
