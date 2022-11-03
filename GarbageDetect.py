import argparse
from system_log_handler import Logger

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np

# -------- ARGUMENTS
ap = argparse.ArgumentParser()
ap.add_argument("-date", "--date", required=False, help="The date of the schedule(document name).")
ap.add_argument("-region", "--region", required=False, help="Region your detecting.")
ap.add_argument("-province", "--province", required=False, help="Province your detecting.")
ap.add_argument("-city", "--city", required=False, help="City your detecting.")
ap.add_argument("-barangay", "--barangay", required=False, help="Barangay your detecting.")
ap.add_argument("-Section", "--Section", required=False, help="Section your detecting.")
args = vars(ap.parse_args())

# ----------- INITIALIZE ------------
log_handler = Logger()
log_handler.appendLog("[SCHEDULER] Executing Automatic Scheduler \n")

# Firebase Firestore
log_handler.appendLog("[DETECTION SCRIPT] Starting Firebase \n")
cred = credentials.Certificate('garbeye_service_account.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client().collection(u'collection_schedule')


# ------------ FUNCTIONS --------------
# Sets the input tensor.
def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.expand_dims((image - 255) / 255, axis=0)


# Returns the output tensor at the given index.
def get_output_tensor(interpreter, index):
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    return tensor


# Returns a list of detection results, each a dictionary of object info.
def detect_objects(interpreter, image, threshold):
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    # Get all output details
    boxes = get_output_tensor(interpreter, 0)
    classes = get_output_tensor(interpreter, 1)
    scores = get_output_tensor(interpreter, 2)
    count = int(get_output_tensor(interpreter, 3))

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results


# Get Schedule
sched_document = db.document(args['date']).get()
if sched_document.exists:
    log_handler.appendLog("[DETECTION SCRIPT] Schedule Acquired. \n")
    schedule = sched_document.to_dict()

    print(schedule)

else:
    log_handler.appendLog("[DETECTION SCRIPT] Failed to get the Schedule. \n")
