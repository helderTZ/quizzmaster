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
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 50, 220, cv2.THRESH_BINARY)
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
        question_idx = text.find("Q:")
        answer_idx = text.find("A:")
        question = text[question_idx:answer_idx]
        answer = text[answer_idx::]

        print("--------- text ---------")
        print(text)
        print("------------------------")
        print("------- question -------")
        print(question)
        print("------------------------")
        print("-------- answer --------")
        print(answer)
        print("------------------------")
        os.system("echo \"" + text + "\" | festival --tts")

    elif k % 256 == 27: # escape
        break

cam.release()
cv2.destroyAllWindows()