import os
import Image
import shutil
import Tkinter

def ins(a):
    s = ""
    if a < 1000:
        s += "0"
    if a < 100:
        s += "0"
    if a < 10:
        s += "0"
    return s + str(a)

def mkdir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print(e)

pdf_file_folder = "pdf_file_temp"
cut_file_folder = "cut_file_temp"
separate_folder = 0
done_file_folder = "done"
mkdir(pdf_file_folder)
mkdir(cut_file_folder)
mkdir(done_file_folder)

file_list = os.listdir(".")

for file_name in file_list:
    if file_name.endswith(".pdf"):
        print "Cutting file %s ..." % file_name
        print "Converting pdf to jpeg..."
        os.system("pdftoppm -jpeg \"%s\" %s/temp" % (file_name, pdf_file_folder))
        jpg_list = os.listdir("%s" % pdf_file_folder)
        jpg_list.sort()
        count = 0
        print "Cutting jpeg files..."
        for jpg_file_name in jpg_list:
            if count % 50 == 0:
                os.mkdir("%s/%d" % (cut_file_folder, count / 50))
                separate_folder = count / 50
            im = Image.open("%s/%s" % (pdf_file_folder, jpg_file_name))
            x, y = im.size
            boxa = (0, 0, x / 2, y)
            boxb = (x / 2, 0, x, y)
            im.crop(boxa).save("%s/%d/cut-%s.jpg" % (cut_file_folder, separate_folder, ins(count * 2)))
            im.crop(boxb).save("%s/%d/cut-%s.jpg" % (cut_file_folder, separate_folder, ins(count * 2 + 1)))
            count = count + 1
        print "Merging jpeg files to pdf..."
        for folder_id in range(0, separate_folder + 1):
            os.system("convert %s/%d/*.jpg %s/\"%s_%d.pdf\"" % (cut_file_folder, folder_id, done_file_folder, file_name[0:-4], folder_id))
        os.system("rm %s/* -rf" % (pdf_file_folder))
        os.system("rm %s/* -rf" % (cut_file_folder))
        print "File %s is converted." % file_name.strip()

shutil.rmtree(pdf_file_folder, ignore_errors=True)
shutil.rmtree(cut_file_folder, ignore_errors=True)
