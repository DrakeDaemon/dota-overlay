from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QListWidget, QFrame, QComboBox, QSizePolicy)
from PyQt5.QtCore import Qt, QPoint, QSettings, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFont
import requests

class OverlayWindow(QWidget):
    # Signal to communicate with main window
    hero_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.settings = QSettings("Dota2CounterApp", "Settings")
        self.hero_mapper = parent.hero_mapper if parent else None
        self.secure_data = parent.secure_data if parent else None
        self.apply_theme()
        
        self.old_pos = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: rgba(50, 50, 50, 200); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 5, 5, 5)
        
        self.title_label = QLabel("Dota 2 Hero Counters")
        self.title_label.setStyleSheet("color: white; font-weight: bold;")
        title_layout.addWidget(self.title_label)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("color: white; font-weight: bold; background-color: transparent; border: none;")
        self.close_btn.clicked.connect(self.hide)
        title_layout.addWidget(self.close_btn)
        
        title_bar.setLayout(title_layout)
        layout.addWidget(title_bar)
        

        
        # Populate with hero names if available
        if self.hero_mapper:
            hero_names = self.hero_mapper.get_hero_names()
        

        
        # Hero info section
        hero_info_widget = QWidget()
        hero_info_layout = QHBoxLayout()
        
        # Hero image
        self.hero_image = QLabel()
        self.hero_image.setFixedSize(60, 60)
        self.hero_image.setStyleSheet("border: 2px solid #FFD700; border-radius: 5px;")
        hero_info_layout.addWidget(self.hero_image)
        
        # Hero name and winrate
        hero_text_layout = QVBoxLayout()
        self.hero_label = QLabel("Select a hero")
        self.hero_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.hero_label.setAlignment(Qt.AlignLeft)
        
        self.winrate_label = QLabel("Winrate: N/A")
        self.winrate_label.setStyleSheet("color: #FFD700; font-size: 14px;")
        self.winrate_label.setAlignment(Qt.AlignLeft)
        
        hero_text_layout.addWidget(self.hero_label)
        hero_text_layout.addWidget(self.winrate_label)
        hero_info_layout.addLayout(hero_text_layout)
        
        hero_info_widget.setLayout(hero_info_layout)
        layout.addWidget(hero_info_widget)
        
        # Counters section
        counters_frame = QFrame()
        counters_frame.setStyleSheet("background-color: rgba(40, 40, 40, 180); border-radius: 5px;")
        counters_layout = QVBoxLayout()
        
        counters_title = QLabel("Countered by")
        counters_title.setStyleSheet("color: white; font-weight: bold; margin: 5px;")
        counters_layout.addWidget(counters_title)
        
        self.counters_list = QListWidget()
        self.counters_list.setStyleSheet("""
            QListWidget {
                color: white;
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(255, 255, 255, 30);
            }
            QListWidget::item:selected {
                background-color: rgba(100, 100, 100, 150);
            }
        """)
        self.counters_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        counters_layout.addWidget(self.counters_list)
        
        counters_frame.setLayout(counters_layout)
        layout.addWidget(counters_frame)
        
        # Countered by section
        countered_frame = QFrame()
        countered_frame.setStyleSheet("background-color: rgba(40, 40, 40, 180; border-radius: 5px;")
        countered_layout = QVBoxLayout()
        
        countered_title = QLabel("Counters")
        countered_title.setStyleSheet("color: white; font-weight: bold; margin: 5px;")
        countered_layout.addWidget(countered_title)
        
        self.countered_list = QListWidget()
        self.countered_list.setStyleSheet("""
            QListWidget {
                color: white;
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(255, 255, 255, 30);
            }
            QListWidget::item:selected {
                background-color: rgba(100, 100, 100, 150);
            }
        """)
        self.countered_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        countered_layout.addWidget(self.countered_list)
        
        countered_frame.setLayout(countered_layout)
        layout.addWidget(countered_frame)
        
        self.setLayout(layout)
        
        # Set initial size from settings
        width = self.settings.value("overlay_width", 300, type=int)
        height = self.settings.value("overlay_height", 400, type=int)
        self.resize(width, height)
        
        
    def apply_theme(self):
        theme = self.settings.value("theme", "Dark")
        opacity = self.settings.value("overlay_opacity", 80, type=int) / 100.0
        
        if theme == "Dark":
            self.setStyleSheet(f"background-color: rgba(30, 30, 30, {opacity*255}); border-radius: 10px;")
        elif theme == "Light":
            self.setStyleSheet(f"background-color: rgba(240, 240, 240, {opacity*255}); border-radius: 10px;")
        else:
            custom_color = self.settings.value("custom_color", QColor(30, 30, 30))
            self.setStyleSheet(f"background-color: rgba({custom_color.red()}, {custom_color.green()}, {custom_color.blue()}, {opacity*255}); border-radius: 10px;")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
            
    def update_data(self, hero_name, winrate, counters, countered_by, hero_image=None):
        self.hero_label.setText(hero_name.capitalize())
        self.winrate_label.setText(f"Winrate: {winrate}")
        
        # Set hero image if available
        if hero_image:
            pixmap = QPixmap()
            pixmap.loadFromData(hero_image)
            self.hero_image.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.hero_image.clear()
        
        self.counters_list.clear()
        for counter in counters:
            if counter:
                self.counters_list.addItem(counter)
                
        self.countered_list.clear()
        for countered in countered_by:
            if countered:
                self.countered_list.addItem(countered)