import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from queue import Queue, Empty

class ChartPlotter:
    def __init__(self):
        self.queue = Queue(maxsize=10)
        self.running = False
        self.thread = None
        
        self.counts = {'red': 0, 'blue': 0, 'yellow': 0}
        self.colors = ['red', 'blue', 'yellow']
        self.color_names = ['红色', '蓝色', '黄色']
        self.color_values = ['#FF0000', '#0000FF', '#FFFF00']
        
        self.fig = None
        self.ax = None
        self.bars = None
        self.anim = None

    def update_counts(self, counts):
        try:
            self.queue.put_nowait(counts)
        except:
            pass

    def _init_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_facecolor('#f0f0f0')
        self.fig.patch.set_facecolor('#f0f0f0')
        
        self.ax.set_title('颜色物体数量实时统计', fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xlabel('颜色', fontsize=12, fontweight='semibold')
        self.ax.set_ylabel('数量', fontsize=12, fontweight='semibold')
        
        initial_counts = [0, 0, 0]
        self.bars = self.ax.bar(self.color_names, initial_counts, color=self.color_values, edgecolor='black', linewidth=1.5)
        
        self.ax.set_ylim(0, max(1, max(initial_counts) + 2))
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                         f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.tight_layout()

    def _animate(self, frame):
        try:
            while True:
                counts = self.queue.get_nowait()
                self.counts = counts
        except Empty:
            pass
        
        current_counts = [self.counts['red'], self.counts['blue'], self.counts['yellow']]
        
        for bar, count in zip(self.bars, current_counts):
            bar.set_height(count)
        
        max_count = max(current_counts)
        self.ax.set_ylim(0, max(1, max_count + 2))
        
        for text in self.ax.texts:
            text.remove()
        
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                         f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        return self.bars,

    def _run(self):
        self._init_plot()
        self.anim = FuncAnimation(self.fig, self._animate, interval=100, blit=False, cache_frame_data=False)
        plt.show(block=False)
        
        while self.running:
            plt.pause(0.05)
        
        plt.close(self.fig)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
