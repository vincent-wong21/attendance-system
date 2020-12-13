import face_recognition
from face_recognition.face_detection_cli import image_files_in_folder
import face_recognition_knn
import cv2
import os
import attendance_window
import bounding_boxes


def recognize():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        _, img = cap.read()
        
        img = bounding_boxes.draw_overlay(img)
        cv2.imshow("Face Detection", img)

        # Scaling image down by 1/4 resolution for faster face recognition
        small_img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
        rgb_small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

        face_bounding_boxes = face_recognition.face_locations(rgb_small_img)

        if len(face_bounding_boxes) == 1:
            print("Face Detected")
            # original_rgb_img = cv2.resize(rgb_small_img, (0,0), fx=4, fy=4)
            
            predictions = face_recognition_knn.predict(rgb_small_img, model_path="knn_model.clf")
            for name, (top, right, bottom, left) in predictions:
                print("- Found {} at ({}, {})".format(name, left, top))
            
            # if predictions:
            name = predictions[0][0]
            present = attendance_window.check_attendance(name)

            if name != "unknown" and not present:
                name_path = os.path.join("data/train", name)
                img_path = image_files_in_folder(name_path)[0]
                attendance_window.show_attendance_window(img_path, int(name))

            # cap.release()
            # cv2.destroyAllWindows()
            # return predictions[0][0]

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":

    print("(1) Train Model")
    print("(2) Face Recognition")
    user_input = int(input("Choose >> "))
    # user_input = 2

    if user_input == 1:
        train_path = "data/train"
        print(" -- (!) Training..")
        classifier = face_recognition_knn.train(train_path, model_save_path="knn_model.clf", n_neighbors=1, verbose=True)
        print(" -- (!) Training completed..")
    else:
        name = recognize()
        # print(name)
        # name_path = os.path.join("data/train", name)
        # img_path = image_files_in_folder(name_path)[0]

        # attendance_window.show_attendance_window(img_path)
        # img = cv2.imread(img_path)
        # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Result", img)
        # cv2.waitKey(0)

