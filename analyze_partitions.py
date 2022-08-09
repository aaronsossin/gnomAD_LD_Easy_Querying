import numpy as np
import pandas as pd
import pickle 

result_df = pd.DataFrame(columns=["chromosome","partitions","mean_hits_per_partition","# >5000","# <5000"])
for i in range(1,23):
    partitions = pickle.load(open("/oak/stanford/groups/zihuai/gnomAD/LD_Scores/nearly_independent_Beriza/partitions/nfe3/partitions_for_" + str(i) + ".pickle","rb"))[str(i)]
    print(len(partitions))
    print(partitions[0])
    print(partitions[10])
    mean_hits = np.mean([len(j) for j in partitions])
    big_partitions = np.sum([len(j) > 4000 for j in partitions])
    print(big_partitions)
    small_partitions = len(partitions) - big_partitions
    print(small_partitions)
    result_df.loc[len(result_df)] = [str(i),len(partitions),mean_hits, big_partitions,small_partitions]
result_df.loc[len(result_df)] = ["total",np.sum(result_df["partitions"]),"n/a",np.sum(result_df["# >5000"]),np.sum(result_df["# <5000"])]
result_df.to_csv("meta_partition_result_nfe_testing.csv")
