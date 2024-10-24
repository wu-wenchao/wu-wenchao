from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


PROMPT_TEMPLATE = """
你是一位数据分析助手，使用中文回答，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   {"answer": "<你的答案写在这里>"}
例如：
   {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. 如果用户的请求适合返回条形图或柱状图时，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

6.如果用户的请求适合返回饼状图，按照这样的格式回答：
   {"pie": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
注意：我们只支持四种类型的图表："bar", "line" , "scatter","pie"。


请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围，"data"列表中要罗列所有符合要求的数据，不要省略。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下： 
"""


def dataframe_agent(openai_api_key, df, query):
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       temperature=0,
                       openai_api_key=openai_api_key,
                       openai_api_base="https://api.aigc369.com/v1")

    agent = create_pandas_dataframe_agent(llm=model,
                                          df=df,
                                          allow_dangerous_code=True,
                                          agent_executor_kwargs={"handle_parsing_errors": True},
                                          verbose=True)
    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})
    # 如果response中有“...”，刚删除掉
    if "..." in response["output"]:
        response["output"] = response["output"].replace(", ...", "")
    return response["output"]



