"""
This is a test file for the simulation of the agent's.
"""

#Library Imports
import time
from Agent import Agent
from Utils.Logger import Logger as CLogger
import streamlit as st
from streamlit_elements import elements, mui, nivo, html, dashboard

#Initial Setup
if not 'Agent' in st.session_state:
    st.session_state.Agent = Agent("Agent1")
    
    #Variables
    st.session_state.Logger = CLogger()
    st.session_state.Agents = []
    st.session_state.x = 0

    #Initial Setup
    st.session_state.Logger.logln("[PAI][SIMULATION]: Simulation started.")
    st.session_state.Logger.logln(f"[PAI][SIMULATION]: Creating Agent# {len(st.session_state.Agents)+1}.")
    Agent1 = st.session_state.Agent
    st.session_state.Attributes = Agent1.body.attributes
    
    x = 0

#Fetch Agent pie data
AttributeById = {
    "Physical": ['Energy', 'Health', 'Hunger', 'Sleep'],
    "Mental": ['Focus', 'Stress', 'Mood'],
    "Social": ['Satisfaction', 'RelationshipQuality'],
    "Cognitive": ['Knowledge', 'Confidence'],
    "Environmental": ['Safety', 'Comfort'],
    "Long-Term": ['Fullfillment', 'Progress']
}

CurrentAgent:Agent = st.session_state.Agent


Status_Data = [
    {
    "id": None,
    'data':[
        {
        "attribute": attribute,
        "value": float(details.value),
        }
    ]
    }
    for attribute,details in st.session_state.Attributes.attributes.items()
]

for i in range(len(Status_Data)):
    for key in AttributeById.keys():
        if(Status_Data[i].get('data')[0].get('attribute') in AttributeById[key]):
            print('Match Found:')
            print('Key: ',Status_Data[i].get('data')[0].get('attribute'), 'Set: ',AttributeById[key],'\n')
            Status_Data[i]['id'] = key
            print(Status_Data[i]['id'])
            break

formatted_data = {}

for entry in Status_Data:
    id_key = entry['id'] or 'Other'  # Replace None with a string for grouping
    if id_key not in formatted_data:
        formatted_data[id_key] = {"id": id_key, "data": []}
    for item in entry['data']:
        attribute = item['attribute']
        value = item['value']
        formatted_data[id_key]["data"].append({attribute: value})
        
final_result = [
    {"id": key, "data": value["data"]} for key, value in formatted_data.items()
]

# Transforming data for Nivo RadialBar chart
nivo_data = [
    {
        "id": item["id"],
        "data": [{"x": attr, "y": value} for entry in item["data"] for attr, value in entry.items()]
    }
    for item in final_result
]


print('Mapped Status Data: ',nivo_data)


# Log pie data for debugging
st.session_state.Logger.logln(f"PIE DATA: {nivo_data}")

with elements("nivo_charts"):
    # Use the Radar chart
    with mui.Box(sx={"height": 500}):
        nivo.RadialBar(
            data=nivo_data,
            valueFormat=">-.2f",
            padding={0.4},
            cornerRadius={2},
            margin={ 'top': 40, 'right': 120, 'bottom': 40, 'left': 40 },
            radialAxisStart={ 'tickSize': 5, 'tickPadding': 5, 'tickRotation': 0 },
            circularAxisOuter={ 'tickSize': 5, 'tickPadding': 12, 'tickRotation': 0 },
            legends=[
                {
                    "anchor": 'right',
                    "direction": 'column',
                    "justify": 'false',
                    "translateX": 80,
                    "translateY": 0,
                    "itemsSpacing": 6,
                    "itemDirection": 'left-to-right',
                    "itemWidth": 100,
                    "itemHeight": 18,
                    "itemTextColor": '#999',
                    "symbolSize": 18,
                    "symbolShape": 'square',
                    "effects": [
                        {
                            "on": 'hover',
                            "style": {
                                "itemTextColor": '#000'
                            }
                        }
                    ]
                }
            ],
            theme={
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
            )

while st.session_state.x < 100:
    st.session_state.x+=1
    time.sleep(3)
    st.rerun() #Reloads the webapp
    print("Site Updated")