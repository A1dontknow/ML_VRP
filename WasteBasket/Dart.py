
# def sort_two_list_together(list1, list2):
#     combined = zip(list1, list2)
#     sorted_combined = sorted(combined, key=lambda x: x[0])
#     return zip(*sorted_combined)
#
#
# # Return list of set of darts in a line of r
# def handle_one_dimenion(darts, darts_id, r):
#     darts, darts_id = sort_two_list_together(darts, darts_id)
#     print(darts, darts_id)
#     result = []
#     for i in range(len(darts) - 1):
#         j = i + 1
#         group = {darts_id[i]}
#
#         while darts[j] - darts[i] <= 2 * r:
#             group.add(darts_id[j])
#             j += 1
#             if j == len(darts):
#                 break
#
#         if len(group) != 1:
#             result.append(group)
#     return result
#
#
# def numPoints(darts, r):
#     # Tach 2 chieu
#     darts_x = [i[0] for i in darts]
#     darts_x_id = [i for i in range(len(darts_x))]
#     darts_y = [i[1] for i in darts]
#     darts_y_id = [i for i in range(len(darts_y))]
#     # Solve tung chieu mot
#     result_x = handle_one_dimenion(darts_x, darts_x_id, r)
#     result_y = handle_one_dimenion(darts_y, darts_y_id, r)
#     # Dung intersect trong set
#     max_ans = 1
#     for set_x in result_x:
#         for set_y in result_y:
#             len_points_same_polar = len(set_x.intersection(set_y))
#             if len_points_same_polar > max_ans:
#                 max_ans = len_points_same_polar
#
#     return max_ans


import numpy as np
from scipy.spatial.distance import cdist

darts = [[-3, 0], [3, 0], [2, 6], [5, 4], [0, 9], [7, 8]]
r = 5

# Convert the darts list to a NumPy array
darts_array = np.array(darts)

# Compute the distance matrix
distance_matrix = cdist(darts_array, darts_array)
group = []
for i in range(len(distance_matrix)):
    same_polar = {i}
    for j in range(len(distance_matrix)):
        if distance_matrix[i][j] <= 2 * r:
            same_polar.add(j)
    if len(same_polar) > 1:
        group.append(same_polar)

print(group)
# Dung intersect trong set
max_ans = 1
for i in range(len(group) - 1):
    for j in range(i + 1, len(group)):
        len_points_same_polar = len(group[i].intersection(group[j]))
        if len_points_same_polar > max_ans:
            max_ans = len_points_same_polar

print(max_ans)



