from django.shortcuts import render
from .models import Point, Segment, SegmentsPair
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import is_pair_intersecting

FIELD_PAIRS = [['ax', 'ay'], ['bx', 'by'], ['cx', 'cy'], ['dx', 'dy']]


class IndexView(generic.TemplateView):
    template_name = 'segments/index.html'


class ResultView(generic.DetailView):
    model = SegmentsPair
    context_object_name = 'segments_pair'
    template_name = 'segments/result.html'

    def get_context_data(self, **kwargs):
        segments_pair = self.get_object()

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        first_segment = segments_pair.get_first_segment()
        second_segment = segments_pair.get_second_segment()

        intersection_amount, intersection_array = is_pair_intersecting(segments_pair)

        print(intersection_amount)
        print(intersection_array)

        context['first_segment'] = first_segment
        context['second_segment'] = second_segment
        context['intersection_amount'] = intersection_amount

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
        point2 = points_arr[i+1]

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
