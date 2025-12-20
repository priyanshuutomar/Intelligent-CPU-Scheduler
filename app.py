import streamlit as st
import io, sys
import main_scheduler

st.title("Intelligent CPU Scheduler Simulator")

# -------- USER INPUT --------
n = st.number_input("Enter number of processes", min_value=1, step=1)
tq = st.number_input("Enter Time Quantum (for Round Robin)", min_value=1, step=1)

processes_basic = []
processes_priority = []

st.subheader("Enter Process Details")

for i in range(n):
    st.markdown(f"### Process P{i+1}")
    at = st.number_input(f"Arrival Time P{i+1}", key=f"at{i}")
    bt = st.number_input(f"Burst Time P{i+1}", key=f"bt{i}")
    pr = st.number_input(f"Priority P{i+1}", key=f"pr{i}")

    processes_basic.append([f"P{i+1}", at, bt])
    processes_priority.append([f"P{i+1}", at, bt, pr])

# -------- RUN BUTTON --------
if st.button("Run Scheduler"):
    buffer = io.StringIO()
    sys.stdout = buffer

    main_scheduler.run_all(processes_basic, processes_priority, tq)

    sys.stdout = sys.__stdout__
    output = buffer.getvalue()

    st.subheader("Scheduling Output")
    st.text(output)
