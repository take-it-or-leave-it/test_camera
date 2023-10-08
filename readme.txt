2023-10-07 usb hub test

    <결과>
    usb hub 에 카메라 3개 정상적으로 작동
    index 0 , 2 , 4 순으로 연결하면됨.

2023-10-07 cam 순차 입력 test

    usb hub usb port 연결
    camera 2 개 순차입력 시,
    0.024~0.026? 정도의 delay 발생. 

    이는 30frame 1/30s  cam 안에서 순차입력 -> 동시입력으로 봐도무방함

    <결과>
    cam 1개 이미지 읽어오는데 '0.01s'정도로 생각하면됨

2023-10-07 calibration test
    cam 왜곡이 너무 심해서 왜곡 제거 시 해상도 극단적으로 낮아짐.

    <결과>
    # raspberry pi 환경
    왜곡 제거시 640 480 -> 52 59


    # 노트북환경
    왜곡 제거시 640 480 -> 205, 261

2023-10-01 ~ 2023-10-07 stitch test
    stitch(=panorama영상만들기) 시 카메라 '왜곡 제거'는 필수.  

    하지만 '왜곡 제거' 시 해상도가 아주 작이짐.

    이에 따라 현재 스펙의 카메라로 stitch 기술 구현 시 '아주 많은' 카메라가 요구됨.

    <결과>
    stitch 기능 구현 하지 않기로함 

2023-10-07 horiziontal_image_concat multi-cam test
    stitch(panorama)기능 구현 말고

    앞 카메라 1개 , 뒤 카메라 2개 를 가로로 붙여서 한번에
    car_detection 이미지 모델을 돌릴 것임.

    <capture 중요>
    cap2.set(cv.CAP_PROP_FPS, 15.0)   # opencv video_capture 는 30 fps 로 고정해서 받아옴 --> 15fps 로 줄였음
    cap2.set(cv.CAP_PROP_FOURCC,cv.VideoWriter_fourcc('M','J','P','G'))  --> 'DIVX' 보다 가벼운 'MJPG' 코덱으로 변경

    <capture 시간 결과> 
    3개 이미지 동시 받는 거 
    0.027sec 정도 걸림.

    <resize 시간>
    detect 모델에는 hd해상도만 들어감 그래서 h : 720 , w : 1280 으로 고정해야함.
    시간  0.00576sec



2023-10-08 hconcat image 에 대한 detection 처리

    concat image = 1280 * 720 ( w * h)

    전면부 카메라 1대
        0~419 ( 420)

    후면부 카메라 2대
        420~849 (430)
        850 ~ 1279 (430)
    
    <중요사항>
    "일단 lane detection 탐지가 진짜 1280 720 고정"
    이에 따라 각 카마레 이미지에 대한 lane detection 처리가 어떻게 되야할지 고민.

    <고민0>
    3개 이미지(640*480) 입력 -> 1개(1280*720)로 합치기 -> car detection 진행 -> car 좌표값(전면1,후면2) 가져옴.
    -> 이후 3개 각각 이미지(640*480) -> 3개 각각 이미지 reszie(1280 * 720) --> lane detection 진행 -->
    -> lane 좌우 값 가져옴 --> lane 좌우 값 안에 car 좌표값 있는지 확인(정면 차선에 차 여부 확인 알고리즘)
    
    for visualize
    3개 각각 이미지 (640 * 480) -> 1 개로 (1280 * 720 합치기) --> 자동차 bounding box + 차선 검출 보여주기 


    <고민1> 
    카메라 해상도 개 조그마한데
    그냥 앞에 적당히 잘라서 정면만 확인하기?
    정면 말고 옆 차선에 차가 있다고 인식 할 수 있을까? --> 앞 차선만 보일거 같음 ㅇㅇ

    너비가 640 이니깐
    예를들어 280 ~ 320 ~ 360
    320 +- 40 사이에 차가 detection 되면 정면에 차가 있다고 인식하는거지.
    lane detection 자체를 날려버리는 것도 방법 일 수 있음. 

    

    