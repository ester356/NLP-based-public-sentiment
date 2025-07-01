# NLP-based-public-sentiment-数据集和爬虫

将绝对路径改为相对路径

clearData.py
这个函数通过以下步骤处理输入的文本：

文本清理：使用 HarvestText 库的 clean_text 方法过滤文本中的特殊字符，保留表情符号。
URL 处理：通过正则表达式移除所有 HTTP 和 HTTPS 链接。
标签内容移除：移除被两个 # 符号包围的内容，通常用于话题标签。
特殊符号处理：移除文本中的《》符号。

globalVariable.py
定义了一个初始化全局变量的函数，用于生成微博爬虫项目所需的数据文件路径。

spiderContent.py
爬取微博内容的 Python 脚本，设计了两种爬取模式：按分类批量爬取和单条微博 URL 爬取。代码整体结构清晰，但存在一些可以优化的地方。

spiderContent.py
微博评论爬取

spiderArticleCategory.py
该代码实现了微博类别的爬取与存储核心功能

clearData1.py
可对特定数据集中的特定列进行清洗
