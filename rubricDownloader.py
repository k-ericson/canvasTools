# Kathleen Ericson
# kericson@utm.edu
# Rubric Downloader and ABET report generator - for a given class and assignment, it will generate a *.txt rubric containing scores and comments from the grader.  The rubric text files are stored by student name in LastFirst.txt.  It will then generate an ABETReport.txt file - it outputs student name and grade from higest to lowest.  It additionally prints out "HIGHEST" next to the top grade, "LOWEST" next to the lowest non-zero grade (assuming zeros coincide largely with no submissions...), and middle next to the grade that is at the halfway point betwen the highest and lowest index (not perfect, but it's something!)  The goal was to make it easier to pull out specifically highest, lowest, and median grades for ABET

#sys for command lines, requests for API GET requests, json to help parse!
import sys
import requests
import json

#make sure we have the correct number of arguments
if len(sys.argv) < 4:
    print("proper usage: python3 rubricDownloader.py classID assignmentID OAuth2Code")
    sys.exit(-1)

classID = str(sys.argv[1])
assignmentID = str(sys.argv[2])
code = str(sys.argv[3])


#Make a request for the assignmnt with full rubric assessment and any submission comments
stuff = requests.get('https://utm.instructure.com/api/v1/courses/'+str(classID)+'/assignments/'+str(assignmentID)+'/submissions?include[]=full_rubric_assessment&include[]=submission_comments&access_token='+str(code))

# Convert request response to json
jstuff = stuff.json()


# get some meta information for the assignment - full rubric descriptions, total possible points, etc
req2 = str('https://utm.instructure.com/api/v1/courses/'+str(classID)+'/assignments/'+assignmentID+'?access_token='+str(code))

# so we can sort by grade at the end
grades = []

#gathering assignment metadata
stuff2 = requests.get(req2)

#holding the long_description for each rubric category
topics = []
#holding the max score for each rubric category
best = []

for item in stuff2.json()['rubric']:
    topics.append(item['long_description'])
    best.append(item['points'])

# what is the total point possible for this assignment
maxPoints = stuff2.json()['points_possible']

# Now actually looping over the graded rubrics
for grade in jstuff:
    userID = str(grade['user_id'])
    #get student name for this graded rubric
    userInfo = requests.get('https://utm.instructure.com/api/v1/courses/'+classID+'/users/'+userID+'?access_token='+code)
    juserInfo = userInfo.json()
    sortable = juserInfo['sortable_name'].split(', ')
    userName = juserInfo['name']
    fname = str(sortable[0]+sortable[1])
    # create and open output file with name LastFirst.txt for each student
    fout = open(fname+'.txt', 'w')
    # write student name and grade at the top of the file
    fout.write('Name: ' + userName+'\nGrade: '+grade['grade']+'/' + str(maxPoints) + '\n\n')
    # add the name and grade to our list for the ABET report file
    grades.append((float(grade['grade']), userName))
    # for each category (topic) in the rubric, print out the description and grade out of possible points
    for t in range(len(topics)):
        try:
            fout.write(topics[t]+": "+str(grade['full_rubric_assessment']['data'][t]['points'])+'/' + str(best[t]) + '\n'+grade['full_rubric_assessment']['data'][t]['comments']+'\n\n')
        except:
            None
    
    # create a section for any additional comments
    fout.write('Comments:\n')
    try:
        fout.write(grade['submission_comments'][0]['comment'] + '\n')
    except:
        None
    #close up the file
    fout.close()

grades.sort(reverse=True)
lowestNonZero = len(grades)-1
while grades[lowestNonZero][0] == '0':
    lowestNonZero -= 1
#generate ABET Report file - high, middle, and low grades marked for easy backup
#if you only want these rubrics, you could create a dictionary above instead of dumping all!
fo = open('ABETReport.txt', 'w')
for i in range(len(grades)):
    fo.write(grades[i][1]+" - "+str(grades[i][0]))
    if i is 0:
        fo.write(" HIGHEST")
    elif i is lowestNonZero:
        fo.write(" LOWEST")
    elif i is lowestNonZero//2:
        fo.write(" MIDDLE")
    fo.write("\n")
fo.close()
