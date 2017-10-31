from PIL import Image
import sys
def binarizing(img,threshold): #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):         
            if y==0 or x==0 or y==17 or x==59:
                pixdata[x, y] = 255
                continue                       
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img
if __name__ == '__main__':
    gif = Image.open(sys.argv[1]).convert("L")
    gif = binarizing(gif,130)
    gif.save(sys.argv[1]+".tif")
