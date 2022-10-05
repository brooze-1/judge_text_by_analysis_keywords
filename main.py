# 开发时间：2021/10/29  18:49
import jieba

class keywords_analysis(object):
    def __init__(self, filename, stop_words_filename=None, user_dict_filename=None, up_or_down=True,list_keywords=10, len_keywords=2):
        # self.filename用于存储待分析txt文件的名称
        self.filename = filename
        # self.words_dic(dict)用于存储关键词及关键词出现的次数
        self.words_dic = {}
        # self.word_length(int)用于限制关键词的长度 默认关键词的长度为2
        self.len_keywords = len_keywords
        # 将self.words_dic中的字典数据转换成列表数据并且排序好存给变量self.sort_lst(list)
        self.sort_lst = None
        # self.up_or_down(bool)用于决定根据关键词次数排序时是升序还是降序 默认是降序排序
        self.up_or_down = up_or_down
        # list_keywords(int)参数是默认的展示的关键字条数以及存储的关键字条数，默认值为10，即默认展示和存储前10个关键字，当真实关键字条数小于list_keywords，将真实关键字条数赋值给list_keywords
        self.list_keywords = list_keywords
        # self.stop_words_filename接收txt文件（除去不需要的词） 默认值为空
        self.stop_words_filename = stop_words_filename
        # self.stopwords_lst(list)是用于存储停用词的列表
        self.stopwords_lst=[]
        # self.user_dict用于接收txt文件(添加分词) 默认值为空
        self.user_dict_filename = user_dict_filename


    def get_filename(self):
        '''从文件路径中获取文件名'''
        pass


    def stop_words_list(self):
        """
        创建停用词列表，未传入文件名时默认为空列表
        :return:
        """
        if self.stop_words_filename:
            self.stopwords_lst = [word.strip() for word in open('stop_words/{}'.format(self.stop_words_filename),"r", encoding='UTF-8').readlines()]
        # print(self.stopwords_lst)


    def get_words_dict(self):
        """
        获取每个关键词及其出现次数存储在字典中
        :return:
        """
        f = open("wait_to_analysis/{}".format(self.filename),"r",encoding="utf8")
        content = f.read()
        f.close()
        if self.user_dict_filename:
            jieba.load_userdict("add_words_to_jieba/{}".format(self.user_dict_filename))
        words_lst = jieba.lcut(content)
        for word in words_lst:
            if word not in self.stopwords_lst:
                if len(word)<self.len_keywords:
                    continue
                else:
                    self.words_dic[word] = self.words_dic.get(word,0) + 1
            else:
                continue

        return None


    def sort_words(self):
        """
        将self.words_dic转换成列表形式 进行排序 默认采用降序排序
        :return:
        """
        items = list(self.words_dic.items())
        self.sort_lst =  sorted(items,key=lambda x:x[1],reverse=self.up_or_down)
        return None


    def up_to_file(self):
        """
        将关键词及关键词次数存储进文件
        :return:
        """
        f = open("analysis_result/(result){}".format(self.filename),"w",encoding="utf8")

        if len(self.sort_lst) < self.list_keywords:
            self.list_keywords = len(self.sort_lst)
        for i in range(self.list_keywords):
            k, v = self.sort_lst[i]
            f.write("{}:{}\n".format(k, v))
        f.close()

        # for k,v in self.sort_lst:
        #     f.write("{}:{}\n".format(k,v))
        # f.close()


    def output(self):
        """
        将分析关键词及关键词出现次数输出
        :return:
        """
        if len(self.sort_lst)< self.list_keywords:
            self.list_keywords = len(self.sort_lst)

        for i in range(self.list_keywords):
            k, v = self.sort_lst[i]
            if i < self.list_keywords - 1:
                print("{}:{}".format(k, v), end=",")
            else:
                print("{}:{}".format(k, v))

        return None

        # for k,v in self.sort_lst:
        #     print("{}:{}".format(k,v))
        # return None


    def main(self):
        """
        主函数
        :return:
        """
        self.stop_words_list()
        self.get_words_dict()
        self.sort_words()
        self.up_to_file()
        self.output()


if __name__=="__main__":
    obj = keywords_analysis(filename="test.txt",user_dict_filename="user_dict.txt",stop_words_filename="stopword.txt")
    obj.main()