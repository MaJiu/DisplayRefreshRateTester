import math
from PIL import Image, ImageColor, ImageDraw
import cv2
import os
import tqdm
import fire


TEMP_DIR = "./.temp_frames/"
BACKGROUND_COLOR = "black"
LINE_COLOR = "white"
SQUARE_COLOR = "white"


def generate_video(row, column, fps, output="output.mp4", width=1920, height=1080, duration=10, linewidth=3, margin=0.1):
    """ 一个生成用于测试屏幕刷新率的视频 Python 脚本

    该程序会生成类似 https://testufo.com/frameskipping 中的视频
    屏幕刷新率测试方法参考视频: https://www.bilibili.com/video/BV1ma411s7SZ
    测试屏幕刷新率的网站:https://testufo.com/
    同时生成的视频也可以用于测试是否丢帧

    Usage:
        python generate_test_video.py 5 12 60 60FPS.mp4 

    Args:
        row (int): 指定网格为 row 行, 大于 0 的整数
        column (int): 指定网格为 column 列, 大于 0 的整数
        fps (int): 视频帧率, 一般 fsp 等于网格数量, 即 fps = row * column, 大于 0 的整数
        output (str): 生成的视频的路径, 如 ./output.mp4, 文件名需要以 .mp4 为结尾
        width (int): 视频分辨率--宽度, 大于 0 的整数
        height (int): 视频分辨率--高度, 大于 0 的整数
        duration (int): 视频时长, 大于 0 的整数
        linewidth (int): 网格线条的宽度, 单位为 像素, 大于 0 的整数
        margin (float): 指定网格边框占据画面的百分比, 0 <= margin < 1

    """

    frame_width, frame_height = width, height
    fps = max(fps, row * column)
    if not len(output.strip()):
        output = f"{fps}FPS.mp4"
    if not output.endswith(".mp4"):
        output += "mp4"
    frames = generate_frames(row, column, fps, frame_width, frame_height, linewidth, margin)
    video_writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_width, frame_height))
    images = [cv2.imread(f) for f in frames]
    print("正在将帧合成视频...")
    with tqdm.tqdm(total=duration*len(images), unit=" 帧") as pbar:
        for i in range(duration):
            for image in images:
                video_writer.write(image)
                pbar.update(1)
    video_writer.release()


def generate_frames(row, colunm, fps, frame_width, frame_height, linewidth, margin):
    x_margin = int(frame_width * margin)
    y_margin = int(frame_height * margin)
    rect_width = (frame_width - x_margin * 2 - linewidth) // colunm - linewidth
    rect_height = (frame_height - y_margin * 2 - linewidth) // row - linewidth
    
    frame = Image.new("RGB", (frame_width, frame_height), ImageColor.getcolor(BACKGROUND_COLOR, "RGB"))
    drawer = ImageDraw.Draw(frame)

    x0 = x_margin + math.ceil(linewidth / 2) - 1
    y0 = y_margin + math.ceil(linewidth / 2) - 1
    
    # 绘制网格
    for i in range(colunm+1):
        x = x0 + i * (rect_width + linewidth)
        drawer.line([x, y0, x, y0 + row * (rect_height + linewidth)], width=linewidth, fill=LINE_COLOR)

    for i in range(row+1):
        y = y0 + i * (rect_height + linewidth)
        drawer.line([x0, y, x0 + colunm * (rect_width + linewidth), y], width=linewidth, fill=LINE_COLOR)

    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    # 填充方格
    x0 = x_margin + linewidth
    y0 = y_margin + linewidth
    frames = []
    print("正在生成帧...")
    for i in tqdm.trange(fps, unit=" 帧"):
        x1 = x0 + (rect_width + linewidth) * (i % colunm)
        y1 = y0 + (rect_height + linewidth) * (i // colunm)
        x2, y2 = x1 + rect_width - 1, y1 + rect_height - 1

        drawer.rectangle([x1, y1, x2, y2], width=0, fill=SQUARE_COLOR)
        filename = f"{TEMP_DIR}{i+1}.jpg"
        frames.append(filename)
        frame.save(filename)
        drawer.rectangle([x1, y1, x2, y2], width=0, fill=BACKGROUND_COLOR) # 恢复为白色

    frames.sort(key=lambda x : int(os.path.splitext(os.path.basename(x))[0]))
    return frames

if __name__ == '__main__':
    fire.Fire(generate_video)


