import pandas as pd

def determine_num_reps(input_data_row_count, num_recors):
    num_reps = num_recors / input_data_row_count
    if not num_reps.is_integer(): raise ValueError("must be divisible")
    return int(num_reps)

def replicate_df(input_df, num_recs): 
    num_reps = determine_num_reps(len(input_df.index), num_recs)
    return input_df.loc[input_df.index.repeat(num_reps)].reset_index(drop=True)


df = pd.read_csv("./test.csv")
print(df.count())
print("\n")
new_df = replicate_df(df, 9)
print(new_df.count())
print("\n")