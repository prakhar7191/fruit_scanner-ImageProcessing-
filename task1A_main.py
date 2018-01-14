#classes and subclasses to import
import cv2
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape):
    #open csv file in append mode
    filep = open('results1A_eYRC#509.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape
    #write to csv
    filep.write(datastr)

def colorOf(BGR = []):
    if ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 60 & BGR[1] >= 0) & (BGR[2] <= 255 & BGR[2] >= 200)):
            return "red",1
    elif ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 255 & BGR[1] >= 200) & (BGR[2] <= 255 & BGR[2] >= 200)):
            return "yellow",2
    elif (( BGR[0] >= 0 & BGR[0] <= 100) & (BGR[1] >= 120 & BGR[1] <= 180) & (BGR[2] == 255)):
            return "orange",3
    elif ((BGR[0] <= 60 & BGR[0] >= 0) & (BGR[1] <= 255 & BGR[1] >= 200) & (BGR[2] <= 60 & BGR[2] >= 0)):
            return "green",4
    elif((BGR[0] <= 255 & BGR[0] >= 200) & (BGR[1] <= 60 & BGR[1] >= 0) & (BGR[2] <= 60 & BGR[2] >= 0)):
            return "blue",5

def main(path):
    original=cv2.imread(path)
    if "test" in path:
        square = cv2.imread('square.jpeg')
        gray_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        ret, thresh_square = cv2.threshold(gray_square,180,255,1)
        _,contours_sqr,heirarchy = cv2.findContours(thresh_square.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt1 = contours_sqr[0]

        edged_image = cv2.Canny(original.copy(),150,150)
        _,contours,heirarchy = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        font = cv2.FONT_HERSHEY_SIMPLEX
        for j in range (0,len(contours),2):
            i=contours[j]
            approx = cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True)
            x = len(approx)
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x1=i[0][0][0]+1
            y1=i[0][0][1]+1
            color,d = colorOf(original[y1,x1])#d is the color index of the required matrix
            area = cv2.contourArea(i)

            if(area < 4000):
                    x=x-1

            if x == 3:
                    writecsv(color,"triangle")
                    cv2.putText(original,str(color)+" triangle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
            elif x == 4:
                    ret = cv2.matchShapes(i,cnt1,1,0.0)
                    if ret < 0.05:
                            writecsv(color,"square")    
                            cv2.putText(original, str(color)+" square", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                    else:
                            writecsv(color,"rectangle")
                            cv2.putText(original, str(color)+" rectangle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)    
            elif x == 5:
                    writecsv(color,"pentagon")
                    cv2.putText(original, str(color)+" pentagon", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
            elif x > 7:
                    writecsv(color,"circle")    
                    cv2.putText(original, str(color)+" circle", (cx, cy), font, 0.4, (0, 0, 0), 1, 0)
                    
        cv2.imwrite(os.getcwd()+"\output"+path[len(path)-5:],original)
                            



#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = ["\\".join([mypath, f]) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('results1A_eYRC#509.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp[2:])
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        #original=cv2.imread(fp)
        #cv2.imshow("fp",fp)
        #cv2.imshow("data",data)
        #open the csv
        filep = open('results1A_eYRC#509.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
