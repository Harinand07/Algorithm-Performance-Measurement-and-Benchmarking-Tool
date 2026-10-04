import streamlit as st
from benchmark_engine import BenchmarkEngine
from search_analysis import linear_search,binary_search
from code_benchmark import single_loop,nested_loop,factorial_recursive,factorial_iterative

st.set_page_config(page_title="Algorithm Benchmarking Tool",layout="wide")
st.title("Algorithm Performance Measurement & Benchmarking Tool")
st.caption("Lab 2 — execution time, memory usage, operation counts and complexity trends")
engine=BenchmarkEngine()
module=st.sidebar.selectbox("Module",["Search Algorithms","Factorial Programs","Loop-Based Programs"])
if module=="Search Algorithms":
    sizes=st.sidebar.multiselect("Input sizes",[100,1000,10000,50000],default=[100,1000,10000,50000]);target=st.sidebar.number_input("Search target",value=-1,step=1)
    if st.button("Run Search Benchmark"):
        for n in sizes:
            data=list(range(n));engine.run(linear_search,[n],name="Linear Search",arg_builder=lambda _:(data,target));engine.run(binary_search,[n],name="Binary Search",arg_builder=lambda _:(data,target))
elif module=="Factorial Programs":
    sizes=st.sidebar.multiselect("Input sizes",[100,500,900],default=[100,500,900])
    if st.button("Run Factorial Benchmark"):
        engine.run(factorial_recursive,sizes,name="Factorial (Recursive)");engine.run(factorial_iterative,sizes,name="Factorial (Iterative)")
else:
    sizes=st.sidebar.multiselect("Input sizes",[100,1000,10000,50000],default=[100,1000,10000,50000])
    if st.button("Run Loop Benchmark"):
        engine.run(single_loop,sizes,name="Single Loop")
        for n in sizes:
            if n<=5000: engine.run(nested_loop,[n],name="Nested Loop")
            else: st.warning(f"Nested Loop n={n} skipped: {n*n:,} iterations would be impractical to execute.")
if engine.results:
    result=engine.as_dataframe();st.dataframe(result,use_container_width=True);st.line_chart(result.pivot(index="input_size",columns="algorithm",values="time_sec"))
