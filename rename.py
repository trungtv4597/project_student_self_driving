import os
import cv2


def rename(data_path):
    '''
        Rename all files in directory
    '''
    i = 0
    data_dir = os.listdir(data_path)
    for filename in data_dir:
        src = filename
        dst = 'cc'+str(i)+'.jpg'
        i += 1
        os.rename(src, dst)
    return print('Accomplish re-name')


def reformat(data_path):
    '''
        Scraping images from Google Image Search sometimes have wrong filenam extension.
    '''
    data_dir = os.listdir(data_path)
    for filename in data_dir:
        print(filename)
        image = cv2.imread(filename)
        #cv2.imshow('xxx', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #break
        cv2.imwrite(filename, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return print('Accomplish re-format')


if __name__ == "__main__":
    data_path = r'C:\Users\DucTRung\Documents\data_set\stop_sign_detection\images\stop'
    os.chdir(data_path)
    #rename(data_path)
    reformat(data_path)
