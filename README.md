<h1>Photo Database Searchable Webpage Generator</h1>

A Quick Summary: This project creates a convenient, searchable web page of a user’s image collection.

Here’s how it works:

* The program recursively scans user-provided graphic image directories and collects paths to image files.

* Then it creates a Sqlite3 database consisting of image filenames, sizes, creation dates, plus GPS coordinates and altitudes if that information is available in the image files.

* Then it uses a small, local AI engine to create a plain-text description of each image file (details below) and saves the text descriptions in the database.

* Then it creates a Web page consisting of links to all scanned images, plus the AI-generated text descriptions added as titles to each image HTML tag. The descriptions appear when the user hovers a pointing device over an image.

* The user searches the Web page by way of a text entry. As the user enters a search expression, the displayed images change to match the search entry, character by character. This search feature allows the user to very quickly find specific images in large image archives.

* The user has the option to create a second Web page. The first Web page, always created, works correctly while located anywhere on the host system because it uses absolute image file addressing. The second Web page, created if the user sets “relative = True”, uses relative addressing and is saved in the graphic image directory.

This second Web page has what may be a non-obvious advantage – if the user creates a USB stick for portable presentations, the relative-address Web page will work from any system the USB stick is plugged into.

Here are the project’s requirements, some of which may be changed by editing the Python source:

* The Python sqlite3, gpsphoto and ollama libraries, and a few others listed in requirements.txt

* Ollama installed locally

* A specific, small (1.3 GB) LLM : “gemma4:e2b”, may be installed using this Ollama command:

    $ ollama pull  gemma4:e2b

The user may substitute another LLM of similar ability, but the LLM must be able to read and describe graphic images. Many small LLMs can provide the desired text descriptions and will run correctly on small systems.

To prepare the program for scanning and use, create a data record in the Python main() function using the instructions found there:

variable name = (task name,basepath,subdirectory, relative (True/False))

The task name can be anything the user wants -- it’s used to name the database and Web pages. This serves to distinguish tasks that span multiple image directories.

Four example data records are included to familiarize users with the data layout. Be sure to remove these examples, or simply avoid using them in the main program loop.

It’s a good idea to start with a small set of graphic images. This program can create huge databases and Web pages, but this can sometimes lead to problems. I have successfully created Web pages that provide access to over 8,000 images, but:

* Such a large Web page can be difficult to use.

* Only certain browsers will tolerate such large image sets, in fact, in my experience the only browser that tolerates such large image sets is Firefox. In any case it’s best to avoid huge image sets within a single Web page.

When executed, the program does the following:

* It creates two subdirectories -- “databases” and “html_pages” – to receive the results.

* It scans the provided image source directories, accumulating image data in a Sqlite3 database saved in the “databases” subdirectory, and calling on the local LLM to provide text descriptions of each image. The AI text description step takes the most time, typically two seconds per image on a properly equipped laptop.

* After the scan and database creation is complete, the program creates an absolute-address Web page in the “html\_pages” subdirectory. If the user sets the relative flag in the task description, a second Web page is also created and saved in the image directory, which allows relative addressing to work as intended.

Another feature of this program deserves mention. After the initial database and Web page creation, if the user changes the contents of the image directories, adds or removes images, or renames them, on subsequent runs this program will automatically recreate the databases and Web pages to take these changes into account, without recreating existing text descriptions or performing any unnecessary tasks.

This program has been tested on Linux and Windows 11. Obviously it works much better on Linux. One drawback to Windows (among many) is that the absolute-addressed webpage won't work on all browsers, for excruciatingly stupid reasons. This is solved by only using the relative-addressed webpage.

To be sure your system is ready to run this application, perform this step before the first run:

    $ python -m pip install -c requirements.txt

