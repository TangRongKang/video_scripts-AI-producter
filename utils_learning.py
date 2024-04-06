from langchain.prompts import ChatPromptTemplate
#从langchain中导入OpenAI模型
from langchain_openai import ChatOpenAI
#引入维基百科搜索模块
from langchain_community.utilities import WikipediaAPIWrapper
#从环境变量获取API—key
#import os

#定义提示模板
def generate_script(subject, video_length,
                    creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human","请为{subject}这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
            视频标题：{title},视频时长：{duration}分钟，生成的脚本长度尽量遵循视频时长的要求。
            要求开头抓住眼球，中间提供干活内容，结尾有精细，脚本格式按照【开头、中间、结尾】分隔。
            整体内容表达方式要尽量轻松有趣，吸引年轻人。
            脚本内容可以结合以下维基百科搜索出的信息，但仅作参考，只结合相关的即可，对不相关的进行忽略：
            '''{wikipedia_search}'''""")
        ]
    )
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity,model = "gpt-3.5-turbo")
    #将提示模板传入model
    title_chain = title_template | model
    script_chain = script_template | model
    #获取AI返回的视频标题
    title = title_chain.invoke({"subject":subject}).content
    #获取wikipedia搜索结果,将搜索语言设置为中文
    search = WikipediaAPIWrapper(lang = "zh")
    search_result = search.run(subject)
    #获取AI返回的脚本内容
    script = script_chain.invoke({"title":title,"duration":video_length,"wikipedia_search":search_result}).content
    return search_result,title,script
#测试
#print(generate_script("sora模型",1,0.75,"sk-2kMZkaS7hkySCft2Ea0e61Dc3e4641D2A47e1f1cD36886Fa"))