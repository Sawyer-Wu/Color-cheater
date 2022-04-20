import pyautogui
import cv2
import numpy as np
import time


def rgbdis(p1, p2):
    dis = sum((p1 - p2) ** 2)
    return dis


def metrix_create(step, parameter):
    sx = parameter[0]
    sy = parameter[1]
    l = parameter[2]
    start_point = [sx, sy]
    x = []
    y = []
    c_x = []
    c_y = []
    for i in range(step+1):
        if i == 0:
            x.append(start_point[0])
            y.append(start_point[1])
        else:
            sx += l / step
            sy += l / step
            x.append(sx)
            y.append(sy)
            c_x.append(int(np.floor(x[i-1] + (x[i] - x[i-1]) / 2)))
            c_y.append(int(np.floor(y[i-1] + (y[i] - y[i-1]) / 2)))
    return c_x, c_y


def click_operation(cord):
    x = cord[0]
    y = cord[1]
    time.sleep(0)
    pyautogui.moveTo(x, y)
    pyautogui.click()


def find_diff(v):
    diff_m = []
    diff_sum = []
    for i in v:
        diff_sum.append(sum(i[0]))
    average = sum(diff_sum)/len(diff_sum)
    for i in v:
        diff_m.append((sum(i[0])-average)**2)
    if max(np.array(diff_m)) < 1:
        cor = 0
    else:
        diff_index = np.argmax(np.array(diff_m))
        cor = [v[diff_index][1], v[diff_index][2]]
    return cor


if __name__ == '__main__':
    parameter = [358, 471, 625, 625]
    step_l = [2, 3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8]
    num = 0
    cx_l = [[514, 826], [462, 670, 878], [436, 592, 748, 904],  [420, 545, 670, 795, 920],  [410, 514, 618, 722, 826, 930],  [402, 491, 581, 670, 759, 849, 938],  [397, 475, 553, 631, 709, 787, 865, 943],  [392, 462, 531, 601, 670, 739, 809, 878, 948]]
    cy_l = [[627, 939], [575, 783, 991], [549, 705, 861, 1017], [533, 658, 783, 908, 1033], [523, 627, 731, 835, 939, 1043], [515, 604, 694, 783, 872, 962, 1051], [510, 588, 666, 744, 822, 900, 978, 1056], [505, 575, 644, 714, 783, 852, 922, 991, 1061]]
    while True:
        if num > 15:
            step = 9
        else:
            step = step_l[num]
        image = pyautogui.screenshot(region=[358, 471, 625, 625])
        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        c_x, c_y = metrix_create(step, parameter)
        # c_x = cx_l[step - 2]
        # c_y = cy_l[step - 2]
        value = []
        for cx in range(len(c_x)):
            for cy in range(len(c_y)):
                if len(c_x) > 2:
                    if cy != 0:
                        dis = rgbdis(img[c_y[cy] - parameter[1]][c_x[cx] - parameter[0]], img[c_y[cy-1] - parameter[1]][c_x[cx] - parameter[0]])

                        if cy > 2:
                            if dis > 0:
                                cord = [c_x[cx], c_y[cy]]
                                break
                            else:
                                continue
                        elif cy == 1:
                            temp_dis = dis
                        else:
                            if dis == temp_dis:
                                if dis == 0:
                                    continue
                                else:
                                    cord = [c_x[cx], c_y[1]]
                                    break
                            else:
                                if dis > 0:
                                    cord = [c_x[cx], c_y[2]]
                                    break
                                else:
                                    cord = [c_x[cx], c_y[0]]
                                    break

                    else:
                        continue
                else:
                    if cy != 0:
                        dis = rgbdis(img[c_y[cy] - parameter[1]][c_x[cx] - parameter[0]], img[c_y[cy-1] - parameter[1]][c_x[cx] - parameter[0]])
                        if dis > 0:
                            if cx == 0:
                                Dis = rgbdis(img[c_y[cy] - parameter[1]][c_x[cx + 1] - parameter[0]],
                                             img[c_y[cy - 1] - parameter[1]][c_x[cx] - parameter[0]])
                                if Dis > 0:
                                    cord = [c_x[cx], c_y[cy-1]]
                                    break
                                else:
                                    cord = [c_x[cx], c_y[cy]]
                                    break
                            else:
                                Dis = rgbdis(img[c_y[cy] - parameter[1]][c_x[cx -1] - parameter[0]],
                                             img[c_y[cy - 1] - parameter[1]][c_x[cx] - parameter[0]])
                                if Dis > 0:
                                    cord = [c_x[cx], c_y[cy-1]]
                                    break
                                else:
                                    cord = [c_x[cx], c_y[cy]]
                                    break
                        else:
                            continue
                    else:
                        continue


        # cord = find_diff(value)
        if num == 260:
            break
        else:
            click_operation(cord)
        num += 1
