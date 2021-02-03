from django.db import models
import numpy as np


class Point(models.Model):
    x_coordinate = models.FloatField(null=False)
    y_coordinate = models.FloatField(null=False)

    def get_as_array(self):
        return np.array([self.x_coordinate, self.y_coordinate])


class Segment(models.Model):
    point1 = models.ForeignKey(Point, related_name='point_1', on_delete=models.CASCADE)
    point2 = models.ForeignKey(Point, related_name='point_2', on_delete=models.CASCADE)

    def get_as_vector(self):
        first_point = self.point1.get_as_array()
        second_point = self.point2.get_as_array()
        x1 = first_point[0]
        y1 = first_point[1]
        x2 = second_point[0]
        y2 = second_point[1]
        return np.array([x2 - x1, y2 - y1])

    def get_as_json_array(self):
        first_point = self.point1.get_as_array()
        second_point = self.point2.get_as_array()
        x1 = first_point[0]
        y1 = first_point[1]
        x2 = second_point[0]
        y2 = second_point[1]
        return [{
                    'x': x1,
                    'y': y1
                },
                {
                    'x': x2,
                    'y': y2
                }]

    def get_first_point(self):
        return self.point1.get_as_array()

    def get_second_point(self):
        return self.point2.get_as_array()

    def are_both_points_equal(self):
        return np.array_equal(self.point1.get_as_array(), self.point2.get_as_array())

    def __str__(self):
        return "Punkt 1: " + str(self.get_first_point()) + " Punkt 2: " + str(self.get_second_point())


class SegmentsPair(models.Model):
    segment1 = models.ForeignKey(Segment, related_name='segment_1', on_delete=models.CASCADE)
    segment2 = models.ForeignKey(Segment, related_name='segment_2', on_delete=models.CASCADE)
    intersection_amount = None
    intersection_array = None

    def get_first_segment(self):
        return self.segment1

    def get_second_segment(self):
        return self.segment2

    def __str__(self):
        return "Odcinek 1:\n" + str(self.segment1) + "\nOdcinek 2:\n" + str(self.segment2)
