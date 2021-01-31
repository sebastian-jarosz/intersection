import numpy as np


class Point:
    def __init__(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    def __str__(self):
        return "x = " + str(self.x_coordinate) + ", y = " + str(self.y_coordinate)


class LineSegment:
    def __init__(self, first_endpoint, second_endpoint):
        self.first_endpoint = first_endpoint
        self.second_endpoint = second_endpoint


def get_vector_from_two_points(first_point, second_point):
    x1 = first_point[0]
    y1 = first_point[1]
    x2 = second_point[0]
    y2 = second_point[1]
    return np.array([x2 - x1, y2 - y1])


# Working points - intersection -1,1
A = np.array([-2, 0])
B = np.array([0, 2])
C = np.array([-2, 2])
D = np.array([0, 0])

# Working points - intersection -3, 1
# A = np.array([-4, 0])
# B = np.array([0, 4])
# C = np.array([-4, 1])
# D = np.array([-2, 1])

# Working points - intersection -4, 0
# A = np.array([-4, 0])
# B = np.array([0, 4])
# C = np.array([-4, 0])
# D = np.array([-2, 0])

# Working points - no intersection
# A = np.array([-4, 0])
# B = np.array([0, 4])
# C = np.array([-2, 0])
# D = np.array([0, 0])

# Working points - collinear
A = np.array([-4, 0])
B = np.array([0, 4])
C = np.array([-3, 1])
D = np.array([-1, 3])

first_segment = LineSegment(A, B)
second_segment = LineSegment(C, D)

vector_AB = get_vector_from_two_points(A, B)
vector_CD = get_vector_from_two_points(C, D)
cross_product_AB_CD_vectors = np.cross(vector_AB, vector_CD)

t = np.cross(C - A, vector_CD) / np.cross(vector_AB, vector_CD)
u = np.cross(C - A, vector_AB) / np.cross(vector_AB, vector_CD)

print("Vector AB: " + str(vector_AB))
print("Vector CD: " + str(vector_CD))
print("Cross AB x CD: " + str(cross_product_AB_CD_vectors))
print("t = " + str(t))
print("u = " + str(u))

if cross_product_AB_CD_vectors == 0 and np.cross(C - A, vector_AB) == 0:
    t0 = np.dot(C - A, vector_AB) / np.dot(vector_AB, vector_AB)
    t1 = t0 + (np.dot(vector_CD, vector_AB) / np.dot(vector_AB, vector_AB))
    if np.dot(vector_CD, vector_AB) < 0:
        print("t1 = " + str(t1))
        print("t0 = " + str(t0))
        begin_of_intersection_segment = A + np.dot(t1, vector_AB)
        end_of_intersection_segment = A + np.dot(t0, vector_AB)
        print("Intersection segment from " + str(begin_of_intersection_segment) + " to " + str(
            end_of_intersection_segment))
    else:
        print("t0 = " + str(t0))
        print("t1 = " + str(t1))
        begin_of_intersection_segment = A + np.dot(t0, vector_AB)
        end_of_intersection_segment = A + np.dot(t1, vector_AB)
        print("Intersection segment from " + str(begin_of_intersection_segment) + " to " + str(
            end_of_intersection_segment))
elif cross_product_AB_CD_vectors == 0 and np.cross(C - A, vector_AB) != 0:
    print("Segments don't intersect")
elif cross_product_AB_CD_vectors != 0 and 0 <= t <= 1 and 0 <= u <= 1:
    intersection_point1 = A + np.dot(t, vector_AB)
    intersection_point2 = C + np.dot(u, vector_CD)
    print("Segments intersect")
    print("First point: " + str(intersection_point1))
    print("Second point: " + str(intersection_point2))
else:
    print("Segments don't intersect")
