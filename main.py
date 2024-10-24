import json

import pandas as pd
import streamlit as st

from utils import dataframe_agent
import matplotlib.pyplot as plt


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)
    # elif chart_type == "pie":
    #     st.pyplot(df_data)
    # elif chart_type == "pie":
    #     # 创建饼图
    #     fig, ax = plt.subplots()
    #     ax.pie(df_data.iloc[0], labels=df_data.columns, autopct='%1.1f%%')
    #     ax.axis('equal')  # 确保饼图是圆形
    #     # 显示饼图
    #     st.pyplot(fig)
    # 假设 DataFrame 的第一列是标签，其余列是值（这里只取第一列值作为示例）
    # 注意：实际使用中可能需要更复杂的逻辑来处理多个值的情况
    elif chart_type == "pie":
        # 示例数据
        # labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
        # values = [15, 30, 45, 10]

        labels = []
        values = []
        for i in input_data["data"]:
            labels.append(i[0])
            values.append(i[1])

        # 创建饼图
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # 在 Streamlit 中显示饼图
        st.pyplot()

st.title("动态分析AI助手")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API key](https://api.aigc369.com/token)")

data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area(
    "请介绍输入的数据表，简单介绍之，再提出您关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图、饼状图）：")
button = st.button("生成回答")

if button and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
if button and "df" not in st.session_state:
    st.info("请先上传数据文件")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI正在思考中，请稍等..."):
        response_dict1 = dataframe_agent(openai_api_key, st.session_state["df"], query)
        # st.write(response_dict1)
        response_dict = json.loads(response_dict1)

        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")
        if "pie" in response_dict:
            create_chart(response_dict["pie"], "pie")
