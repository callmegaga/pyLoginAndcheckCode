from PIL import Image
import pytesseract
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

def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img
def getCheckCode(img):
    gif = Image.open(img).convert("L")
    gif = binarizing(gif,130)
    # gif = depoint(gif)
    code = pytesseract.image_to_string(gif, config="-psm 7 digits").replace(' ', '')
    return code
if __name__ == '__main__':
    gif = Image.open(sys.argv[1]).convert("L")
    gif = binarizing(gif,130)
    # gif = depoint(gif)
    code = pytesseract.image_to_string(gif, config="-psm 7 digits")
    print code
