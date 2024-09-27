# 高速公路应急车道紧急启用模型-数据提取

根据视频数据提取相关交通流参数

## 目录

- [激活虚拟环境](#激活虚拟环境)
- [用法](#用法)
- [贡献](#贡献)
- [声明](#声明)

## 激活虚拟环境
   ```
   conda create -f environment.yml
   conda activate yolo
   ```
## 用法

### 1. 数据标注

使用[labelme](https://github.com/wkentaro/labelme)进行数据标注，标注结果保存在`./data/xx.xx.xx.xx/xx.xx.xx.xx-xx.json`文件中

**NOTE**： `labelme`最好在windows系统下安装

### 2. 获取流量、速度等信息

```
python SpeedEsm_multi.py
```
### 3. 获取变道信息

```
python LaneChange.py
```

### 4. 流量、速度数据平滑

```
python traffic_flow.py
```

### 贡献

Kewei Li: kwbb1997@gmail.com

Yanwen Kong

Fei Li

## 声明
```
2024年研究生数学建模竞赛E题
```