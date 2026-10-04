import time, tracemalloc
import pandas as pd

class BenchmarkEngine:
    """Runs a function across input sizes and records time, memory and operation count."""
    def __init__(self): self.results=[]
    def run(self, func, input_sizes, name=None, arg_builder=lambda n:(n,)):
        algo_name=name or func.__name__
        for n in input_sizes:
            args=arg_builder(n)
            tracemalloc.start(); start=time.perf_counter()
            result=func(*args)
            elapsed=time.perf_counter()-start
            _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            operations=None; output=result
            if isinstance(result,tuple) and len(result)==2: output,operations=result
            self.results.append({"algorithm":algo_name,"input_size":n,"time_sec":elapsed,"memory_kb":peak/1024,"operations":operations,"result":output,"status":"executed"})
        return self
    def as_dataframe(self): return pd.DataFrame(self.results)

if __name__ == "__main__":
    from search_analysis import linear_search,binary_search
    from code_benchmark import single_loop,nested_loop,factorial_recursive,factorial_iterative
    engine=BenchmarkEngine()
    for n in [100,1000,10000,50000]:
        data=list(range(n))
        engine.run(linear_search,[n],name="Linear Search",arg_builder=lambda _: (data,-1))
        engine.run(binary_search,[n],name="Binary Search",arg_builder=lambda _: (data,-1))
        engine.run(single_loop,[n],name="Single Loop")
        if n <= 5000:
            engine.run(nested_loop,[n],name="Nested Loop")
        else:
            print(f"Nested Loop n={n}: skipped; theoretical operations={n*n:,}")
    engine.run(factorial_recursive,[100,500,900],name="Factorial (Recursive)")
    engine.run(factorial_iterative,[100,500,900],name="Factorial (Iterative)")
    df=engine.as_dataframe();print(df.to_string(index=False));df.to_csv("benchmark_results.csv",index=False)
