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

## 接口说明

### 输入参数

|  参数名   | 格式  |说明  |
|  ----  | ----  |----  |
| image-path  | str | 待检测图片路径|

### 输出参数

|  参数名   | 格式  |说明  |
|  ----  | ----  |----  |
| status | str | 是否返回有效结果，取值"success \| fail"|
| results  | json | 检测结果数组，数组每个元素中包含'label'、'confidence'、'topleft'和'bottomright'4个字段的处理结果；当status为fail时，results为空。|


results中的字段实例如下：

```
{
	"status": "success",  # 是否返回有效结果，取值"success \| fail"
	"results": [
        {
            "label": "caries_middle", # 检测结果的标签
		    "confidence": 0.6430898904800415, # 检测结果的置信度
		    "topleft": [1332, 1897], # 检测结果的左上角坐标
		    "bottomright": [1356, 1922] # 检测结果的右下角坐标
	    }, 
        {
            "label": "caries_middle",
            "confidence": 0.6489260196685791,
            "topleft": [1353, 1896],
            "bottomright": [1379, 1922]
        }, 

        ...

        {
            "label": "caries",
            "confidence": 0.7274314165115356,
            "topleft": [2101, 1804],
            "bottomright": [2137, 1833]
        }
    ]
}
```