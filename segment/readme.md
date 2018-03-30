### 处理爬取下来的文档
- run.py 执行categorize.py并导出结果到result/

### 生成格式
日期/文章/所有出现过的json文章

### 函数描述
- categorize.py
    ```
    用OptionParser写好了调用命令
    ```

- extracttags.py
    ```
    def ExtractTagsFromFile(file_path, num_of_tags):
        传入: 路径和给定标签数
        返回: 提取出对应文本的关键词(jieba.analyse.extract_tags)
        剔除含有关键词较少的句子后的正文(如删去"扫一扫获取公众号"等)
    ```
    


- tfidf.py  
    def GetTermFreqFromFile(tags, file_path):  
    主函数: 给关键词和文本路径,统计出关键词tags=[]的词频,返回对应字典  
    
- findsimilarpassage.py
    ```
    给一个文本的关键词字典,和一堆文本,判断是否有相似(cos夹角)
    ```

- basicfuncs.py
    ```
    一些常用函数:
    CosinSimilarityForDict(dict1, dict2):
    提取两个字典values作为权重向量,然后计算夹角cos值
    ```
    
- getabstract.py
    ```  
    def GetPassageAbstract(passage, 0.4, 0.3):
        传入: 正文,取词比例,取句子比例
        返回: 剔除含有关键词较少的句子后的正文(如删去"扫一扫获取公众号"等)
    ```