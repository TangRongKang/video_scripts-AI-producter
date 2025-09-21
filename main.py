# 导入streamlit和后端工具
import streamlit as st
from utils import generate_script

# 设置网站标题
st.title("欢迎使用视频脚本生成器><")
# 设置网站侧边栏
with st.sidebar:
    api_key = st.text_input("请输入您的api密钥：", type="password")
    st.markdown("[获取相关api密钥](https://sg.uiuiapi.com/)")

# 获取用户输入title video_langth creativity
subject = st.text_input("💡 请输入您的视频主题")
#用户输入视频时长,min_value,max_value,value,step必须同为浮点数或者整数
video_length = st.number_input("请输入视频的大致时长：（单位：分钟）", min_value=0.2, step=0.1)
creativity = st.slider("⭐请输入视频脚本的创造力（数字越小越严谨，越大更具有创造力）", min_value=0.1, max_value=1.0, value=0.2,step=0.1)

# 提交按钮，设置点击事件运行后端
submit = st.button("点击生成脚本")# 点击返回True

# 提交但没有密钥，subject等给出必要的提示，验证校验
if submit and not subject:
    st.info("请输入您的视频主题")
    st.stop() # 停止执行下面的代码
if submit and not api_key:
    st.info("请输入您的密钥！")
    st.stop()
# 得到返回结果，进行展示
if submit:
    # 网站运行中，给用户展示网站运行中
    with st.spinner("生成中，请耐心等待哦"):
        title, script, search_result = generate_script(subject,video_length,creativity, api_key)
    # 提示运行成功，并进行信息展示
    st.success("视频脚本生成成功！请查收")
    st.subheader("❤ 标题：")
    st.write(title)
    st.subheader("❤ 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)

