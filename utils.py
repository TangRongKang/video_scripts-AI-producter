# 搞定后端逻辑，根据用户输入的视频主题，时长以及创造性获得tile内容，脚本内容和维基百科的搜索结果
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, api_key):
    # 创建标题prompttemplate
    title_prompt = ChatPromptTemplate.from_messages([
        ("human", "请为{subject}这个主题的视频想一个吸引人的标题,用中文回答")
    ])
    # 创建脚本内容prompt tempalte
    script_prompt = ChatPromptTemplate.from_messages([
        ("human", """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
            视频标题：{title},视频时长：{duration}分钟，生成的脚本长度尽量遵循视频时长的要求。
            要求开头抓住眼球，中间提供干活内容，结尾有精细，脚本格式按照【开头、中间、结尾】分隔。
            整体内容表达方式要尽量轻松有趣，吸引年轻人。***用中文进行回答***
            脚本内容可以结合以下维基百科搜索出的信息，但仅作参考，只结合相关的即可，对不相关的进行忽略，一定要用中文进行回答：
            '''{wikipedia_search}'''""")
    ])
    # 创建client model
    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, base_url="https://sg.uiuiapi.com/v1",
                       temperature=creativity)
    # 将提示模板分别传入model得到链
    title_chain = title_prompt | model
    script_chain = script_prompt | model
    # 传入参数，获得ai回答
    title = title_chain.invoke({"subject": subject}).content
    # script先获得维基百科的回答，一同传入
    search_result = WikipediaAPIWrapper(lang="zh").run(subject)
    script = script_chain.invoke({
        "title": title,
        "duration": video_length,
        "wikipedia_search": search_result
    }).content
    # 将title script search_result 一并返回
    return title, script, search_result
