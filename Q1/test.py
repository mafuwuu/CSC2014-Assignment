import numpy as np
import cv2

#add files into list
videofiles = ["street.mp4","exercise.mp4","office.mp4"]
overlay =  cv2.VideoCapture("talking.mp4")
overlay.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # float `width`
overlay.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
width = 320
height = 480


video_index = 0
cap = cv2.VideoCapture(videofiles[0])
out = cv2.VideoWriter('processed_video.avi',cv2.VideoWriter_fourcc(*'MJPG'),30.0,(1280,720))

while(cap.isOpened()):
    ret, frame = cap.read()

    if int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) != 1280:
        if frame is None:
            video_index  == 2
        else:
            frame = cv2.resize(frame, (1280, 720))
    if frame is None:
        video_index += 1
        if video_index >= len(videofiles):
            break
        
        cap = cv2.VideoCapture(videofiles[ video_index ])
        ret, frame = cap.read()
    
    cv2.imshow('frame',frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

final = cv2.VideoCapture('processed_video.avi')
x = 50
y = 50
video_frame_counter = 0
while final.isOpened():
    # Capture frame-by-frame
    ret, frame = final.read()

    if ret:
        ret_video, frame_video = overlay.read()
        video_frame_counter += 1

        if video_frame_counter == overlay.get(cv2.CAP_PROP_FRAME_COUNT):
            video_frame_counter = 0
            overlay.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if ret_video:
            # add image to frame
            frame_video = cv2.resize(frame_video, (width, height))
            frame[y:y + height, x:x + width] = frame_video

            '''
            tr = 0.3 # transparency between 0-1, show camera if 0
            frame = ((1-tr) * frame.astype(np.float) + tr * frame_vid.astype(np.float)).astype(np.uint8)
            '''
            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Exit if ESC key is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break
            
final.release()
cap.release()
out.release()
cv2.destroyAllWindows()