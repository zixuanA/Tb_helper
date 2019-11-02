import os
import xml.etree.ElementTree as elementTree
import time

user_name = 'zixuan'
file_path = ''


def get_ui_xml():
    file = os.popen("adb shell uiautomator dump --compressed /data/local/tmp/uidump.xml")
    file.close()
    print(os.popen("adb pull /data/local/tmp/uidump.xml " + file_path).read())


def analysis_xml(number_of_layer):
    file = open(file_path + 'uidump.xml')
    root = elementTree.parse(file).getroot()
    file.close()
    for i in range(number_of_layer):
        root = root.find('node')
    return root


def tap(x, y):
    line = os.popen("adb shell input tap " + str(x) + " " + str(y))
    line.close()


def get_point(position_string):
    point_x = 0
    point_y = 0
    check = True
    for i in position_string:
        if i == ']':
            break
        elif i == ',':
            check = False
        if i == '[' or i == ',':
            continue
        if check:
            point_x = point_x * 10 + int(i)
        else:
            point_y = point_y * 10 + int(i)
    return [point_x, point_y]


get_ui_xml()
fla = analysis_xml(11).findall('node')[2][1][0][5].attrib['bounds']
# check = True
point_x = get_point(fla)[0]
point_y = get_point(fla)[1]
tap(point_x + 10, point_y + 10)
print(point_x, point_y)
flag = True
while flag:
    time.sleep(1)
    get_ui_xml()
    int_flag = 0
    for i in analysis_xml(11)[5][1][1][0][13]:

        int_flag += 1
        print("raw:"+i[2].attrib['text'] + str(len(analysis_xml(11)[5][1][1][0][13])) + "   " + str(int_flag))
        if i[2].attrib['text'][1] == '浏' or i[2].attrib['text'][1] == '进':

            if i[2].attrib['text'][0] != '已' and '首页' not in i[1][0].attrib['text']:
                time.sleep(2)
                print("tap:"+i[2].attrib['text'])
                tap(get_point(i[2].attrib['bounds'])[0] + 100, get_point(i[2].attrib['bounds'])[1] + 40)
                if '进店'in i[1][1].attrib['text']:
                    time.sleep(5)
                    os.popen('adb shell input swipe 300 600 300 100')
                    time.sleep(5)
                    os.popen('adb shell input swipe 300 600 300 100')
                    time.sleep(12)
                    os.popen('adb shell input swipe 300 600 300 100')
                    time.sleep(5)
                else:
                    time.sleep(11)
                    os.popen('adb shell input swipe 300 600 300 100')
                    time.sleep(10)
                os.popen('adb shell input keyevent 4')
                if analysis_xml(11)[5][1][1][0][13] != int_flag and i[2].attrib['text'][0] == '已':
                    break

        # print(str(len(analysis_xml(11)[5][1][1][0][13] - 1))+" "+str(int_flag))
        print(i[2].attrib['text']  +str(len(analysis_xml(11)[5][1][1][0][13]))+"   "+str(int_flag))
        if len(analysis_xml(11)[5][1][1][0][13]) == int_flag and i[2].attrib['text'][0] == '已':
            flag = False
            print('执行结束')
