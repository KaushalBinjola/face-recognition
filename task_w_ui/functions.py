import os

# import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import face_recognition
import pandas as pd


# import face_recognition


def all_paths(directory):
    files_to_go = []
    for file in os.walk(directory):
        if file[-1] != []:
            for i in file[-1]:
                file_dir = file[0] + "\\" + i
                files_to_go.append(file_dir)
    people = logic(files_to_go)
    return people


def face(path):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    max_rect = []
    max_ar = 0
    for x, y, w, h in faces:
        if w * h > max_ar:
            max_ar = w * h
            max_rect = [x, y, w, h]
    x, y, w, h = max_rect
    new_img = Image.open(path).crop((x, y, x + w, y + h))
    return new_img


def logic(files_to_go):
    people = {}
    for i in files_to_go:
        img = face(i).resize((100, 100))
        name = i[i.rindex("\\") + 1 : i.rindex(".")]
        img_type = i[i.rindex("\\") - 6 : i.rindex("\\")]
        enc = face_recognition.face_encodings(np.asarray(img))[0]
        if name not in people:
            people[name] = {
                "location_adhaar": i if img_type == "adhaar" else None,
                "location_driver": i if img_type == "driver" else None,
                # "adhaar_sames": [],
                "adhaar_enc": enc if img_type == "adhaar" else None,
                # "driver_sames": [],
                "drivers_enc": enc if img_type == "driver" else None,
                # "ad_to_dl_match": [],
                # "dl_to_ad_match": [],
                "sames": []
                # "distant": {"enc": None, "distance": None},
            }
        else:
            if img_type == "adhaar":
                people[name]["adhaar_enc"] = enc
                people[name]["location_adhaar"] = i
            else:
                people[name]["drivers_enc"] = enc
                people[name]["location_driver"] = i

        if people != {}:
            for j in people:
                if j != name:
                    if not isinstance(people[j]["adhaar_enc"], type(None)):
                        result = face_recognition.compare_faces(
                            [enc], people[j]["adhaar_enc"]
                        )
                        dist = face_recognition.face_distance(
                            [enc], people[j]["adhaar_enc"]
                        )
                        result = result[0]
                        dist = dist[0]
                        if result == True:
                            if name not in people[j]["sames"]:
                                people[j]["sames"].append(name)
                                people[name]["sames"].append(j)
                            # if (
                            #     people[j]["distant"]["distance"] == None
                            #     or dist > people[j]["distant"]["distance"]
                            # ):
                            #     people[j]["distant"]["distance"] = dist
                            #     people[j]["distant"]["enc"] = enc

                            # if img_type == "adhaar":
                            #     people[j]["adhaar_sames"].append(name)
                            #     people[name]["adhaar_sames"].append(j)
                            # else:
                            #     people[j]["ad_to_dl_match"].append(name)
                            #     people[name]["dl_to_ad_match"].append(j)

                    if not isinstance(people[j]["drivers_enc"], type(None)):
                        result = face_recognition.compare_faces(
                            [enc], people[j]["drivers_enc"]
                        )
                        dist = face_recognition.face_distance(
                            [enc], people[j]["drivers_enc"]
                        )
                        result = result[0]
                        dist = dist[0]
                        if result == True:
                            if name not in people[j]["sames"]:
                                people[j]["sames"].append(name)
                                people[name]["sames"].append(j)
                            # if (
                            #     people[j]["distant"]["distance"] == None
                            #     or dist > people[j]["distant"]["distance"]
                            # ):
                            #     people[j]["distant"]["distance"] = dist
                            #     people[j]["distant"]["enc"] = enc

                            # if img_type == "adhaar":
                            #     people[j]["dl_to_ad_match"].append(name)
                            #     people[name]["ad_to_dl_match"].append(j)
                            # else:
                            #     people[j]["driver_sames"].append(name)
                            #     people[name]["driver_sames"].append(j)
    return people


def create_dataframe(a):
    df = {"Name": [], "Adhaar": [], "Drivers": [], "Total Same": [], "Sames with": []}
    for i in a:
        df["Name"].append(i)
        df["Adhaar"].append(a[i]["location_adhaar"])
        df["Drivers"].append(a[i]["location_driver"])
        df["Total Same"].append(len(a[i]["sames"]))
        df["Sames with"].append(a[i]["sames"])

    return pd.DataFrame(df)


# {
#     name:{
#         adhaar_sames : [list of people w same adhaar card face]
#         adhaar_enc : encoded adhaar for easy reference
#         driver_sames : [list of ppl w same drivers license face]
#         drivers_enc : encoded drivers for easy reference
#         distant : {
#             enc: encode of the face w the most distant but still true image,
#             distance: dist from the face
#         }
#     }
# }
