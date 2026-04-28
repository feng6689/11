import cv2
from color_tracker import ColorTracker
from chart_plotter import ChartPlotter
import time

def main():
    tracker = ColorTracker(camera_index=0)
    plotter = ChartPlotter()
    
    total_counts = {'red': 0, 'blue': 0, 'yellow': 0}
    frame_count = 0
    
    print("程序启动中...")
    print("操作说明：")
    print("  - 按 's' 键保存当前帧为 1.jpg")
    print("  - 按 'q' 键安全退出程序")
    
    plotter.start()
    
    try:
        while True:
            frame = tracker.get_frame()
            if frame is None:
                print("无法获取视频帧，程序退出")
                break
            
            frame = tracker.detect_colors(frame)
            counts = tracker.get_counts()
            
            plotter.update_counts(counts)
            
            total_counts['red'] += counts['red']
            total_counts['blue'] += counts['blue']
            total_counts['yellow'] += counts['yellow']
            frame_count += 1
            
            cv2.imshow('Color Tracking', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                if tracker.save_frame('1.jpg'):
                    print(f"已保存当前帧为 1.jpg (当前统计: 红={counts['red']}, 蓝={counts['blue']}, 黄={counts['yellow']})")
                else:
                    print("保存失败，没有可用的帧")
            
            elif key == ord('q'):
                print("正在退出程序...")
                break
            
    except KeyboardInterrupt:
        print("\n检测到键盘中断，正在退出...")
    
    finally:
        tracker.release()
        plotter.stop()
        cv2.destroyAllWindows()
        
        if frame_count > 0:
            avg_red = total_counts['red'] / frame_count
            avg_blue = total_counts['blue'] / frame_count
            avg_yellow = total_counts['yellow'] / frame_count
            
            print("\n" + "="*50)
            print("运行统计结果：")
            print("="*50)
            print(f"总帧数: {frame_count}")
            print(f"红色物体总数量: {total_counts['red']}, 平均数量: {avg_red:.2f}")
            print(f"蓝色物体总数量: {total_counts['blue']}, 平均数量: {avg_blue:.2f}")
            print(f"黄色物体总数量: {total_counts['yellow']}, 平均数量: {avg_yellow:.2f}")
            print("="*50)
        else:
            print("\n程序运行期间未捕获到任何帧")
        
        print("程序已安全退出")

if __name__ == "__main__":
    main()
