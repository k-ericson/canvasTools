# canvasTools
some scripts to work with Canvas LMS API

## rubricDownloader.py
This is a quick little program that will pull down rubric grades and comments for a given assignment, creating an individual file with this information for each student.
It will also create a file called ABETReport.txt that will have an overall listing of each student name and grade, sorted from highest grade to lowest.  It will further mark the highest grade, lowest non-zero grade, and the grade that falls in the middle (to hopefully make pulling out these grades a bit easier)

To run:
<tt>python3 rubricDownloader.py ClassID AssignmentID OAuth2Code</tt>

