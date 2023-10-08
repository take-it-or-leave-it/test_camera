import cv2
cap = cv2.VideoCapture(2)
if cap.isOpened:
    file_path = 'record.mp4'
    fps = 20
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')            # 인코딩 포맷 문자
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width), int (height))                   # 프레임 크기
    
    out = cv2.VideoWriter(file_path, fourcc, fps, size) # VideoWriter 객체 생성
    while True:
        ret, frame = cap.read()
        if ret:
            #cv2.imshow('camera-recording', frame)
            out.write(frame)                            # 파일 저장
            if cv2.waitKey(int(200/fps)) != -1:
                break
        else:
            print('no file!')
            break
    out.release()                                       # 파일 닫기
else:
    print("Can`t open camera!")
cap.release()
cv2.destroyAllWindows()

## 0 , 2 
# numpy.ndarray <-- frame type
## 0 1 2 3 중 2개임.
## raspberry pi4 는 plug and play 지원 X 