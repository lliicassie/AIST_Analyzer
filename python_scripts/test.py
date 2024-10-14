#!/opt/anaconda3/envs/beatnet_env/bin/python

from aist_processor import AISTDataProcessor
import os
from tqdm import tqdm
import time

def main():
    # 设置输出路径
    output_path = os.path.join(os.getcwd(), 'aist_output')
    os.makedirs(output_path, exist_ok=True)

    # AIST++ 视频的下载链接
    video_url = 'https://drive.google.com/uc?id=1L2IVvq3Z_0DpiI9NRSCTADvEBE5JZb4I&export=download'
    
    # AIST++ 动作数据的下载链接
    motion_data_url = 'https://drive.google.com/uc?id=1X54DfEG5TrAbFmGWO3Z6lnfoqXwodTFb&export=download'

    # 创建 AISTDataProcessor 实例
    processor = AISTDataProcessor(output_path)
    

    # 设置环境（包括修复 chumpy 兼容性）
    processor.setup_environment()

    # 定义处理步骤
    steps = [
        "设置环境",
        "下载视频",
        "下载动作数据",
        "解压动作数据",
        "加载动作数据",
        "分析动作数据"
    ]

    # 使用tqdm创建进度条
    with tqdm(total=len(steps), desc="总体进度") as pbar:
        # 设置环境
        print("\n设置环境...")
        processor.setup_environment()
        pbar.update(1)
        time.sleep(0.5)  # 为了更好的视觉效果添加短暂延迟

        # 处理数据
        print("\n开始处理数据...")
        result = processor.process_data(video_url, motion_data_url)
        
        # 模拟剩余步骤的进度
        for _ in range(len(steps) - 1):
            pbar.update(1)
            time.sleep(0.5)  # 为了更好的视觉效果添加短暂延迟

    if result:
        print("\n分析结果:")
        print(f"统计信息: {result['statistics']}")
        print(f"直方图保存路径: {result['file_paths']['histogram']}")
        print(f"视频文件路径: {result['video_path']}")
    else:
        print("数据处理失败。")

if __name__ == "__main__":
    main()