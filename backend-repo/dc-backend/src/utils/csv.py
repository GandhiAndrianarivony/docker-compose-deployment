import os
import glob
from datetime import datetime
import pandas as pd

def concat(glob_pattern, output_dir, filename):
    
    date = datetime.today().isoformat().split("T")[0]
    
    dfs = []

    for f in glob.glob(glob_pattern):
        try:
            df = pd.read_csv(f)
            dfs.append(df)
            print(f)
        except:
            pass

    df = pd.concat(dfs)
    
    print(df.shape)
    
    output_fname = f"{output_dir}/{filename}-{date}.txt"
    
    df.to_csv(output_fname)
    return output_fname 