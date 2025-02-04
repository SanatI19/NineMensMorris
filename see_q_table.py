import pickle
import pandas as pd

# with open("white_q_table.pkl", "rb") as f:
#     q_table = pickle.load(f)

# # df = pd.DataFrame(data)

# import pandas as pd

# # Flatten the nested dictionary into a list of dictionaries
# flattened_q_table = [
#     {"State": state, "Action": action, "Q-Value": q_value}
#     for state, actions in q_table.items()
#     for action, q_value in actions.items()
# ]

# # Convert the flattened list to a DataFrame
# df = pd.DataFrame(flattened_q_table)


# df.to_csv("output.csv", index=False)



with open("white_q_table.pkl", "rb") as f:
    q_table = pickle.load(f)


first_key, first_value = next(iter(q_table.items()))
# print(f"First entry: {first_key}: {first_value}")
# print(first_key)
# print(type(first_key))
# print(q_table[first_key])
# print(data)  # Prints the contents
first_entry = list(q_table.items())
# print(first_entry[0][0])
# for i in range(len(first_entry)):
#     print(first_entry[i][1])
print(len(first_entry))
print(first_entry[10000:10010][1])
# print(f"First entry: {first_entry[0]}: {first_entry[1]}")
position = (('W', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),1,'B',False)
# print(position)
# print(type(position))
# position = (('W', None, 'W', None, None, None, None, 'B', None, 'B', None, None, None, None, None, None, None, None, None, None, None, None, None, None),1,'W',False)

# print(q_table[position])
# print(len(q_table))
