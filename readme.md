### 简介

  一个生成用于测试屏幕刷新率的视频 Python 脚本

  该程序会生成类似 https://testufo.com/frameskipping 中白色格子移动的的视频

  屏幕刷新率测试方法参考视频: https://www.bilibili.com/video/BV1ma411s7SZ

  测试屏幕刷新率的网站: https://testufo.com/

  同时生成的视频也可以用于测试是否丢帧

### 环境依赖

使用 `pip` 依次安装即可

| 模块   | 功能       |
| ------ | ---------- |
| pillow | 生成帧     |
| opencv | 合成视频   |
| tqdm   | 进度条     |
| fire   | 命令行封装 |

```
pip install fire opencv-python Pillow tqdm
```



### 使用方法

```shell
python generate_test_video.py ROW COLUMN FPS <flags>

# 例如
python generate_test_video.py 5 12 60 60FPS.mp4

# 查看说明
python generate_test_video.py -h | --help

POSITIONAL ARGUMENTS
    ROW
        指定网格为 row 行, 大于 0 的整数
    COLUMN
        指定网格为 column 列, 大于 0 的整数
    FPS   
        视频帧率, 一般 fsp 等于网格数量, 即 fps = row * column, 大于 0 的整数
FLAGS
    --output=OUTPUT
        Default: 'output.mp4'
        生成的视频的路径, 如 ./output.mp4, 文件名需要以 .mp4 为结尾
    --width=WIDTH
        Default: 1920
        视频分辨率--宽度, 大于 0 的整数
    --height=HEIGHT
        Default: 1080
        视频分辨率--高度, 大于 0 的整数
    --duration=DURATION
        Default: 10
        视频时长, 大于 0 的整数
    --linewidth=LINEWIDTH
        Default: 3
        网格线条的宽度, 单位为 像素, 大于 0 的整数
    --margin=MARGIN
        Default: 0.1
        指定网格边框占据画面的百分比, 0 <= margin < 1
```



### 待办事项

- [ ] 自动化分析相机慢动作(高帧率)拍出的视频
- [ ] 生成带数字的视频，并借助 OCR 进行自动化分析
- [ ] 可配置网格背景色和移动的方格的颜色
- [ ] 完善文档

### 参考资料

https://www.bilibili.com/video/BV1ma411s7SZ

https://www.jianshu.com/p/c6f5d62cca41

https://www.cnblogs.com/adenosine/p/16394447.html

