from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Point, Segment, SegmentsPair
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import is_pair_intersecting
from chartjs.views.lines import BaseLineChartView
from chartjs.colors import next_color


FIELD_PAIRS = [['ax', 'ay'], ['bx', 'by'], ['cx', 'cy'], ['dx', 'dy']]


class IndexView(generic.TemplateView):
    template_name = 'segments/index.html'


def set_intersection_data(context, segments_pair):
    intersection_amount, intersection_array = is_pair_intersecting(segments_pair)
    context['intersection_amount'] = intersection_amount

    if intersection_amount == 1:
        x = intersection_array[0]
        y = intersection_array[1]
        context['intersection_x'] = x
        context['intersection_y'] = y

        return [{'x': x,
                 'y': y}]

    elif intersection_amount == 2:
        intersection_first_point = intersection_array[0]
        intersection_second_point = intersection_array[1]
        x1 = intersection_first_point[0]
        y1 = intersection_first_point[1]
        x2 = intersection_second_point[0]
        y2 = intersection_second_point[1]
        context['intersection_first_point_x'] = x1
        context['intersection_first_point_y'] = y1
        context['intersection_second_point_x'] = x2
        context['intersection_second_point_y'] = y2

        return [{'x': x1,
                 'y': y1},
                {'x': x2,
                 'y': y2}]


# Provides only data for chart
class ChartResultJSONView(BaseLineChartView):
    template_name = 'segments/result.html'

    def get_colors(self):
        # Colors for provided data
        colors = [
            (0, 204, 0),  # Green
            (255, 153, 153),  # Light red
            (255, 204, 153),  # Light orange
        ]
        return next_color(colors)

    def get_context_data(self, **kwargs):
        segments_pair_id = self.kwargs['pk']
        segments_pair = get_object_or_404(SegmentsPair, pk=segments_pair_id)

        first_segment = segments_pair.get_first_segment()
        second_segment = segments_pair.get_second_segment()

        # Used to pass segments to get_data()
        self.kwargs['first_segment'] = first_segment
        self.kwargs['second_segment'] = second_segment
        self.get_intersection_json(segments_pair)

        # Call the base implementation to get a context
        return super().get_context_data(**kwargs)

    def get_intersection_json(self, segments_pair):
        intersection_amount, intersection_array = is_pair_intersecting(segments_pair)

        if intersection_amount == 1:
            x = intersection_array[0]
            y = intersection_array[1]

            intersection_array = [{'x': x,
                                   'y': y}]

        elif intersection_amount == 2:
            intersection_first_point = intersection_array[0]
            intersection_second_point = intersection_array[1]
            x1 = intersection_first_point[0]
            y1 = intersection_first_point[1]
            x2 = intersection_second_point[0]
            y2 = intersection_second_point[1]

            intersection_array = [{'x': x1,
                                   'y': y1},
                                  {'x': x2,
                                   'y': y2}]

        self.kwargs['intersection_array'] = intersection_array

    def get_labels(self):
        # Return labels for x axis
        return []

    def get_providers(self):
        # Return names of datasets.
        return ["Miejsce przecięcia", "Pierwszy odcinek", "Drugi odcinek"]

    def get_data(self):
        # Return datasets to plot
        first_segment = self.kwargs['first_segment']
        second_segment = self.kwargs['second_segment']
        intersection_array = self.kwargs['intersection_array']
        arr1 = first_segment.get_as_json_array()
        arr2 = second_segment.get_as_json_array()
        return [intersection_array, arr1, arr2]

    def get_dataset_options(self, index, color):
        # Additional options for dataset
        my_opt = {
            "showLine": "true",
            "fill": "false"
        }

        default_opt = super(ChartResultJSONView, self).get_dataset_options(index, color)
        default_opt.update(my_opt)

        return default_opt


# Provides data for result page
class ChartResultView(TemplateView):
    template_name = "segments/result.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        segments_pair_id = context['pk']

        segments_pair = get_object_or_404(SegmentsPair, pk=segments_pair_id)

        first_segment = segments_pair.get_first_segment()
        second_segment = segments_pair.get_second_segment()

        # Set context data about intersection
        set_intersection_data(context, segments_pair)

        context['first_segment'] = first_segment
        context['second_segment'] = second_segment

        return context


def check_intersection(request):
    # Check if all fields are filled
    if not validate_fields(request):
        return render(request, 'segments/index.html', {
            'error_message': "Proszę wypełnić wszystkie pola.",
        })

    points_arr = []
    for field_pair in FIELD_PAIRS:
        point_from_request = get_point_from_request(field_pair, request)
        points_arr.append(point_from_request)

    segments_arr = []
    # increment range by 2
    for i in range(0, len(points_arr), 2):
        point1 = points_arr[i]
        point2 = points_arr[i + 1]

        segment = Segment.objects.create(point1=point1, point2=point2)
        segments_arr.append(segment)

    segment1 = segments_arr[0]
    segment2 = segments_arr[1]
    segments_pair = SegmentsPair.objects.create(segment1=segment1, segment2=segment2)

    print(segments_pair)

    return HttpResponseRedirect(reverse('segments:result', args=(segments_pair.id,)))


def validate_fields(request):
    for field_pair in FIELD_PAIRS:
        x = request.POST[field_pair[0]]
        y = request.POST[field_pair[1]]

        if x == "" or y == "":
            return False

    return True


def get_point_from_request(field_pair, request):
    x = float(request.POST[field_pair[0]])
    y = float(request.POST[field_pair[1]])

    return Point.objects.create(x_coordinate=x, y_coordinate=y)
