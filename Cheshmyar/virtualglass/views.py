import cv2
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import os
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie

import pages.views
from Cheshmyar.settings import STATIC_ROOT, STATICFILES_DIRS
from virtualglass.camera import VideoCamera
from virtualglass.filter import ColorFilter


def remove_extension_file(filename):
    return filename.replace(".jpg", "").replace(".JPG", "")


def slice_to_4_member_arrays(array):
    result = []
    x = len(array) // 4
    for i in range(0, x + 1):
        result.append(array[(4 * i): (4 * i + 4)])
    return result

# virtualglass : glasses pictures for virtual
# colorglass : glasses pictures for color filter
# colordefault : default pictures for color filter
# glassesfilters : filters with the same names of glasses


def index(request):
    sunglasses_list = os.listdir(os.path.join(STATICFILES_DIRS[0], "Services\\virtualglass"))
    sunglasses_list = [remove_extension_file(i) for i in sunglasses_list]
    color_glasses_list = os.listdir(os.path.join(STATICFILES_DIRS[0], "Services\\colorglass"))
    color_glasses_list = [remove_extension_file(i) for i in color_glasses_list]
    return render(request, 'services/virtual-glass2.html', {
        'is_logged_in': pages.views.is_logged_in,
        'sunglasses_list': slice_to_4_member_arrays(sunglasses_list),
        'color_glasses_list': slice_to_4_member_arrays(color_glasses_list)
    })


def video(request, glasses):
    return render(request, 'services/virtualglass/virtual-try-on.html', {'glasses': glasses})


def gen(camera, glasses):
    while True:
        frame = camera.get_frame(glasses=glasses)
        yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_stream(request, glasses):
    return StreamingHttpResponse(gen(VideoCamera(), glasses), content_type='multipart/x-mixed-replace; boundary=frame')


def return_context(glasses):
    default_list = os.listdir(os.path.join(STATICFILES_DIRS[0], "Services\\colordefault"))
    default_list = [remove_extension_file(i) for i in default_list]
    context = {
        'is_logged_in': pages.views.is_logged_in,
        'default_list': slice_to_4_member_arrays(default_list),
        'glasses': glasses
    }
    return context


@ensure_csrf_cookie
def upload_files(request, glasses):
    context = return_context(glasses)
    if request.method == "GET":
        return render(request, 'services/virtualglass/color-filter.html', context)
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        filename = "media/colorfilter/input/" + file.name
        handle_uploaded_file(file, filename)
        source = '<img src="../../../../' + filter_process(filename, glasses, True) + '" width=200 height=200>'
        return JsonResponse({'img': source})
    else:
        return render(request, 'services/virtualglass/color-filter.html', context)


@ensure_csrf_cookie
def choose_pic(request, glasses):
    context = return_context(glasses)
    if request.method == "GET":
        return render(request, 'services/virtualglass/color-filter.html', context)
    if request.method == 'POST':
        image = request.POST['im_source']

        source = '<img src="../../../../' + filter_process(image[8:], glasses, False) + '" width=200 height=200>'
        return JsonResponse({'img': source})
    else:
        return render(request, 'services/virtualglass/color-filter.html', context)


def handle_uploaded_file(f, src):
    with open(src, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def convert_static_to_media(string):
    return string.replace("Services/colordefault", "media/colorfilter/output")


def remove_static(string):
    return string.replace("/static", "")


def filter_process(filename, glasses, is_default):
    print(f"glasses : {glasses} , filename : {filename}")
    color_filter = ColorFilter(glasses, filename)
    color_filter.fetch_images()
    result = color_filter.img_blendd
    output = filename
    if not is_default:
        output = convert_static_to_media(filename)
    cv2.imwrite(output, result)
    return output
