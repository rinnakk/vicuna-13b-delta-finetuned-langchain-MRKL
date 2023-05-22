prefix = """Answer the following questions as best you can. You have access to the following tools:

Search: useful for when you need to answer questions about current events
Calculator: useful for when you need to answer questions about math
Chitchat: useful for when you do not need tool to answer questions

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Search, Calculator, Chitchat]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""
ids = []
def process(example):
    example = example.strip()
    if not example.startswith("Question"):
        return None
    lines = example.split("\n")
    prelines = ""
    instances = []
    for i,line in enumerate(lines):
        if line.startswith("Thought:"):
            output = ""
            input = ""
            if "previous steps:" not in line:
                output = line[8:].lstrip()
            output+="\n"+"\n".join(lines[i+1:])
            if "previous steps:" in line:
                input = prelines+line
            else:
                input = prelines+"Thought:"
            input,output = input.strip(),output.strip()
            instances.append([input,output])
        prelines += line+'\n'
    return instances
rawdata = open("examples").read().split("###")
for example in rawdata:
    ret = process(example)
    if ret:
#        for i in range(32):
        for i in range(1):
            ids.extend(ret)
import random
random.shuffle(ids)
##format data
outlist = []
for i,instance in enumerate(ids):
    id_dict = {}
    id_dict["id"] = "identity_"+str(i)
    id_dict["conversations"] = []
    id_dict["conversations"].append({
        "from":"human",
        "value":prefix+"\n\n"+instance[0]
    })
    id_dict["conversations"].append({
        "from":"gpt",
        "value":instance[1]
    })
    outlist.append(id_dict)
import json
#json_str = json.dumps(outlist, indent =2, ensure_ascii= False)
json_str = json.dumps(outlist, indent =2)
with open("my.json","w") as outfile:
    outfile.write(json_str)
