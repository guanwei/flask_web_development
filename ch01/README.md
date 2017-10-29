## 第一章：安装

### 1.1 使用虚拟环境

安装virtualenv
```
$ pip install virtualenv
```

检查系统是否安装了virtualenv
```
$ virtualenv --version
```

创建Python虚拟环境，一般虚拟环境会被命名为`venv`
```
$ virtualenv venv
```

激活这个虚拟环境（Linux和Mac OS X系统）
```
$ source venv/bin/activate
```

激活这个虚拟环境（Windows系统）
```
$ venv\Scripts\activate
```

激活后的虚拟环境，命令提示符前会加入环境名
```
(venv) $
```

退出虚拟环境
```
$ deactivate
```

### 1.2 使用pip安装Python包

在虚拟环境中安装Flask
```
(venv) $ pip install flask
```

可以进入Python解释器，尝试导入Flask，如果没有看到错误提醒，说明Flask已正确安装
```
(venv) $ python
>>> import Flask
>>>
```