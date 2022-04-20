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
    while True:
        if num > 15:
            step = 9
        else:
            step = step_l[num]
        image = pyautogui.screenshot(region=[358, 471, 625, 625])
        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        c_x, c_y = metrix_create(step, parameter)
        value = []
        for cx in c_x:
            for cy in c_y:
                value.append([img[cy-parameter[1]][cx-parameter[0]], cx, cy])

        cord = find_diff(value)
        if cord == 0:
            break
        else:
            click_operation(cord)
        num += 1
