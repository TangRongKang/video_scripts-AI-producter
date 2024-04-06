import streamlit as st
from utils_learning import generate_script
#给网站添加标题
st.title("🎦视频脚本生成器")
#侧边栏展示用户API密钥输入和获取OPENAI API密钥官方网址
with st.sidebar:
    openai_api_key = st.text_input("请输入您的API密钥：",type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
#用户输入自己想要的视频主题
subject = st.text_input("💡 请输入您的视频主题")
#用户输入视频时长,min_value,max_value,value,step必须同为浮点数或者整数
video_length = st.number_input("请输入视频的大致时长：（单位：分钟）",min_value= 0.1,step=0.1)
creativity = st.slider("⭐请输入视频脚本的创造力（数字越小越严谨，越大更具有创造力）",min_value=0.1,max_value=1.3,value=0.3,step=0.1)
#用户提交
submit = st.button("点击生成脚本")
#判断用户是否提供全部数据，并进行提示
if submit and not openai_api_key:
    st.info("请输入您的API密钥")
    #没有的话停止执行下面的代码
    st.stop()
if submit and not subject:
    st.info("请输入您的视频主题")
    # 没有的话停止执行下面的代码
    st.stop()
if submit and not video_length >= 0.1:
    st.info("请调整视频时长大于等于0.1分钟")
    # 没有的话停止执行下面的代码
    st.stop()
if submit:
    #网站运行中，给用户展示网站运行中
    with st.spinner("AI正在思考中，请稍等..."):
        search_result,title,script = generate_script(subject,video_length,creativity,openai_api_key)
    #提示用户运行成功
    st.success("视频脚本已生成！")
    #添加副标题
    st.subheader("❤ 标题：")
    st.write(title)
    st.subheader("❤ 视频脚本：")
    st.write(script)
    #维基百科搜索结果用折叠展开组件
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)
