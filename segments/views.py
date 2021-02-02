from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Point, Segment, SegmentsPair
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import is_pair_intersecting
from chartjs.views.lines import BaseLineChartView

FIELD_PAIRS = [['ax', 'ay'], ['bx', 'by'], ['cx', 'cy'], ['dx', 'dy']]


class IndexView(generic.TemplateView):
    template_name = 'segments/index.html'


def set_intersection_data(context, segments_pair):
    intersection_amount, intersection_array = is_pair_intersecting(segments_pair)

    if intersection_amount == 1:
        context['intersection_x'] = intersection_array[0]
        context['intersection_y'] = intersection_array[1]
    elif intersection_amount == 2:
        intersection_first_point = intersection_array[0]
        intersection_second_point = intersection_array[1]
        context['intersection_first_point_x'] = intersection_first_point[0]
        context['intersection_first_point_y'] = intersection_first_point[1]
        context['intersection_second_point_x'] = intersection_second_point[0]
        context['intersection_second_point_y'] = intersection_second_point[1]

    context['intersection_amount'] = intersection_amount


# Provides only data for chart
class ChartResultJSONView(BaseLineChartView):
    template_name = 'segments/result.html'

    def get_context_data(self, **kwargs):
        context = super(BaseLineChartView, self).get_context_data(**kwargs)
        print(context)
        return context

    def get_labels(self):
        # Return labels for x axis
        return []

    def get_providers(self):
        # Return names of datasets.
        return []

    def get_data(self):
        # Return datasets to plot
        return []


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
