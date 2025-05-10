import cv2
import dlib
import time
import datetime
import numpy as np
import os
import argparse
from scipy.spatial import distance
from threading import Thread
import winsound  # Cho Windows, sử dụng các thư viện khác cho Linux/Mac

def eye_aspect_ratio(eye):
    """Tính tỷ lệ khía cạnh mắt (EAR)"""
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_ratio(mouth):
    """Tính tỷ lệ mở miệng khi ngáp"""
    H = distance.euclidean(mouth[13], mouth[19])  # 62-66
    W = distance.euclidean(mouth[0], mouth[6])    # 48-54
    return H / W if W > 0 else 0

def sound_alarm():
    """Phát âm thanh cảnh báo"""
    winsound.Beep(1000, 1000)

class DrowsinessDetector:
    def __init__(self, args):
        # Tham số
        self.ear_threshold = args.ear_threshold
        self.ear_consec_frames = args.ear_frames
        self.yawn_threshold = args.yawn_threshold
        self.show_landmarks = args.show_landmarks
        self.alarm = args.alarm
        self.log_path = args.log
        self.face_tracking = args.face_tracking
        
        # Khởi tạo các biến theo dõi
        self.eye_counter = 0
        self.yawn_count = 0
        self.yawn_status = False
        self.alarm_on = False
        self.start_time = time.time()
        self.prev_face = None
        self.face_lost_counter = 0
        
        # Khởi tạo detector và predictor
        print("[INFO] Đang tải facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        
        predictor_path = args.shape_predictor
        if not os.path.isfile(predictor_path):
            raise FileNotFoundError(f"File {predictor_path} không tồn tại. Vui lòng tải xuống từ dlib website.")
        
        self.predictor = dlib.shape_predictor(predictor_path)
        
        # Chỉ số cho các bộ phận khuôn mặt
        self.left_eye_idx = list(range(36, 42))
        self.right_eye_idx = list(range(42, 48))
        self.mouth_idx = list(range(48, 68))
        
        # Khởi tạo camera
        print("[INFO] Đang khởi tạo camera...")
        self.cap = cv2.VideoCapture(args.camera)
        
        if not self.cap.isOpened():
            raise ValueError("Không thể mở camera. Vui lòng kiểm tra lại thiết bị.")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Biến cho kích thước cửa sổ và chế độ toàn màn hình
        self.fullscreen = False
        self.screen_width = 1920  # Có thể lấy động
        self.screen_height = 1080  # Có thể lấy động
        self.window_width = int(self.screen_width * 0.8)
        self.window_height = int(self.screen_height * 0.8)
        
        # Tạo file log nếu được yêu cầu
        if self.log_path:
            with open(self.log_path, "a") as f:
                f.write("\n\n" + "="*50 + "\n")
                f.write(f"Phiên phát hiện buồn ngủ bắt đầu lúc {datetime.datetime.now()}\n")
                f.write(f"Ngưỡng EAR: {self.ear_threshold}, Khung hình: {self.ear_consec_frames}, Ngưỡng ngáp: {self.yawn_threshold}\n")
                f.write("="*50 + "\n\n")
    
    def log_event(self, event):
        """Ghi sự kiện vào file log"""
        if self.log_path:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_path, "a") as f:
                f.write(f"[{timestamp}] {event}\n")
    
    def resize_frame(self, frame, target_width, target_height):
        """Resize khung hình để lấp đầy cửa sổ/màn hình, không giữ tỷ lệ"""
        return cv2.resize(frame, (target_width, target_height))
    
    def run(self):
        """Chạy vòng lặp chính của chương trình"""
        print("[INFO] Bắt đầu phát hiện buồn ngủ...")
        
        # Tạo cửa sổ có thể thay đổi kích thước
        window_name = "Hệ thống phát hiện buồn ngủ"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, self.window_width, self.window_height)
        
        # Lưu kích thước cửa sổ hiện tại
        current_width = self.window_width
        current_height = self.window_height

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Không thể đọc khung hình từ camera")
                break
            
            # Resize khung hình gốc để xử lý
            process_frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(process_frame, cv2.COLOR_BGR2GRAY)
            
            # Phát hiện khuôn mặt
            faces = self.detector(gray)
            
            if len(faces) == 0 and isinstance(self.prev_face, dlib.rectangle):
                x, y, w, h = (self.prev_face.left(), self.prev_face.top(), 
                             self.prev_face.width(), self.prev_face.height())
                expand = int(w * 0.5)
                x = max(0, x - expand)
                y = max(0, y - expand)
                right = min(gray.shape[1], x + w + 2*expand)
                bottom = min(gray.shape[0], y + h + 2*expand)
                
                roi = gray[y:bottom, x:right]
                roi_faces = self.detector(roi)
                
                for face in roi_faces:
                    face_rect = dlib.rectangle(
                        face.left() + x,
                        face.top() + y,
                        face.right() + x,
                        face.bottom() + y
                    )
                    faces = [face_rect]
                    break
            
            if len(faces) > 0:
                self.prev_face = faces[0]
            
            # Overlay thông tin lên khung hình xử lý
            self.overlay_info(process_frame, gray, faces)
            
            # Lấy kích thước mục tiêu
            if self.fullscreen:
                target_width, target_height = self.screen_width, self.screen_height
            else:
                target_width, target_height = current_width, current_height
            
            # Resize khung hình để lấp đầy cửa sổ/màn hình
            display_frame = self.resize_frame(process_frame, target_width, target_height)
            
            # Hiển thị khung hình
            cv2.imshow(window_name, display_frame)
            
            # Kiểm tra phím ấn
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('r'):
                self.eye_counter = 0
                self.yawn_count = 0
                print("[INFO] Đã reset các bộ đếm")
            elif key == ord('+'):
                self.ear_threshold += 0.01
                print(f"[INFO] Ngưỡng EAR mới: {self.ear_threshold:.2f}")
            elif key == ord('-'):
                self.ear_threshold = max(0.01, self.ear_threshold - 0.01)
                print(f"[INFO] Ngưỡng EAR mới: {self.ear_threshold:.2f}")
            elif key == ord('f'):
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    cv2.setWindowProperty(window_name, 
                                        cv2.WND_PROP_FULLSCREEN, 
                                        cv2.WINDOW_FULLSCREEN)
                    current_width, current_height = self.screen_width, self.screen_height
                else:
                    cv2.setWindowProperty(window_name, 
                                        cv2.WND_PROP_FULLSCREEN, 
                                        cv2.WINDOW_NORMAL)
                    cv2.resizeWindow(window_name, self.window_width, self.window_height)
                    current_width, current_height = self.window_width, self.window_height
        
        self.cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Chương trình đã kết thúc")
        
    def overlay_info(self, frame, gray, faces):
        """Hiển thị thông tin overlay lên khung hình"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        elapsed_time = time.time() - self.start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        elapsed_str = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
        cv2.putText(frame, f"Thời gian: {elapsed_str}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if len(faces) == 0:
            self.face_lost_counter += 1
            message = "KHONG PHAT HIEN KHUON MAT"
            if self.face_tracking and self.face_lost_counter < 30:
                message = "DANG TIM KIEM KHUON MAT..."
            cv2.putText(frame, message, (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if self.face_lost_counter > 30:
                self.eye_counter = 0
            return
        
        self.face_lost_counter = 0
        face = faces[0]
        
        landmarks = self.predictor(gray, face)
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.left_eye_idx]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.right_eye_idx]
        mouth = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.mouth_idx]
        
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0
        mr = mouth_ratio(mouth)
        
        if self.show_landmarks:
            for (x, y) in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            for (x, y) in mouth:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
        
        left_eye_hull = cv2.convexHull(np.array(left_eye))
        right_eye_hull = cv2.convexHull(np.array(right_eye))
        mouth_hull = cv2.convexHull(np.array(mouth))
        
        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [mouth_hull], -1, (255, 0, 0), 1)
        
        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"MR: {mr:.2f}", (10, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if avg_ear < self.ear_threshold:
            self.eye_counter += 1
            progress = self.eye_counter / self.ear_consec_frames
            bar_length = 200
            bar_height = 20
            filled_length = int(bar_length * progress)
            
            cv2.rectangle(frame, (10, 180), (10 + bar_length, 180 + bar_height), (0, 0, 255), 2)
            cv2.rectangle(frame, (10, 180), (10 + filled_length, 180 + bar_height), (0, 0, 255), -1)
            
            if self.eye_counter >= self.ear_consec_frames:
                cv2.putText(frame, "CANH BAO BUON NGU!", (10, 220),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 200), -1)
                cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
                
                if self.alarm and not self.alarm_on:
                    self.alarm_on = True
                    self.log_event("CẢNH BÁO: Phát hiện buồn ngủ")
                    t = Thread(target=sound_alarm)
                    t.daemon = True
                    t.start()
        else:
            self.eye_counter = 0
            self.alarm_on = False
        
        if mr > self.yawn_threshold:
            if not self.yawn_status:
                self.yawn_count += 1
                self.yawn_status = True
                self.log_event(f"Phát hiện ngáp lần thứ {self.yawn_count}")
            cv2.putText(frame, "NGAP PHAT HIEN!", (10, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 3)
        else:
            self.yawn_status = False
        
        cv2.putText(frame, f"So lan ngap: {self.yawn_count}", (10, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def main():
    parser = argparse.ArgumentParser(description='Hệ thống phát hiện buồn ngủ')
    parser.add_argument('--shape-predictor', type=str, default='shape_predictor_68_face_landmarks.dat',
                        help='Đường dẫn đến file dlib facial landmark predictor')
    parser.add_argument('--ear-threshold', type=float, default=0.25,
                        help='Ngưỡng tỷ lệ khía cạnh mắt để phát hiện mắt nhắm')
    parser.add_argument('--ear-frames', type=int, default=20,
                        help='Số khung hình liên tiếp với EAR dưới ngưỡng để kích hoạt cảnh báo')
    parser.add_argument('--yawn-threshold', type=float, default=0.6,
                        help='Ngưỡng tỷ lệ miệng để phát hiện ngáp')
    parser.add_argument('--camera', type=int, default=0,
                        help='Chỉ số camera (mặc định là 0 cho webcam chính)')
    parser.add_argument('--show-landmarks', action='store_true',
                        help='Hiển thị facial landmarks')
    parser.add_argument('--alarm', action='store_true',
                        help='Bật cảnh báo âm thanh')
    parser.add_argument('--log', type=str, default='',
                        help='Đường dẫn đến file log (để trống nếu không cần ghi log)')
    parser.add_argument('--face-tracking', action='store_true', default=True,
                        help='Bật tính năng theo dõi khuôn mặt liên tục')
    
    args = parser.parse_args()
    
    print("====== Hướng dẫn sử dụng ======")
    print("ESC: Thoát chương trình")
    print("r: Reset bộ đếm")
    print("+: Tăng ngưỡng EAR")
    print("-: Giảm ngưỡng EAR")
    print("f: Chuyển đổi chế độ toàn màn hình")
    print("==============================")
    
    try:
        detector = DrowsinessDetector(args)
        detector.run()
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()