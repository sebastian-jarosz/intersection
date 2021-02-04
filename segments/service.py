from .models import Segment, Point
import numpy as np


def are_intersecting_boolean(segment_ab, segment_cd):
    int_points_amount, int_array = are_intersecting(segment_ab, segment_cd)
    return True if int_points_amount > 0 else False


def is_pair_intersecting_boolean(segments_pair):
    segment_ab = segments_pair.get_first_segment()
    segment_cd = segments_pair.get_second_segment()
    int_points_amount, int_array = are_intersecting(segment_ab, segment_cd)
    return True if int_points_amount > 0 else False


def is_pair_intersecting(segments_pair):
    segment_ab = segments_pair.get_first_segment()
    segment_cd = segments_pair.get_second_segment()
    return are_intersecting(segment_ab, segment_cd)


# Main method to check segments intersection
# Return amount of intersections (Ex. 1 if only one intersection point,
# 2 if intersection is a segment, 0 if no intersection) and
# intersection array (1 dim in case of one intersection point, 2 dim in case of intersection segment else None)
def are_intersecting(segment_ab, segment_cd):
    # Before checking there are no intersection points
    int_points_amount = 0

    # Validate if segments are not points - Special Case
    if are_segments_points(segment_ab, segment_cd):
        int_point = get_intersection_with_point(segment_ab, segment_cd)
        int_points_amount = 1 if int_point is not None else 0
        return int_points_amount, int_point

    point_a = segment_ab.get_first_point()
    point_c = segment_cd.get_first_point()
    vector_ab = segment_ab.get_as_vector()
    vector_cd = segment_cd.get_as_vector()

    # Cross product of vectors AB and CD
    cross_ab_cd = np.cross(vector_ab, vector_cd)
    # Cross product of Point C - Point A and vector AB
    cross_c_sub_a_ab = np.cross(point_c - point_a, vector_ab)

    # Calculate scalar parameters t and u
    t = calc_t(point_c, point_a, vector_ab, vector_cd)
    u = calc_u(point_c, point_a, vector_ab, vector_cd)

    # Uncomment in case of debugging
    # print_debug_data(vector_ab,vector_cd, cross_ab_cd, t, u)

    # Segments are collinear - if intersecting return amount 2 and points (segment begin and segment end)
    # else amount 0 and None
    if cross_ab_cd == 0 and cross_c_sub_a_ab == 0:
        int_segment = calc_int_segment(segment_ab, segment_cd, vector_ab, vector_cd)
        int_points_amount = 2 if int_segment is not None else 0
        return int_points_amount, int_segment
    # Segments are not parallel and have only one intersection point
    elif cross_ab_cd != 0 and 0 <= t <= 1 and 0 <= u <= 1:
        int_point = calc_int_point(point_a, point_c, t, u, vector_ab, vector_cd)
        int_points_amount = 1 if int_point is not None else 0
        return int_points_amount, int_point
    # Segments are parallel and don't intersect or
    # Segments just don't have any intersection point - return amount 0 and None
    else:
        return int_points_amount, None


# Validate if segments are not points
def are_segments_points(segment1, segment2):
    return segment1.are_both_points_equal() or segment2.are_both_points_equal()


# At least one of segment is point - check intersection
# If there is intersection return Point else None
def get_intersection_with_point(segment1, segment2):
    p1 = segment1.get_first_point()
    p2 = segment2.get_first_point()

    # Both segments are points
    if segment1.are_both_points_equal() and segment2.are_both_points_equal():
        # If both points equal return one of them as intersection point (doesn't matter which one)
        return p1 if np.array_equal(p1, p2) else None
    elif segment1.are_both_points_equal():
        # If Segment1 is point return it in case of intersecting with Segment2
        return p1 if is_point_on_segment(p1, segment2) else None
    elif segment2.are_both_points_equal():
        # If Segment2 is point return it in case of intersecting with Segment1
        return p2 if is_point_on_segment(p2, segment1) else None


# If DOT PRODUCT of Segment Vector (Segment as a Vector) and Point from Segment to Provided Point Vector
# is BETWEEN 0 and DOT PRODUCT of two Segment Vectors (Segment as Vector)
# Then point is ON SEGMENT else point IS NOT ON SEGMENT
def is_point_on_segment(point, segment):
    # Point A
    point_from_segment = segment.get_first_point()
    # Vector(A,B)
    segment_vector = segment.get_as_vector()
    # Vector(A, Point)
    points_vector = get_vector_from_two_points(point_from_segment, point)
    # Vector(A,B) * Vector(A, Point) - * represents DOT PRODUCT
    dot_segment_vector_and_points_vector = np.dot(segment_vector, points_vector)
    # Vector(A,B) * Vector(A,B) - * represents DOT PRODUCT
    dot_segment_vector = np.dot(segment_vector, segment_vector)

    # True - there is intersection
    return 0 < dot_segment_vector_and_points_vector < dot_segment_vector


