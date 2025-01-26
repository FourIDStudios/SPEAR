"""
This is a test file for the simulation of the agent's.
"""

#Library Imports
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

    #Initial Setup
    st.session_state.Logger.logln("[PAI][SIMULATION]: Simulation started.")
    st.session_state.Logger.logln(f"[PAI][SIMULATION]: Creating Agent# {len(st.session_state.Agents)+1}.")
    Agent1 = st.session_state.Agent
    st.session_state.Agents.append(Agent1)

#Fetch Agent pie data

CurrentAgent:Agent = st.session_state.Agent

radar_data = [
    {
    "attribute": attribute,
    "value": float(details.value),
    }
    for attribute,details in CurrentAgent.body.attributes.attributes.items()
    ]

DATA = [
    {
        'attribute': 'Attributes',
        **{entry['attribute']: entry['value'] for entry in radar_data}
    }
]

# Format the radar data for each agent attribute as separate values for keys
keys = list(CurrentAgent.body.attributes.attributes.keys())


# Log pie data for debugging
st.session_state.Logger.logln(f"PIE DATA: {radar_data}")

with elements("demo"):
    mui.Typography("Hello, World!", variant="h4")

# Use the Radar chart
    with mui.Box(sx={"height": 500}):
        nivo.Radar(
            data=DATA,
            keys=keys,
            indexBy="taste",  # This is the attribute like "taste"
            valueFormat=">-.2f",
            margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
            borderColor={"from": "color"},
            gridLabelOffset=36,
            dotSize=10,
            dotColor={"theme": "background"},
            dotBorderWidth=2,
            motionConfig="wobbly",
            legends=[
                {
                    "anchor": "top-left",
                    "direction": "column",
                    "translateX": -50,
                    "translateY": -40,
                    "itemWidth": 80,
                    "itemHeight": 20,
                    "itemTextColor": "#999",
                    "symbolSize": 12,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemTextColor": "#000"
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