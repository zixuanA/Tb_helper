import os
import xml.etree.ElementTree as elementTree
import time
user_name = 'zixuan'
def get_ui_xml():
    file = os.popen("adb shell uiautomator dump --compressed /data/local/tmp/uidump.xml")
    file.close()
    print(os.popen("adb pull /data/local/tmp/uidump.xml ~/Desktop").read())


def analysis_xml(number_of_layer):
    file = open('/Users/'+user_name+'/Desktop/uidump.xml')
    root = elementTree.parse(file).getroot()
    file.close()
    for i in range(number_of_layer):
        root = root.find('node')
    return root

def tap(x,y):
    line = os.popen("adb shell input tap "+str(x)+" "+str(y))
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
    return [point_x,point_y]

get_ui_xml()
fla = analysis_xml(11).findall('node')[2][1][0][5].attrib['bounds']
point_x = 0
point_y = 0
check = True
for i in fla:
    if i == ']':
        break
    elif i == ',':
        check = False
    if i == '[' or i == ',':
        continue
    if check:
        point_x=point_x*10+int(i)
    else:
        point_y=point_y*10+int(i)
tap(point_x+10,point_y+10)
print(point_x,point_y)
flag = True
while flag:
    get_ui_xml()
    int_flag = 0
    for i in analysis_xml(11)[5][1][1][0][13]:


        int_flag += 1
        if i[2].attrib['text'][1] == '浏' or i[2].attrib['text'][1] == '进':

            if i[2].attrib['text'] != '已完成':

                # print(get_point(i[2].attrib['bounds'])[0],get_point(i[2].attrib['bounds'])[1])
                tap(get_point(i[2].attrib['bounds'])[0] + 100,get_point(i[2].attrib['bounds'])[1] + 40)
                if i[2].attrib['text'][1] == '进':
                    time.sleep(10)
                    os.popen('adb shell input swipe 300 300 300 100')
                    time.sleep(20)
                else:
                    time.sleep(20)
                os.popen('adb shell input keyevent 4')
                break

        print(str(len(analysis_xml(11)[5][1][1][0][13] - 1))+" "+str(int_flag))
        if len(analysis_xml(11)[5][1][1][0][13]) - 1 == int_flag:
            flag = False
            print('执行结束')