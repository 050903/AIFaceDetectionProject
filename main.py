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
    # Tần số 1000Hz trong 1 giây
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
        self.prev_face = None  # Lưu khuôn mặt từ frame trước
        self.face_lost_counter = 0  # Đếm số frame mất dấu khuôn mặt
        
        # Khởi tạo detector và predictor
        print("[INFO] Đang tải facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        
        # Kiểm tra file landmark predictor
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
        
        # Điều chỉnh độ phân giải camera để cải thiện hiệu suất
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
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
    
    def run(self):
        """Chạy vòng lặp chính của chương trình"""
        print("[INFO] Bắt đầu phát hiện buồn ngủ...")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Không thể đọc khung hình từ camera")
                break
            
            # Resize để cải thiện hiệu suất
            frame = cv2.resize(frame, (640, 480))
            
            # Chuyển đổi sang ảnh xám
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Phát hiện và theo dõi khuôn mặt động
            # Sử dụng phát hiện khuôn mặt mỗi frame để bám theo liên tục
            faces = self.detector(gray)
            
            # Nếu không phát hiện khuôn mặt nhưng có khuôn mặt trước đó,
            # thử mở rộng vùng tìm kiếm xung quanh vị trí cũ
            if len(faces) == 0 and isinstance(self.prev_face, dlib.rectangle):
                # Lấy tọa độ khuôn mặt trước đó và mở rộng vùng tìm kiếm
                x, y, w, h = (self.prev_face.left(), self.prev_face.top(), 
                             self.prev_face.width(), self.prev_face.height())
                
                # Mở rộng vùng tìm kiếm
                expand = int(w * 0.5)  # Mở rộng thêm 50% kích thước
                x = max(0, x - expand)
                y = max(0, y - expand)
                right = min(gray.shape[1], x + w + 2*expand)
                bottom = min(gray.shape[0], y + h + 2*expand)
                
                # Tạo ROI (Region of Interest) và chỉ tìm kiếm trong vùng này
                roi = gray[y:bottom, x:right]
                roi_faces = self.detector(roi)
                
                # Điều chỉnh tọa độ của các khuôn mặt tìm thấy
                for face in roi_faces:
                    face_rect = dlib.rectangle(
                        face.left() + x,
                        face.top() + y,
                        face.right() + x,
                        face.bottom() + y
                    )
                    faces = [face_rect]
                    break
            
            # Lưu khuôn mặt hiện tại để theo dõi trong frame tiếp theo
            if len(faces) > 0:
                self.prev_face = faces[0]
            
            # Overlay thông tin
            self.overlay_info(frame, gray, faces)
            
            # Hiển thị khung hình
            cv2.imshow("Hệ thống phát hiện buồn ngủ", frame)
            
            # Kiểm tra phím ấn
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('r'):  # Reset các bộ đếm
                self.eye_counter = 0
                self.yawn_count = 0
                print("[INFO] Đã reset các bộ đếm")
            elif key == ord('+'):  # Tăng ngưỡng EAR
                self.ear_threshold += 0.01
                print(f"[INFO] Ngưỡng EAR mới: {self.ear_threshold:.2f}")
            elif key == ord('-'):  # Giảm ngưỡng EAR
                self.ear_threshold = max(0.01, self.ear_threshold - 0.01)
                print(f"[INFO] Ngưỡng EAR mới: {self.ear_threshold:.2f}")
        
        # Giải phóng tài nguyên
        self.cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Chương trình đã kết thúc")
        
    def overlay_info(self, frame, gray, faces):
        """Hiển thị thông tin overlay lên khung hình"""
        # Hiển thị thời gian
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Hiển thị thời gian chạy
        elapsed_time = time.time() - self.start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        elapsed_str = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
        cv2.putText(frame, f"Thời gian: {elapsed_str}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Nếu không có khuôn mặt
        if len(faces) == 0:
            self.face_lost_counter += 1
            message = "KHONG PHAT HIEN KHUON MAT"
            
            # Nếu sử dụng tính năng theo dõi, hiển thị thông báo tìm kiếm
            if self.face_tracking and self.face_lost_counter < 30:
                message = "DANG TIM KIEM KHUON MAT..."
            
            cv2.putText(frame, message, (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Chỉ reset bộ đếm nếu mất dấu quá lâu (30 frames)
            if self.face_lost_counter > 30:
                self.eye_counter = 0
            return
        else:
            # Reset bộ đếm mất dấu khi tìm thấy khuôn mặt
            self.face_lost_counter = 0
        
        # Xử lý cho mỗi khuôn mặt (lấy khuôn mặt đầu tiên)
        face = faces[0]
        
        # Lấy facial landmarks
        landmarks = self.predictor(gray, face)
        
        # Vẽ hình chữ nhật quanh khuôn mặt
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Lấy tọa độ các điểm landmarks
        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.left_eye_idx]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.right_eye_idx]
        mouth = [(landmarks.part(n).x, landmarks.part(n).y) for n in self.mouth_idx]
        
        # Tính các tỷ lệ
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0
        mr = mouth_ratio(mouth)
        
        # Vẽ landmarks nếu được yêu cầu
        if self.show_landmarks:
            for (x, y) in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            for (x, y) in mouth:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
        
        # Tạo convex hull cho mắt để trực quan hóa tốt hơn
        left_eye_hull = cv2.convexHull(np.array(left_eye))
        right_eye_hull = cv2.convexHull(np.array(right_eye))
        mouth_hull = cv2.convexHull(np.array(mouth))
        
        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [mouth_hull], -1, (255, 0, 0), 1)
        
        # Hiển thị giá trị EAR và MR
        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"MR: {mr:.2f}", (10, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Phát hiện mắt nhắm
        if avg_ear < self.ear_threshold:
            self.eye_counter += 1
            
            # Hiển thị thanh tiến trình
            progress = self.eye_counter / self.ear_consec_frames
            bar_length = 200
            bar_height = 20
            filled_length = int(bar_length * progress)
            
            cv2.rectangle(frame, (10, 180), (10 + bar_length, 180 + bar_height), (0, 0, 255), 2)
            cv2.rectangle(frame, (10, 180), (10 + filled_length, 180 + bar_height), (0, 0, 255), -1)
            
            if self.eye_counter >= self.ear_consec_frames:
                # Phát cảnh báo
                cv2.putText(frame, "CANH BAO BUON NGU!", (10, 220),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                
                # Vẽ nền đỏ để báo động
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 200), -1)
                cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
                
                if self.alarm and not self.alarm_on:
                    self.alarm_on = True
                    self.log_event("CẢNH BÁO: Phát hiện buồn ngủ")
                    # Bắt đầu một thread mới để phát âm thanh
                    t = Thread(target=sound_alarm)
                    t.daemon = True
                    t.start()
        else:
            self.eye_counter = 0
            self.alarm_on = False
        
        # Phát hiện ngáp
        if mr > self.yawn_threshold:
            if not self.yawn_status:
                self.yawn_count += 1
                self.yawn_status = True
                self.log_event(f"Phát hiện ngáp lần thứ {self.yawn_count}")
            
            cv2.putText(frame, "NGAP PHAT HIEN!", (10, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 3)
        else:
            self.yawn_status = False
        
        # Hiển thị số lần ngáp
        cv2.putText(frame, f"So lan ngap: {self.yawn_count}", (10, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def main():
    """Hàm chính để thiết lập các tham số và khởi chạy chương trình"""
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
    
    # Thông báo về các phím tắt
    print("====== Hướng dẫn sử dụng ======")
    print("ESC: Thoát chương trình")
    print("r: Reset bộ đếm")
    print("+: Tăng ngưỡng EAR")
    print("-: Giảm ngưỡng EAR")
    print("==============================")
    
    # Tạo và chạy detector
    try:
        detector = DrowsinessDetector(args)
        detector.run()
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()