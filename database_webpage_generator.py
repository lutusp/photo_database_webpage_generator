#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ollama
import sqlite3
from pathlib import Path
import time
import re
import sys
import os
from datetime import datetime
from dataclasses import dataclass


# pip install GPSPhoto exifread piexif
from GPSPhoto import gpsphoto


def get_photo_description(model, photopath):
    reply = ""
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant who provides very brief replies",
                },
                {
                    "role": "user",
                    "content": "briefly describe this picture",
                    "images": [
                        f"{photopath}",
                    ],
                },
            ],
        )
        reply = response["message"]["content"]
    except:
        reply = f"get_photo_description: Error reading file: {photopath}"
    return reply


def query_os_file_list(base, subdir):
    files = []
    spec = base + subdir
    result = Path(base).rglob("*", case_sensitive=False)
    for posixpath in result:
        path = str(posixpath)
        if spec in path:
            files += [path]
    files = [f for f in files if not re.search("(?i)MagicLantern", f)]
    files = [f for f in files if re.search(r"(?i)\.(jpg|jpeg|png)$", f)]
    files.sort()
    return files


# a single data line within the target HTML page


def html_line(path, desc, tab):
    return f'{tab}<a href="{path}" target="_blank"><img src="{path}" width=200 title="{desc}" class="gallery-item"></a>'


@dataclass
class Photorec:
    path: str
    size: int
    date_time: datetime
    gpslat: str
    gpslng: str
    altitude: str
    desc: str


# creates a web page containing links to the images
# plus the generated descriptions
# the page has a search entry for the descriptions.
# this can create a huge web page that,
# with linked graphics, will kill most browsers
# ... except firefox


def create_webpage(dir_html, task_name, base, valid_records, relative):
    pic_data = []
    rel_pic_data = []
    tab = ""
    for path in sorted(valid_records):
        rec: Photorec = valid_records[path]
        # create relative path
        relpath = re.sub(base, "./", path)
        # process description string
        desc = re.sub(r'"', r"&quot;", rec.desc)

        # absolute address
        pic_data += [html_line(path, desc, tab)]
        # relative address
        rel_pic_data += [html_line(relpath, desc, tab)]
        tab = " " * 8
    html_data = "\n".join(pic_data)
    with open("page_template.html") as f:
        raw_page = f.read()
    page = re.sub("#html_data#", html_data, raw_page)
    page_name = f"image_search_page_{task_name}.html"
    page_path = f"{dir_html}/{page_name}"
    with open(page_path, "w") as f:
        f.write(page)
    # this relative-address page version
    # is created along with the default
    if relative:
        rel_html_data = "\n".join(rel_pic_data)
        rel_page = re.sub("#html_data#", rel_html_data, raw_page)
        page_path = f"{base}/{page_name}"
        with open(page_path, "w") as f:
            f.write(rel_page)


def process(task_name, base, db_name, subdir, model):
    # these are debugging limits
    max_images = 50000
    db = sqlite3.connect(f"{db_name}")
    curs = db.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS photodata (id INTEGER PRIMARY KEY,path TEXT,size TEXT,datetime TEXT,gpslat TEXT,gpslng TEXT,altitude TEXT,desc TEXT)"
    )
    curs.execute("Select path,size,datetime,gpslat,gpslng,altitude,desc from photodata")
    dbdata = curs.fetchall()

    # acquire a list of existing graphic files
    filelist = query_os_file_list(base, subdir)

    # collect records of existing files, exclude all others
    valid_records = {}
    for item in dbdata:
        rec = Photorec(*item)
        if rec.path in filelist:
            valid_records[rec.path] = rec

    # overconfidently erase all prior table content
    curs.execute("DELETE from photodata")

    # this scan will includes any new files
    for n, path in enumerate(filelist):
        print(f"Processing: {task_name:<12} record {n+1:6} : {path}")
        sys.stdout.flush()
        # recreate all the trivially acquired data
        m_time = os.path.getmtime(path)
        # avoid fractional seconds
        mi_time = int(m_time)
        # make sure this creates a string
        date_time = f"{datetime.fromtimestamp(mi_time)}"
        size = os.path.getsize(path)
        # acquire latitude, longitude, altitude if they exist
        gpslat = "N/A"
        gpslng = "N/A"
        altitude = "N/A"
        # only available from these file types
        if re.search(r"(?i)\.(jpg|jpeg)$", path):
            try:
                data = gpsphoto.getGPSData(path)
                gpslat = data.get("Latitude") or "N/A"
                gpslng = data.get("Longitude") or "N/A"
                altitude = data.get("Altitude") or "N/A"
            except Exception:
                None
        # avoid recreating descriptions, requires much time and processing
        # try to recover prior description
        desc = ""
        if path in valid_records:
            rec: Photorec = valid_records[path]
            desc = rec.desc
        # must create new description, slowest part of this process
        if len(desc) == 0:
            desc = get_photo_description(model, path)
        # create new database record
        curs.execute(
            "INSERT INTO photodata (path,size,datetime,gpslat,gpslng,altitude,desc) VALUES (?,?,?,?,?,?,?)",
            (path, size, date_time, gpslat, gpslng, altitude, desc),
        )
        # replace or update array record
        valid_records[path] = Photorec(
            path, size, date_time, gpslat, gpslng, altitude, desc
        )
    # the database and array should now contain all valid records
    db.commit()
    db.close()
    return valid_records


def main():
    dir_html = "html_pages"
    dir_db = "databases"
    for dir in (dir_html, dir_db):
        if not os.path.exists(dir):
            os.mkdir(dir)

    model = "gemma4:e2b"  # via ollama, the AI model used to create photo descriptions

    # layout: variable name = (task name,basepath,subdirectory, relative (True/False))

    alaska = ("alaska", "/netbackup/GRFIX/", "alaska_", False)
    travels = ("travels", "/netbackup/GRFIX/", "all_travels_", False)
    winter = ("winter", "/netbackup/GRFIX/", "Winter_travel_pics", False)
    worldsail = ("worldsail", "/netbackup/GRFIX/", "WorldSail", False)

    global_start = time.time()
    for task in (worldsail, travels, winter, alaska):
        task_name, base, subdir, relative = task
        db_name = f"{dir_db}/photo_database_{task_name}.db"
        print(f"* Begin task: {task_name} ...")
        sys.stdout.flush()
        start_time = time.time()
        valid_records = process(task_name, base, db_name, subdir, model)
        create_webpage(dir_html, task_name, base, valid_records, relative)
        end_time = time.time()
        print(
            f"* Done with {task_name}. Elapsed time: {end_time-start_time:.2f} seconds."
        )
    global_end = time.time()
    global_elapsed = global_end - global_start
    print(
        f"*** Time for all tasks: {global_elapsed:.2f} seconds or {global_elapsed/60.0:.2f} minutes."
    )


if __name__ == "__main__":
    main()
