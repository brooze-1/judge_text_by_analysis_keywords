## 🍭文本分词脚本

## 🍝一、前言
之前写过一个[文本关键字分析](https://blog.csdn.net/booze_/article/details/127146221)的脚本，但是那个脚本还绑定了一些其他的功能，相当于有些冗杂了☠，这里我将文本分词功能拎出来单独写，然后还在之前的文本分词中**添加**了一些**其他的功能**😎，**像是添加停用词以及添加分词等功能**。

## 🍛二、开发历程
### 1.需求分析🥝
首先我希望它能**有这么几个功能**🙄：
- **统计**一篇文章中，**每个词出现的次数**并以`词：次数`的形式在终端输出，并以这种形式保存在文件夹中。
- 根据词出现的次数**对词进行排序**，可以自定义排序的方向，升序或者降序。
- **筛选出指定长度的词**，比如说只筛选出一篇文章中长度大于3的词。
- 自定义**展示以及保存排序后的前多少个词**。
- 可以 **添加停用词，添加停用词是什么意思呢？** 就是除去分词产生的一些不需要的词，像是因为、所以、例如、即使这类没有意义的词，就在分词结果中去除掉。
- 可以 **自定义词语，自定义词语是什么意思？** 比如"中国的"是一个词，"年轻人"是一个词，当直接使用jieba库进行分词时，可能就会把"中国的年轻人"分成两个词，但是我们处于某种需求需要将"中国的年轻人"作为一个词，而不需要将它分开，这个时候就要将"中国的年轻人"这个词告诉jieba分词的时候不对它进行拆开，这就相当于自定义词语。

项目的**目录结构**像是这样：
```
----judge_text_by_analysis_keywords\
    |----.idea\
    |----add_words_to_jieba\          # 用于存储添加词的txt文本
    |    |----readme.md						
    |    |----user_dict.txt
    |----analysis_result\					# 用于存储文本分词后的分析结果
    |    |----(result)test.txt
    |    |----readme.md
    |----main.py                             # 主函数
    |----stop_words\                      # 用于存储停用词的txt文本
    |    |----readme.md
    |    |----stopword.txt
    |----wait_to_analysis\             # 用于存储待分词的txt文本
    |    |----readme.md
    |    |----test.txt
```
### 2.参数说明🥥
**keywords_analysis类有六个参数**🐱‍🏍：
- **filename** - **用于存储待分析txt文件的名称**，**注意**传入这个参数的时候，只需要传入文件名+后缀即可不需要带上路径，例"test.txt"千万不要写出"./wait_to_analysis/test.txt"，因为我在代码中默认写了是从wait_to_analysis文件夹下读取文件，所以注意要将待分析的文本放在wait_to_analysis文件夹下再进行操作。
- **stop_words_filename** - **用于接收停用词的txt文件**，**注意**传入的txt文件，需要放在stop_words文件夹下，传入这个参数的时候，只需要传入文件名+后缀即可不需要带上路径，例"stopword.txt"千万不要写出"./stop_words/stopword.txt"，因为我在代码中默认写了是从stop_words文件夹下读取停用词txt文件，所以注意要将停用词文本放在stop_words文件夹下再进行操作。
- **user_dict_filename** - **用于接收用户自定义词的txt文件**，**注意**传入的txt文件，需要放在add_words_to_jieba文件夹下，传入这个参数的时候，只需要传入文件名+后缀即可不需要带上路径，例"userdict.txt"千万不要写出"./add_words_to_jieba/userdict.txt"，因为我在代码中默认写了是从add_words_to_jieba文件夹下读取用户自定义词的txt文件，所以注意要将停用词文本放在add_words_to_jieba文件夹下再进行操作。
- **up_or_down** - up_or_down(bool)参数**用来选择是升序排列还是降序排列**，升序和降序是相对于关键词在文章中的出现次数来排序的(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True。
- **list_keywords** - list_keywords(int)参数是设**置展示的关键词条数以及存储的关键词条数**，默认值为10，即默认展示和存储前10个关键词，当真实关键词条数小于list_keywords，将真实关键词条数赋值给list_keywords。
- **len_keywords** - len_keywords(int)参数是用于**筛选关键词长度大于等于len_keywords的关键词**,默认值为3，即默认筛选长度大于3的关键词，就是**筛选出大于指定长度的关键词**。


### 3.演示效果🍇
待分词文本：
```
“躺平”，当下在中国的年轻人中成为了一个网络流行语，意思是他们更愿意躺下，降低自己的消费欲望，远离名利竞争。
激烈的升学竞争，紧张忙碌的996工作时间表（从早上9点工作到晚上9点，一周六天），还有飞涨的房价都让很多年轻人感到十分沮丧。有些人甚至认为无论他们怎样努力都无法成功，既然如此，干嘛不先躺下呢？
这些声音反映了当代中国社会年轻人对生活的不同态度。它一方面警示我们不要让国人变得不思进取、无欲无求；另一方面，它更多的是自嘲。不过我们不应夸大这种悲观情绪，政府正在积极寻求办法，试图解决年轻人关心的问题，这是件好事。
与一些人选择消极躺下相比，更多的年轻人则选择对工作恪尽职守。六万七千多名科学家和工程师献身于中国的航天事业，他们的平均年龄只有36岁，这比发达国家的同行们大约年轻了15岁。
成功不应该仅仅用名利来衡量。年轻人，如果累了就躺下，但不要让自己被压垮。
```
分词结果：
```
年轻人:5
工作:3
名利:2
竞争:2
成功:2
中国:2
选择:2
躺平:1
中国的年轻人:1
网络:1
```

<center><img src="https://img-blog.csdnimg.cn/0b25e76606de4d49a8fa7481c227cd2a.gif" width="85%"></center>



## 🍕三、脚本的发文平台及开源平台
[github仓库地址🙈]()<br>[gitee仓库地址🙉]()<br>[博客首页🙊](https://blog.csdn.net/booze_/article/details/127166990)



## ☕请我喝卡布奇诺

如果本仓库对你有帮助，可以请作者喝杯卡布奇诺☜(ﾟヮﾟ☜)

<center><img src="https://user-images.githubusercontent.com/112611204/192464009-5ecf272b-c818-4fff-9569-7f3d42d5042b.png" width="40%"></center>



