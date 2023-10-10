import cv2
import numpy as np

#face detection
face_cascade = cv2.CascadeClassifier("face_detector.xml")

vid = cv2.VideoCapture('office.mp4') #load video here

#read images
img1 = cv2.imread('watermark1.png',cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('watermark2.png', cv2.IMREAD_UNCHANGED)

counter  = 0

#save video after blurring
out = cv2.VideoWriter('processed_video.avi',cv2.VideoWriter_fourcc(*'MJPG'),30.0,(1280,720))

#overlay settings
overlay =  cv2.VideoCapture("talking.mp4")
overlay.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  
overlay.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
width = 320
height = 180

#watermarking
def watermarking(counter):
    global frame
    if counter < 100:
        frame = cv2.addWeighted(frame, 1.0, img1, 1.0, 0)
        return frame
    else:
        frame = cv2.addWeighted(frame, 1.0, img2, 1.0, 0)
        return frame

while True:
   _,frame = vid.read()
#resize all videos to 1280x720 if theres a frame   
   if _:
       if int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)) != 1280:
           frame = cv2.resize(frame, (1280, 720))
   else:
        break       

   counter +=1
   if frame is None:
       break
   else:
       watermarking(counter)
      
   #face detection for blurring
   faces = face_cascade.detectMultiScale(frame, 1.04, 3)
   
   for (x, y, w, h) in faces:
       frame[y:y+h,x:x+w] = cv2.GaussianBlur(frame[y:y+h,x:x+w],(15,15),cv2.BORDER_TRANSPARENT)       
       
       cv2.imshow("output",frame)
       out.write(frame)      
       if cv2.waitKey(1) == 27 or 0xFF == ord('q'):
            break
       
final = cv2.VideoCapture('processed_video.avi')

#x,y location for the talking.mp4 video 
x = 50
y = 50

#save video after blurring + adding talking.mp4
overlay_output = cv2.VideoWriter('Blurred_Video_talking.mp4',cv2.VideoWriter_fourcc(*'MPV4'),30.0,(1280,720))

while final.isOpened():
    # Capture frame-by-frame
    ret, frame = final.read()

    #checking if there is an existing frame
    if ret:
        # read the overlay
        ret_video, frame_video = overlay.read()

        overlay.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if ret_video:
            # add overlay to frame using the set parameters
            frame_video = cv2.resize(frame_video, (width, height))
            frame[y:y + height, x:x + width] = frame_video

            # display the resulting frame
            cv2.imshow('frame', frame)
            #video after blurring + adding talking.mp4
            overlay_output.write(frame)      

            # cancel the vid if the vid ends or if esc key is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break
    else:
        break
        
       
vid.release()
overlay_output.release()
cv2.destroyAllWindows()