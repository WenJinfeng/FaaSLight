import time
init_st = time.time() * 1000
from skimage import io
import urllib
import skimage.segmentation as segmentation
init_ed = time.time() * 1000

def handler(request):

    fun_st = time.time() * 1000
    urllib.request.urlretrieve('https://upload.wikimedia.org/wikipedia/commons/3/38/JPEG_example_JPG_RIP_001.jpg', '/tmp/hi.jpg')
    img = io.imread('/tmp/hi.jpg')
    print(img)

    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)




# handler("","")