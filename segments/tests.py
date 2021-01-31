from django.test import TestCase
from .service import *
from .models import Segment, Point


def create_point(x, y):
    return Point.objects.create(x_coordinate=x, y_coordinate=y)


def create_segment(p1, p2):
    return Segment.objects.create(point1=p1, point2=p2)


def create_segment_from_coordinates(x1, y1, x2, y2):
    p1 = create_point(x1, y1)
    p2 = create_point(x2, y2)
    return create_segment(p1, p2)


class IntersectionTests(TestCase):
    def test_intersection_point_1(self):
        segment1 = create_segment_from_coordinates(-2, 0, 0, 2)
        segment2 = create_segment_from_coordinates(-2, 2, 0, 0)
        int_points_amount, int_array = are_intersecting(segment1, segment2)
        x = int_array[0]
        y = int_array[1]
        print(int_array)
        self.assertEqual(int_points_amount, 1)
        self.assertEqual(x, -1)
        self.assertEqual(y, 1)

    def test_intersection_point_2(self):
        segment1 = create_segment_from_coordinates(-4, 0, 0, 4)
        segment2 = create_segment_from_coordinates(-3, 1, -2, 1)
        int_points_amount, int_array = are_intersecting(segment1, segment2)
        x = int_array[0]
        y = int_array[1]
        self.assertEqual(int_points_amount, 1)
        self.assertEqual(x, -3)
        self.assertEqual(y, 1)

    def test_intersection_point_segment_to_point_case(self):
        segment1 = create_segment_from_coordinates(-4, 0, 0, 4)
        segment2 = create_segment_from_coordinates(-3, 1, -3, 1)
        int_points_amount, int_array = are_intersecting(segment1, segment2)
        x = int_array[0]
        y = int_array[1]
        self.assertEqual(int_points_amount, 1)
        self.assertEqual(x, -3)
        self.assertEqual(y, 1)

    def test_no_intersection_point_segment_to_point_case(self):
        segment1 = create_segment_from_coordinates(-4, 0, 0, 4)
        segment2 = create_segment_from_coordinates(-5, 1, -5, 1)
        int_points_amount, int_array = are_intersecting(segment1, segment2)
        self.assertEqual(int_points_amount, 0)

    def test_no_intersection_boolean_point_segment_to_point_case(self):
        segment1 = create_segment_from_coordinates(-4, 0, 0, 4)
        segment2 = create_segment_from_coordinates(-5, 1, -5, 1)
        result = are_intersecting_boolean(segment1, segment2)
        self.assertEqual(result, False)

    def test_intersection_segment_same_segments(self):
        segment1 = create_segment_from_coordinates(-4, 0, 0, 4)
        segment2 = create_segment_from_coordinates(-4, 0, 0, 4)
        int_points_amount, int_array = are_intersecting(segment1, segment2)
        print(int_array[0])
        print(int_array[1])
        self.assertEqual(int_points_amount, 2)

