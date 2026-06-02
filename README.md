\# photo\_database\_webpage\_generator

This Python project does several things:

\* It scans user-provided graphic image directories and collects the names of image files.

\* It creates a Sqlite3 database consisting of image filenames, sizes, creation dates, plus GPS coordinates and altitudes if that information is available in the image files.

\* It uses a local AI engine to create a plain-text description of each image file (details below) and saves the generated descriptions in the database.

\* It creates a Web page consisting of links to all scanned images, plus the AI-generated text descriptions added as titles to each image HTML tag – this causes the descriptions to appear when the user hovers a pointing device over an image.

The Web page includes a text entry that allows the user to enter a search string. As the user enters a search, the displayed images change to those whose descriptions match the search entry. This search feature allows the user to find specific images in large image archives.

The user may choose to create two Web pages. The first Web page, always created, works correctly while located anywhere on the host system because it uses absolute image file addressing. The second Web page, created if the user sets “relative = True”, uses relative addressing and is saved in the graphic image directory.

This second Web page has what may be a non-obvious advantage – if the user creates a USB stick for portable presentations, the relative-address Web page will work from any system the USB stick is plugged into.

Here are the project’s requirements, some of which may be changed by editing the Python source:

\* The Python sqlite3, gpsphoto and ollama libraries

\* Ollama installed locally

\* A specific, small (1.3 GB) LLM : “gemma4:e2b”, may be installed using this ollama command:

$ ollama pull  gemma4:e2b

The user may substitute another LLM of similar ability, but the LLM must be able to read and describe graphic images.

To prepare the program for scanning and use, create a data record in the main() function using the instructions found there:

\# layout: variable name = (task name,basepath,subdirectory, relative (True/False))

Four example data records are included to familiarize users with the data layout. Be sure to remove these examples, or simply avoid using them in the main program loop.

It’s a good idea to start with a small set of graphic images. This program can create huge databases and Web pages, but this can sometimes lead to problems. I have successfully created Web pages that provide access to over 8,000 images, but:

\* Such a large Web page can be difficult to use.

\* Only certain browsers will tolerate such large image sets, in fact, in my experience the only browser that tolerates such large image sets is Firefox. In any case it’s best to avoid huge image sets within a single Web page.

In practice, when presented with a large image collection, the program does the following:

\* It creates two subdirectories -- databases and html\_pages – to receive the results.

\* It scans the provided image source directories, accumulating image data in a Sqlite3 database and calling on the local LLM to provide text descriptions of each image. The AI text description step takes the most time, typically two seconds per image on a properly equipped laptop.

\* After the scan and database creation is complete, the program creates an absolute-address Web page in the “html\_pages” subdirectory. If the user sets the relative flag in the task description, a second Web page is created and saved in the image directory, which allows relative addressing to work as intended.

Another feature of this program deserves mention. After the initial database and Web page creation, if the user changes the contents of the image directories, adds or removes images, or renames them, on subsequent runs this program will automatically recreate the databases and Web pages to take these changes into account, without creating new text descriptions or performing any unnecessary tasks.

I have only run this program on Linux, but it should function the same on Windows, and if not, please tell me – I’ll see about making it more cross-platform.

