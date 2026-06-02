\# photo\_database\_webpage\_generator

This Python project does several things:

  \* It scans user-provided graphic image directories and collects the names of image files.

  \* It then creates a Sqlite3 database consisting of image filenames, sizes, creation dates, plus GPS coordinates and altitudes if that information is available in the image file.

  \* It uses a local AI engine to create a plain-language description of each image file (details below) and saves the generated description in the database.

  \* It creates a Web page consisting of links to all scanned images, plus the AI-generated descriptions added as titles to each image HTML tag – this causes the descriptions to appear when the user hovers a pointing device over an image.

The Web page includes a text entry that allows the user to enter a search string. As the user enters a search, the displayed images change to those whose descriptions matrch the search entry.

The user may choose to create two Web pages. One Web page, always created, works correctly while located anywhere on the host system because it uses absolute image file addressing. The second Web page, created if the user sets “relative = True”, uses relative addressing and is saved in the graphic image directory.

This second Web page has a non-obvious advantage – if the user creates a USB stick for portable presentations, the relative-address Web page will work from any system the USB stick is connected to.
