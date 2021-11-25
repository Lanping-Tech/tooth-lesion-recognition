# Tooth Lesion Recognition

## Download the pre-trained model

两个阶段的预训练模型下载链接：[https://pan.baidu.com/s/1wC2VZfTsd7K3d3BlxQZn4w](https://pan.baidu.com/s/1wC2VZfTsd7K3d3BlxQZn4w) 提取码：lnki 

下载完成后，将预训练模型文件`step_one.pt`和`step_two.pt`放到`models`文件夹中即可。

## Install & Deploy

```
pip install -r requirements.txt
```

## Running

```
python manage.py runserver 0.0.0.0:8000
```

then,

```
http://127.0.0.1:8000/detect/?image-path=图片路径
```

即可得到识别结果。