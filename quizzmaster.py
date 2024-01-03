# Adapted from: https://github.com/maazismail/ocr-camera/blob/main/main.py

import cv2
import pytesseract
import os

cam = cv2.VideoCapture(0)
cv2.namedWindow("Quizzmaster")

while True:
    ret, frame = cam.read()

    # flip = cv2.flip(frame, 1)
    # cv2.imshow("Quizzmaster", flip)
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 180, cv2.THRESH_BINARY)
    cv2.imshow("Quizzmaster", blackAndWhiteImage)

    k = cv2.waitKey(1)
    if k % 256 == 32:   # space
        cv2.imwrite("capture.png", blackAndWhiteImage)
        img = cv2.imread('capture.png')
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)

        # filter out weird characters for festival
        text = text.replace("\"", "")
        text = text.replace("\n", " ")

        question_idx_1  = text.find("Q:")
        answer_idx_1    = text.find("A:")
        question_idx_2  = text.find("Q:", answer_idx_1)
        answer_idx_2    = text.find("A:", question_idx_2)
        question1   = text[question_idx_1:answer_idx_1]
        answer1     = text[answer_idx_1:question_idx_2]
        question2   = text[question_idx_2:answer_idx_2]
        answer2     = text[answer_idx_2::]

        # print("--------- text ---------")
        # print(text)
        # print("------------------------")
        # print("------- question -------")
        # print(question)
        # print("------------------------")
        # print("-------- answer --------")
        # print(answer)
        # print("------------------------")
        print(question1)
        os.system("echo \"" + question1 + "\" | festival --tts")
        print(question2)
        os.system("echo \"" + question2 + "\" | festival --tts")

    elif k % 256 == 27: # escape
        break

cam.release()
cv2.destroyAllWindows()