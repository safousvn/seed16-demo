{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;\f2\fnil\fcharset0 STIXTwoMath-Regular;
}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28860\viewh18120\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import time\
import streamlit as st\
import requests\
\
st.set_page_config(page_title="Seed 1.6 Auto Caller", layout="wide")\
\
st.title("
\f1 \uc0\u55357 \u56960 
\f0  Seed 1.6 Auto Caller Dashboard")\
st.caption("Automatically call Seed 1.6 Chat API and monitor token usage in real time.")\
\
# --- Secrets ---\
API_KEY = st.secrets.get("ARK_API_KEY", None)\
\
if not API_KEY:\
    st.error("
\f1 \uc0\u10060 
\f0  Missing ARK_API_KEY in Streamlit Secrets.")\
    st.stop()\
\
# --- Initialize ---\
if "total_calls" not in st.session_state:\
    st.session_state.total_calls = 0\
if "total_tokens" not in st.session_state:\
    st.session_state.total_tokens = 0\
\
# --- API Settings ---\
API_URL = "https://ark.byteplusapi.com/v1/chat/completions"\
MODEL_NAME = "seed-1.6"\
\
prompt_text = st.text_area("
\f1 \uc0\u55358 \u56800 
\f0  Prompt for Seed 1.6:", "Hello Seed, tell me something creative!", height=100)\
interval = st.number_input("
\f2 \uc0\u9201 
\f0  Call Interval (seconds):", 0.5, 60.0, 2.0)\
auto_run = st.checkbox("Start Auto-Calling", value=False)\
\
log_area = st.empty()\
\
def call_seed_api():\
    headers = \{\
        "Authorization": f"Bearer \{API_KEY\}",\
        "Content-Type": "application/json"\
    \}\
    data = \{\
        "model": MODEL_NAME,\
        "messages": [\{"role": "user", "content": prompt_text\}],\
        "max_tokens": 100\
    \}\
\
    start = time.time()\
    response = requests.post(API_URL, headers=headers, json=data)\
    latency = time.time() - start\
\
    if response.status_code == 200:\
        result = response.json()\
        usage = result.get("usage", \{\})\
        tokens = usage.get("total_tokens", 100)\
        st.session_state.total_tokens += tokens\
        st.session_state.total_calls += 1\
        return \{"ok": True, "latency": latency, "tokens": tokens\}\
    else:\
        return \{"ok": False, "error": response.text\}\
\
if auto_run:\
    st.success("
\f1 \uc0\u9989 
\f0  Auto-calling is running...")\
    progress = st.progress(0)\
    for i in range(1000000):  # effectively infinite loop\
        result = call_seed_api()\
        if result["ok"]:\
            log_area.write(f"
\f1 \uc0\u9989 
\f0  Call \{st.session_state.total_calls\} | Tokens: \{result['tokens']\} | Latency: \{result['latency']:.2f\}s")\
        else:\
            log_area.write(f"
\f1 \uc0\u10060 
\f0  Error: \{result['error']\}")\
        st.metric("Total Calls", st.session_state.total_calls)\
        st.metric("Total Tokens", st.session_state.total_tokens)\
        time.sleep(interval)\
        progress.progress((i % 100) / 100)\
else:\
    st.info("
\f1 \uc0\u55357 \u57314 
\f0  Click checkbox above to start auto-calling.")\
}