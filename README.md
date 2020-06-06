### Angelina  
这个小工具的名称源于明日方舟，之前写了批量解压ZIP文件并更名MD5的代码，想着直接做成工具比较好，就用Tkinter简单写了一个，要说为撒不用QT...因为不会，其实Tkinter也是现看了教程😆  

#### 工具功能🎈  
批量解压ZIP文件，支持将解压后的文件更名为MD5  
![example](https://github.com/Applenice/Angelina/blob/master/image/example.png)  

使用要求:  
 - 批量解压: 输入目录内必须只存在ZIP文件，批量解压带密码的ZIP文件时请保证输入目录内各ZIP文件的密码一样  
 - 更名MD5: ZIP文件中存在文件夹，会导致任务中断  

#### 应用场景🎯  
该工具可能应用的场景:  
 - 批量的恶意样本需要解压、更名MD5  

#### 运行环境🔔  
可直接通过release下载，但只在Windows 10下进行了测试，其他环境不做保证  

#### 打包方式🎁  
使用Pyinstaller打包成exe，利用[UPX](https://github.com/upx/upx)进行了压缩，虽然也没压缩多少🤣  
```
pyinstaller -F -w --upx-exclude=vcruntime140.dll --upx-exclude=python37.dll --upx-exclude=ucrtbase.dll -i Angelina.ico --add-data="Angelina.ico;." Angelina.py
```

#### 备注👀  
1、图片转换工具: https://convertico.com/  
