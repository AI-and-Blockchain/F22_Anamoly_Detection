import numpy as np
import pandas as pd

def BENFORD(n, B):
    def ben(d):
        return 1/np.log(B) * np.sum([np.log(1 + 1/(k*B+d)) for k in range(B**(n-1), B**n-1)])
    return ben

def create_feature_dataframe(data_df):
    def benfords(values, idx):
        idx = idx-1
        def pull_val(value):
            i = idx
            val_str = str(value)
            while val_str[i] in ('0','x'):
                i += 1
            i += idx # Offset to the idx-index from beginning
            return val_str[i]

        counts = {i:0 for i in ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']}
        total = 0
        for value in values:
            total += 1
            # Catch 0x0...0
            if len(set(value.replace('x',''))) == 1:
                continue
            v = pull_val(value)
            if v == '0':
                continue
            counts[pull_val(value)] += 1
        return [v/total for _,v in counts.items()]

    def chi_square(counted, expected):
        stat = 0
        for count, expectation in zip(counted, expected):
            stat += (count - expectation)**2 / expectation
        return stat

    bens_first = [BENFORD(1, 16)(d) for d in range(1,16)]
    bens_second = [BENFORD(2, 16)(d) for d in range(1,16)]
    addr_from_df = data_df.sort_values(by=['from'], ignore_index=True)
    addr_to_df = data_df.sort_values(by=['to'], ignore_index=True)
        
    feature_dict = {
        "total_count": [],
        "in_count": [],
        "in_unique": [],
        "in_value_avg": [],
        "in_value_med": [],
        "in_value_std": [],
        "in_gas_limit_avg": [],
        "in_gas_limit_med": [],
        "in_gas_limit_std": [],
        "from_benfords_first": [],
        "from_benfords_second": [],
        "out_count": [],
        "out_unique": [],
        "out_value_avg": [],
        "out_value_med": [],
        "out_value_std": [],
        "out_gas_limit_avg": [],
        "out_gas_limit_med": [],
        "out_gas_limit_std": [],
        "to_benfords_first": [],
        "to_benfords_second": [],
        "merged_benfords_first": [],
        "merged_benfords_second": [],
    }
    
    feature_dict["in_count"].append(len(addr_to_df))
    
    if len(addr_to_df) != 0:
        feature_dict["in_unique"].append(len(addr_to_df["from"].unique()))

        addr_to_desc = addr_to_df.describe()

        feature_dict["in_value_avg"].append(addr_to_desc["value"]["mean"])
        feature_dict["in_value_med"].append(addr_to_desc["value"]["50%"])
        feature_dict["in_value_std"].append(addr_to_desc["value"]["std"])

        feature_dict["in_gas_limit_avg"].append(addr_to_desc["gasLimit"]["mean"])
        feature_dict["in_gas_limit_med"].append(addr_to_desc["gasLimit"]["50%"])
        feature_dict["in_gas_limit_std"].append(addr_to_desc["gasLimit"]["std"])
    else:
        feature_dict["in_unique"].append(0)
        feature_dict["in_value_avg"].append(0.0)
        feature_dict["in_value_med"].append(0.0)
        feature_dict["in_value_std"].append(0.0)
        feature_dict["in_gas_limit_avg"].append(0.0)
        feature_dict["in_gas_limit_med"].append(0.0)
        feature_dict["in_gas_limit_std"].append(0.0)
    
    if len(addr_to_df["from"]) == 0:
        feature_dict["from_benfords_first"].append(0.)
        feature_dict["from_benfords_second"].append(0.)
    else:
        from_first_benfords = benfords(addr_to_df["from"], 1)
        from_second_benfords = benfords(addr_to_df["from"], 2)
        from_first_chi_squared = chi_square(from_first_benfords, bens_first)
        from_second_chi_squared = chi_square(from_second_benfords, bens_second)
        feature_dict["from_benfords_first"].append(from_first_chi_squared)
        feature_dict["from_benfords_second"].append(from_second_chi_squared)


    feature_dict["out_count"].append(len(addr_from_df))
    
    if len(addr_from_df) != 0:
        feature_dict["out_unique"].append(len(addr_from_df["to"].unique()))

        addr_from_desc = addr_from_df.describe()

        feature_dict["out_value_avg"].append(addr_from_desc["value"]["mean"])
        feature_dict["out_value_med"].append(addr_from_desc["value"]["50%"])
        feature_dict["out_value_std"].append(addr_from_desc["value"]["std"])

        feature_dict["out_gas_limit_avg"].append(addr_from_desc["gasLimit"]["mean"])
        feature_dict["out_gas_limit_med"].append(addr_from_desc["gasLimit"]["50%"])
        feature_dict["out_gas_limit_std"].append(addr_from_desc["gasLimit"]["std"])
    else:
        feature_dict["out_unique"].append(0)
        feature_dict["out_value_avg"].append(0.0)
        feature_dict["out_value_med"].append(0.0)
        feature_dict["out_value_std"].append(0.0)
        feature_dict["out_gas_limit_avg"].append(0.0)
        feature_dict["out_gas_limit_med"].append(0.0)
        feature_dict["out_gas_limit_std"].append(0.0)
    
    feature_dict["total_count"].append(len(addr_to_df) + len(addr_from_df))
    
    if len(addr_from_df["to"]) == 0:
        feature_dict["to_benfords_first"].append(0.)
        feature_dict["to_benfords_second"].append(0.)
    else:
        from_first_benfords = benfords(addr_from_df["to"], 1)
        from_second_benfords = benfords(addr_from_df["to"], 2)
        from_first_chi_squared = chi_square(from_first_benfords, bens_first)
        from_second_chi_squared = chi_square(from_second_benfords, bens_second)
        feature_dict["to_benfords_first"].append(from_first_chi_squared)
        feature_dict["to_benfords_second"].append(from_second_chi_squared)
    
    if len(addr_from_df["to"]) == 0:
        mbf = feature_dict["from_benfords_first"][-1]
        mbs = feature_dict["from_benfords_second"][-1]
    elif len(addr_to_df["from"]) == 0:
        mbf = feature_dict["to_benfords_first"][-1]
        mbs = feature_dict["to_benfords_second"][-1]
    else:
        merged_addresses = pd.concat([addr_from_df["to"], addr_to_df["from"]])
        merged_benfords_first = benfords(merged_addresses, 1)
        merged_benfords_second = benfords(merged_addresses, 2)
        mbf = chi_square(merged_benfords_first, bens_first)
        mbs = chi_square(merged_benfords_second, bens_second)
    
    feature_dict["merged_benfords_first"].append(mbf)
    feature_dict["merged_benfords_second"].append(mbs)

    return pd.DataFrame(feature_dict).fillna(0)

def MDM(X, MUS, SIGMAS):
    return np.sqrt((X-MUS).T @ np.linalg.inv(SIGMAS) @ (X-MUS))