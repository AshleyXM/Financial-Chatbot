# **[Demo-Video-Click-Here](https://www.youtube.com/watch?v=D6i6AI3S7YQ)**

- 视频上传到Youtube，国内访问需要科学上网

# **Demo-Gif**

![demo-1.gif](https://github.com/AshleyXM/Financial-Chatbot/blob/master/demo/demo-1.gif)


# 配置环境（python==3.6.2）

1. 下载zip包或者git clone

2. 进入Financial-Chatbot目录，打开Anaconda Prompt，激活环境

3. 在命令行中输入：

   ```python
   pip install -r requirements.txt
   ```

4. 友情提示:建议使用国内镜像源安装第三方库，比如Tsinghua,USTC和Douban的都不错！

   ```python
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   或
   pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
   或
   pip install -i http://pypi.douban.com/simple/ -r requirements.txt
   ```

   当然，如果你会科学上网，那么只需要开启你的全局代理即可。如下使用：

   ```python
   pip install 第三方库名 --proxy=地址:端口
   ```

# 说明

- 本程序实现的是英文的股票OHLC问答机器人financebot，是基于rasa-nlu 0.15.1版本及其支持的外部组件实现的

- rasa的pipeline配置如下：

  ```python
  language: "en"
  
  pipeline: "spacy_sklearn"
  ```

# 运行bot

1. 首先，你需要通过[BotFather](https://telegram.me/botfather)创建一个属于你自己的机器人，获取api token
2. 然后只需要将克隆的项目放到Pycharm里
3. 将申请到的独一无二的api token取代项目里的main.py文件的<your  telegram token>，并修改下一行的chat_id（获取机器人的chat_id）
4. 最后运行该项目，即可实现与financebot的股票问询对话啦！

# **参考资料**

[python-telegram-bot官方文档](https://pypi.org/project/python-telegram-bot/3.4/)

[yfinance官方文档](https://pypi.org/project/yfinance/)

Yahoo Finance API[参考文档](https://aroussi.com/post/python-yahoo-finance)

[美股列表](http://vip.stock.finance.sina.com.cn/usstock/ustotal.php)

