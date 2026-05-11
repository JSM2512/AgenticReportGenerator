import streamlit as st
from state_graph_module import build_graph

st.set_page_config(page_title="Orchestrator Worker Demo")

st.title("Orchestrator Worker – Report Generator")
st.write("Enter a topic to automatically generate a structured report using a multi-step orchestration workflow.")

topic = st.text_input("Report topic", value="Agentic AI RAGs")
generate_btn = st.button("Generate Report")

if generate_btn and topic:
    graph = build_graph()
    state = graph.invoke({"topic": "create a report on "+topic})

    st.subheader("Final Report")
    st.markdown(state.get("final_report", "No report generated."))

    if hasattr(graph, "get_graph"):
        try:
            img_bytes = graph.get_graph().draw_mermaid_png()
            st.image(img_bytes, caption="Workflow Graph")
        except Exception as e:
            st.info("Cannot render graph image. Error: %s" % e)