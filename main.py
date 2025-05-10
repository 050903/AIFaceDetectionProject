import cv2
import dlib
import time
import datetime
import numpy as np
import os
import argparse
from scipy.spatial import distance
from threading import Thread
import winsound  # For Windows, use other libraries for Linux/Mac
import collections # Added for deque
import sys

def eye_aspect_ratio(eye):
    """Calculate Eye Aspect Ratio (EAR)"""
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_ratio(mouth):
    """Calculate Mouth Aspect Ratio (MAR) for yawning"""
    H_M = distance.euclidean(mouth[13], mouth[19])  # Height
    W_M = distance.euclidean(mouth[0], mouth[6])    # Width
    return H_M / W_M if W_M > 0 else 0

def play_sound_alert():
    """Play alert sound"""
    winsound.Beep(1000, 1000)

class DrowsinessDetector:
    def __init__(self, args):
        self.ear_threshold = args.ear_threshold
        self.ear_consec_frames = args.ear_frames
        self.yawn_threshold = args.yawn_threshold
        self.show_landmarks = args.show_landmarks
        self.log_path = args.log
        self.face_tracking = args.face_tracking
        self.perclos_window_seconds = args.perclos_window
        self.runtime_alarm_active = args.alarm
        self.drowsiness_event_notified = False
        self.yawn_event_notified = False
        self.eye_blink_counter = 0
        self.yawn_counter = 0
        self.current_yawn_event = False
        self.start_time = time.time()
        self.prev_face_rect = None
        self.face_lost_frames_counter = 0
        self.perclos_frame_history = collections.deque()
        self.perclos_value = 0.0
        self.drowsiness_alert_visual_active = False
        self.yawn_alert_visual_active = False      
        self.screen_flash_on = False
        self.last_flash_toggle_time = 0
        self.flash_interval_seconds = 0.25

        print(f"[INFO] Initial runtime sound/flash alarm state (key 'a'): {'ON' if self.runtime_alarm_active else 'OFF'}")
        if not self.runtime_alarm_active:
            print("[INFO] To enable sound/flash for events, press 'a'.")

        print("[INFO] Loading facial landmark predictor...")
        self.face_detector = dlib.get_frontal_face_detector()
        predictor_path = args.shape_predictor
        if not os.path.isfile(predictor_path):
            raise FileNotFoundError(f"Shape predictor: {predictor_path} not found.")
        self.landmark_predictor = dlib.shape_predictor(predictor_path)
        
        self.left_eye_indices = list(range(36, 42))
        self.right_eye_indices = list(range(42, 48))
        self.mouth_indices = list(range(48, 68))
        
        print("[INFO] Initializing camera...")
        self.video_capture = cv2.VideoCapture(args.camera) # Use args.camera
        if not self.video_capture.isOpened():
            # Try with DSHOW backend as a fallback for Windows if MSMF fails
            print("[WARN] MSMF backend failed, trying DSHOW...")
            self.video_capture = cv2.VideoCapture(args.camera + cv2.CAP_DSHOW)
            if not self.video_capture.isOpened():
                raise ValueError("Cannot open camera with MSMF or DSHOW. Please check your device and permissions.")
        
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.fullscreen_mode = False
        try:
            import tkinter as tk
            root = tk.Tk()
            self.screen_width = root.winfo_screenwidth()
            self.screen_height = root.winfo_screenheight()
            root.destroy()
        except ImportError:
            self.screen_width, self.screen_height = 1920, 1080
        self.window_width_default = int(self.screen_width * 0.8)
        self.window_height_default = int(self.screen_height * 0.8)
        
        if self.log_path:
            try:
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n{'='*50}\nSession started: {datetime.datetime.now()}\n")
                    f.write(f"EAR Th:{self.ear_threshold}, EAR Fr:{self.ear_consec_frames}, Yawn Th:{self.yawn_threshold}, PERCLOS Win:{self.perclos_window_seconds}s\n")
                    f.write(f"Initial Runtime Alarm (sound/event flash): {'ON' if self.runtime_alarm_active else 'OFF'}\n{'='*50}\n\n")
            except Exception as e:
                print(f"[ERROR] Log init failed: {e}"); self.log_path = None
    
    def log_and_print_event(self, event_message):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{ts}] {event_message}"
        try: print(full_msg)
        except UnicodeEncodeError: print(full_msg.encode(sys.stdout.encoding if sys.stdout.encoding else 'ascii', errors='replace').decode())
        if self.log_path:
            try:
                with open(self.log_path, "a", encoding="utf-8") as f: f.write(full_msg + "\n")
            except Exception as e: print(f"[ERROR] Log write failed: {e}")
    
    def resize_frame(self, frame, target_width, target_height):
        return cv2.resize(frame, (int(target_width), int(target_height)))
    
    def run(self):
        print("[INFO] Starting detection...")
        win_name = "Drowsiness Detection System"
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(win_name, self.window_width_default, self.window_height_default)
        curr_disp_w, curr_disp_h = self.window_width_default, self.window_height_default

        while True:
            ret, frame = self.video_capture.read()
            if not ret: self.log_and_print_event("ERROR: Cannot read frame."); break
            proc_fr = cv2.resize(frame, (640, 480))
            gray_fr = cv2.cvtColor(proc_fr, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector(gray_fr)
            
            if not faces and self.face_tracking and isinstance(self.prev_face_rect, dlib.rectangle):
                x,y,w,h = self.prev_face_rect.left(),self.prev_face_rect.top(),self.prev_face_rect.width(),self.prev_face_rect.height()
                exp=int(w*0.5); xr,yr=max(0,x-exp),max(0,y-exp); rr,br=min(gray_fr.shape[1],x+w+exp),min(gray_fr.shape[0],y+h+exp)
                roi=gray_fr[yr:br,xr:rr]
                if roi.size>0: 
                    roi_f=self.face_detector(roi)
                    if roi_f: faces=[dlib.rectangle(roi_f[0].left()+xr,roi_f[0].top()+yr,roi_f[0].right()+xr,roi_f[0].bottom()+yr)]
            
            if faces: self.prev_face_rect=faces[0]; self.face_lost_frames_counter=0
            else: self.face_lost_frames_counter+=1

            curr_time = time.time()
            
            flash_active_for_event = self.drowsiness_alert_visual_active or \
                                     (self.yawn_alert_visual_active and self.runtime_alarm_active)
            if flash_active_for_event:
                if curr_time - self.last_flash_toggle_time > self.flash_interval_seconds:
                    self.screen_flash_on = not self.screen_flash_on
                    self.last_flash_toggle_time = curr_time
                if self.screen_flash_on:
                    flash_overlay = proc_fr.copy()
                    flash_color = (0,0,200)
                    if self.yawn_alert_visual_active and self.runtime_alarm_active and not self.drowsiness_alert_visual_active:
                         flash_color = (0, 100, 220)
                    cv2.rectangle(flash_overlay, (0,0), (proc_fr.shape[1],proc_fr.shape[0]), flash_color, -1)
                    cv2.addWeighted(flash_overlay, 0.3, proc_fr, 0.7, 0, proc_fr)
            else:
                self.screen_flash_on = False

            self.draw_overlay_info(proc_fr, gray_fr, faces, curr_time)
            
            tgt_w, tgt_h = curr_disp_w, curr_disp_h
            if self.fullscreen_mode: tgt_w,tgt_h = self.screen_width,self.screen_height
            else:
                try:
                    _, _, ww, wh = cv2.getWindowImageRect(win_name)
                    if ww > 0 and wh > 0:
                        tgt_w, tgt_h = ww, wh
                        curr_disp_w, curr_disp_h = ww, wh
                except cv2.error as e:
                    print(f"[WARN] Unable to get window dimensions: {e}")
                except cv2.error: pass
            disp_fr = self.resize_frame(proc_fr, tgt_w, tgt_h)
            cv2.imshow(win_name, disp_fr)
            
            key = cv2.waitKey(1)&0xFF
            if key==27: break
            elif key==ord('r'):
                self.eye_blink_counter=0; self.yawn_counter=0; self.perclos_frame_history.clear(); self.perclos_value=0.0
                self.drowsiness_alert_visual_active=False; self.yawn_alert_visual_active=False; self.screen_flash_on=False
                self.drowsiness_event_notified=False; self.yawn_event_notified=False
                self.log_and_print_event("Counters and states reset.")
            elif key==ord('+'): self.ear_threshold+=0.01; self.log_and_print_event(f"EAR Thresh: {self.ear_threshold:.2f}")
            elif key==ord('-'): self.ear_threshold=max(0.01,self.ear_threshold-0.01); self.log_and_print_event(f"EAR Thresh: {self.ear_threshold:.2f}")
            elif key==ord('f'):
                self.fullscreen_mode = not self.fullscreen_mode
                if self.fullscreen_mode: cv2.setWindowProperty(win_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                else: cv2.setWindowProperty(win_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL); cv2.resizeWindow(win_name,self.window_width_default,self.window_height_default)
                curr_disp_w,curr_disp_h = (self.screen_width,self.screen_height) if self.fullscreen_mode else (self.window_width_default,self.window_height_default)
            elif key==ord('a'):
                self.runtime_alarm_active = not self.runtime_alarm_active
                state_msg = "ON" if self.runtime_alarm_active else "OFF"
                self.log_and_print_event(f"Runtime Sound/Event Flash Alarm Toggled: {state_msg}")
                if not self.runtime_alarm_active:
                    self.drowsiness_event_notified = False; self.yawn_event_notified = False
                    self.yawn_alert_visual_active = False
        self.video_capture.release(); cv2.destroyAllWindows(); self.log_and_print_event("Program terminated.")
        
    def draw_overlay_info(self, frame, gray_frame, detected_faces, current_timestamp):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, time_str, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        el = current_timestamp - self.start_time; h,r=divmod(el,3600); m,s=divmod(r,60)
        cv2.putText(frame, f"Elapsed: {int(h):02}:{int(m):02}:{s:05.2f}", (frame.shape[1]-220,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        y_s, l_h = 60, 30
        alarm_txt = f"Alarm ('a'): {'ON' if self.runtime_alarm_active else 'OFF'}"
        cv2.putText(frame, alarm_txt, (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255) if self.runtime_alarm_active else (100,100,100) , 1)

        if not detected_faces:
            self.drowsiness_alert_visual_active = False; self.yawn_alert_visual_active = False
            msg = "NO FACE DETECTED"; 
            if self.face_tracking and self.face_lost_frames_counter < 30: msg = "SEARCHING..."
            cv2.putText(frame, msg, (10,y_s), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            if self.face_lost_frames_counter > 30: self.eye_blink_counter = 0
            
            while self.perclos_frame_history and current_timestamp - self.perclos_frame_history[0][0] > self.perclos_window_seconds:
                self.perclos_frame_history.popleft()
            c_f = sum(1 for _,c in self.perclos_frame_history if c)
            self.perclos_value = (c_f/len(self.perclos_frame_history))*100 if self.perclos_frame_history else 0.0
            cv2.putText(frame,f"EAR: N/A",(10,y_s+l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,f"MAR: N/A",(10,y_s+2*l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,f"PERCLOS ({self.perclos_window_seconds:.0f}s): {self.perclos_value:.1f}%",(10,y_s+3*l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,f"Yawns: {self.yawn_counter}",(10,y_s+4*l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
            return
        
        face = detected_faces[0]; xf,yf,wf,hf = face.left(),face.top(),face.width(),face.height()
        cv2.rectangle(frame,(xf,yf),(xf+wf,yf+hf),(0,255,0),2)
        lndmks = self.landmark_predictor(gray_frame,face); sh_np = np.array([(lndmks.part(i).x,lndmks.part(i).y) for i in range(68)])
        le,re,mo = sh_np[self.left_eye_indices],sh_np[self.right_eye_indices],sh_np[self.mouth_indices]
        avg_e=(eye_aspect_ratio(le)+eye_aspect_ratio(re))/2.0; mar_v=mouth_ratio(mo)
        
        if self.show_landmarks: [cv2.circle(frame,(x,y),1,(0,255,0),-1) for x,y in sh_np]
        [cv2.drawContours(frame,[cv2.convexHull(p)],-1,c,1) for p,c in [(le,(0,255,0)),(re,(0,255,0)),(mo,(255,0,0))]]
        
        cv2.putText(frame,f"EAR: {avg_e:.2f}",(10,y_s+l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
        cv2.putText(frame,f"MAR: {mar_v:.2f}",(10,y_s+2*l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
        is_cl=avg_e<self.ear_threshold; self.perclos_frame_history.append((current_timestamp,is_cl))
        while self.perclos_frame_history and current_timestamp-self.perclos_frame_history[0][0]>self.perclos_window_seconds: self.perclos_frame_history.popleft()
        cl_iw=sum(1 for _,c in self.perclos_frame_history if c); self.perclos_value=(cl_iw/len(self.perclos_frame_history))*100 if self.perclos_frame_history else 0.0
        cv2.putText(frame,f"PERCLOS ({self.perclos_window_seconds:.0f}s): {self.perclos_value:.1f}%",(10,y_s+3*l_h),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
        
        alert_y_base = y_s + 4*l_h

        # --- CORRECTED DROWSINESS DETECTION LOGIC ---
        if avg_e < self.ear_threshold: # Check if eyes are closed first
            self.eye_blink_counter += 1 # Increment counter

            if self.eye_blink_counter >= self.ear_consec_frames: # THEN check if threshold is met
                self.drowsiness_alert_visual_active = True
                cv2.putText(frame, "DROWSINESS ALERT!", (10, alert_y_base + l_h), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 3)
                
                if not self.drowsiness_event_notified: 
                    if self.runtime_alarm_active:
                        self.log_and_print_event("ALERT: Drowsiness detected (EAR). Runtime alarm ON.")
                        Thread(target=play_sound_alert, daemon=True).start()
                    else:
                        self.log_and_print_event("INFO: Drowsiness detected (EAR). Runtime alarm OFF.")
                    self.drowsiness_event_notified = True
            # If eye_blink_counter is less than ear_consec_frames, but eyes are closed,
            # drowsiness_alert_visual_active remains as is (could be false, or true from a previous detection still in progress)
            # The key is that self.drowsiness_event_notified only gets set once the threshold is truly met.
        else: # Eyes are open
            self.eye_blink_counter = 0 # Reset counter
            if self.drowsiness_alert_visual_active: 
                self.drowsiness_event_notified = False # Reset notification flag for next episode
            self.drowsiness_alert_visual_active = False # Turn off visual alert

        # Yawn Detection Logic
        yawn_alert_y_offset = (2*l_h if self.drowsiness_alert_visual_active else l_h)
        
        if mar_v > self.yawn_threshold:
            self.yawn_alert_visual_active = True 
            cv2.putText(frame, "YAWN DETECTED!", (10, alert_y_base + yawn_alert_y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,165,255), 3)
            if not self.current_yawn_event: 
                self.current_yawn_event = True
                self.yawn_counter += 1
                self.log_and_print_event(f"Yawn detected (Total: {self.yawn_counter}, MAR: {mar_v:.2f})")
                
                if self.runtime_alarm_active and not self.yawn_event_notified:
                    self.log_and_print_event("ALERT: Yawn detected. Runtime alarm ON.")
                    Thread(target=play_sound_alert, daemon=True).start()
                    self.yawn_event_notified = True
        else: 
            if self.current_yawn_event: 
                self.yawn_event_notified = False 
            self.current_yawn_event = False
            self.yawn_alert_visual_active = False 

        cv2.putText(frame, f"Yawns: {self.yawn_counter}", (10, alert_y_base + yawn_alert_y_offset + l_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)


def main():
    parser = argparse.ArgumentParser(description='Drowsiness Detection System')
    parser.add_argument('--shape-predictor',type=str,default='shape_predictor_68_face_landmarks.dat')
    parser.add_argument('--ear-threshold',type=float,default=0.23)
    parser.add_argument('--ear-frames',type=int,default=25)
    parser.add_argument('--yawn-threshold',type=float,default=0.6)
    parser.add_argument('--camera',type=int,default=0) # Default camera index
    parser.add_argument('--show-landmarks',action='store_true')
    parser.add_argument('--alarm', action='store_true', help='Start with runtime sound/event flash alarm ON (toggle with A key)')
    parser.add_argument('--log',type=str,default='drowsiness_log.txt')
    parser.add_argument('--face-tracking',action='store_true',default=True)
    parser.add_argument('--perclos-window',type=float,default=60.0)
    args = parser.parse_args()
    if args.log == '': args.log = None

    print("====== Usage Instructions ======")
    print("ESC: Exit | r: Reset | + / -: Adjust EAR Thresh.")
    print("f: Fullscreen | a: Toggle Sound/Event Flash Alarm")
    print(f"Initial Runtime Alarm (from --alarm flag): {'ON' if args.alarm else 'OFF'}")
    print("==============================")
    
    try: DrowsinessDetector(args).run()
    except FileNotFoundError as e: print(f"[ERROR] File not found: {e}\nEnsure predictor is correct.")
    except ValueError as e: print(f"[ERROR] Value error: {e}")
    except Exception as e: print(f"[ERROR] Unexpected: {e}"); import traceback; traceback.print_exc()
    return 0

if __name__ == "__main__":
    main()