# Calculate t scalar parameter
# t = (C - A) x Vector CD / Vector AB x Vector CD
def calc_t(point_c, point_a, vector_ab, vector_cd):
    t = np.cross(point_c - point_a, vector_cd) / np.cross(vector_ab, vector_cd)
    return t


# Calculate u scalar parameter
# u = (C - A) x Vector AB / Vector AB x Vector CD
def calc_u(point_c, point_a, vector_ab, vector_cd):
    u = np.cross(point_c - point_a, vector_ab) / np.cross(vector_ab, vector_cd)
    return u


# Calculate intersection segment in case of collinear segments
# If intersecting return [begin_of_int_segment, end_of_int_segment] else None
def calc_int_segment(segment_ab, segment_cd, vector_ab, vector_cd):
    point_a = segment_ab.get_first_point()
    point_b = segment_ab.get_second_point()
    point_c = segment_cd.get_first_point()
    point_d = segment_cd.get_second_point()
    all_points = [point_a, point_b, point_c, point_d]

    # Vector AB * Vector AB - * represents DOT PRODUCT
    dot_ab_ab = np.dot(vector_ab, vector_ab)
    # Vector CD * Vector AB - * represents DOT PRODUCT
    dot_cd_ab = np.dot(vector_cd, vector_ab)

    t0 = np.dot(point_c - point_a, vector_ab) / dot_ab_ab
    t1 = t0 + (dot_cd_ab / dot_ab_ab)

    # If vectors point in opposite directions (dot_cd_ab < 0) we are checking [t1, t0] interval
    # in other case we are checking [t0, t1] interval
    # If the interval between t0 and t1 (or t1 and t0) intersects the interval [0, 1]
    # then the line segments are collinear and overlapping; otherwise they are collinear and disjoint.
    if dot_cd_ab < 0 <= t0 and t1 <= 1:
        return get_intersection_segment_from_points(all_points)
    elif t0 <= 1 and 0 <= t1:
        return get_intersection_segment_from_points(all_points)
    else:
        return None


def get_intersection_segment_from_points(all_points):
    dont_check_by_x = all_points[0][0] == all_points[1][0] == all_points[2][0] == all_points[3][0]

    coordinate_to_check = 0 if not dont_check_by_x else 1

    point_min_checked_coordinate = None
    point_max_checked_coordinate = None

    # Get points with MIN_X and MAX_X
    for point in all_points:
        coordinate_value = point[coordinate_to_check]
        if point_min_checked_coordinate is None or coordinate_value < point_min_checked_coordinate[coordinate_to_check]:
            point_min_checked_coordinate = point
        if point_max_checked_coordinate is None or coordinate_value > point_max_checked_coordinate[coordinate_to_check]:
            point_max_checked_coordinate = point

    int_segment_points = []
    # From all points get only points which are not matching MIN_X, MAX_X
    for point in all_points:
        if not (np.array_equal(point, point_min_checked_coordinate) or np.array_equal(point, point_max_checked_coordinate)):
            int_segment_points.append(point)

    # Special Case - Both segments are equal
    if len(int_segment_points) == 0:
        int_segment_points.extend([point_min_checked_coordinate, point_max_checked_coordinate])
    # Special Case - Beginning or Ending of both segments are equal
    elif len(int_segment_points) == 1:
        x = int_segment_points[0][1]
        int_segment_points.append(point_min_checked_coordinate if x > point_min_checked_coordinate[0] else point_max_checked_coordinate)

    return int_segment_points


# Calculate intersection point - return point
# Additional check added, but there should not be situation where int point calculated
# from provided equations will be different - in case of conditions
# (ab_cd_vectors_cross_product != 0 and 0 <= t <= 1 and 0 <= u <= 1) are True
def calc_int_point(point_a, point_c, t, u, vector_ab, vector_cd):
    intersection_point1 = point_a + np.dot(t, vector_ab)
    intersection_point2 = point_c + np.dot(u, vector_cd)

    # There should not be a situation where this two points are not equal
    if np.array_equal(intersection_point1, intersection_point2):
        return intersection_point1
    else:
        return None


def get_vector_from_two_points(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return np.array([x2 - x1, y2 - y1])


# Help method to print data in case of debugging
def print_debug_data(vector_ab, vector_cd, cross_ab_cd, t, u):
    print("Vector AB: " + str(vector_ab))
    print("Vector CD: " + str(vector_cd))
    print("Cross AB x CD: " + str(cross_ab_cd))
    print("t = " + str(t))
    print("u = " + str(u))

