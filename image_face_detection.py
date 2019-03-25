import cv2
import os
import dlib
import face_recognition
from multiprocessing import Process, Manager
import datetime
import time
import sys
import argparse

def recognize_face(cropped_image, face_location, return_dict, images):
    height, width = cropped_image.shape[:2]
    start = time.time()
    face_matched = False
    image_to_be_matched_encoded = face_recognition.face_encodings(cropped_image, known_face_locations=[face_location])[0]
    for image in images:
        current_image = face_recognition.load_image_file("images/" + image)
        if(face_recognition.face_encodings(current_image)):
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
            result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
            # check if it was a match
            if result[0] == True:
#                print ("Matched: " + image)
                face_matched = True
                if(return_dict.get(image) != None):
                    return_dict[image] += 1
                else:
                    return_dict[image] = 1
            stop = time.time()
    
#    print("Time taken:", stop-start)
    if(not face_matched):
        print("Face not matched")
        if(return_dict.get("unknown") != None):
            return_dict["unknown"] += 1
        else:
            return_dict["unknown"] = 1
        x, y, w, h = face_location
        x1, w1, h1, y1 = 30, 30, 30, 30
        if(x-2*x1 < 0):
            x1 = x/2
        if(w+w1 > height):
            w1 = height - w
        if(h-h1 < 0):
            h1 = h
        if(y+y1 > width):
            y1 = width - y
        cv2.imwrite("images/unknown-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg", cropped_image[int(x-2*x1):int(w+w1), int(h-h1):int(y+y1)])
        return False
    else: return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--image', type=str,
        help='path to image file'
    )
    parser.add_argument(
        '--repo', type=str,
        help='path to saved images directory'
    )
    image_path = parser.parse_args().image
    repository = parser.parse_args().repo
    procs = []
    return_dict=Manager().dict()
    images = os.listdir(repository)
    image_to_be_matched = face_recognition.load_image_file(image_path)    
    #gray = cv2.cvtColor(image_to_be_matched, cv2.COLOR_BGR2GRAY)
    face_locations = face_recognition.face_locations(image_to_be_matched)
    for (x, y, w, h) in face_locations:
#       print("Recognizing...")
        proc = Process(target = recognize_face, args = (image_to_be_matched,(x,y,w,h),return_dict,images,))
        proc.start()
        procs.append(proc)
        frame_count = 0
        cv2.rectangle(image_to_be_matched, (y, x), (h, w), (0, 255, 0), 2)
        frame_count += 1
    
#    print("Joining")
    for proc in procs:
        proc.join()
        print(return_dict)