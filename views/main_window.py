from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QPushButton, QListWidget, QFrame, 
                                QComboBox, QCheckBox, QProgressBar, QApplication,
                                QDialog, QMessageBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from models.hero_mapper import HeroMapper
from models.secure_data import SecureDataManager
from models.image_cache import ImageCache
from views.settings_dialog import SettingsDialog
from workers.fetch_worker import FetchWorker
from views.overlay_window import OverlayWindow
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.overlay = None
        self.hero_mapper = HeroMapper()
        self.settings = QSettings("Dota2Overlay", "Settings")
        self.secure_data = SecureDataManager()
        self.image_cache = ImageCache()
        
        # Create progress bar here
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setVisible(False)
        
        self.setup_ui()
        self.apply_theme()
        
        # Pre-load hero names in a separate thread to avoid UI freeze
        self.preload_hero_names()
        
    def preload_hero_names(self):
        # Load hero names in a separate thread to avoid UI freeze
        def load_names():
            hero_names = self.hero_mapper.get_hero_names()
            self.hero_input.addItems(hero_names)
            
        threading.Thread(target=load_names, daemon=True).start()
        
    def setup_ui(self):
        self.setWindowTitle("Dota 2 Overlay")
        self.setWindowIcon(QIcon("overlayicon.ico"))
        self.setGeometry(100, 100, 450, 350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title and settings button
        title_layout = QHBoxLayout()
        
        title = QLabel("Dota 2 Overlay")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(title)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        title_layout.addWidget(self.settings_btn)
        
        layout.addLayout(title_layout)
        
        # Progress bar
        layout.addWidget(self.progress_bar)
        
        # Input section
        input_layout = QHBoxLayout()
        
        self.hero_input = QComboBox()
        self.hero_input.setEditable(True)
        self.hero_input.setPlaceholderText("Enter hero name")
        
        # Start with empty list, will be populated in background thread
        self.hero_input.addItem("Loading heroes...")
        
        input_layout.addWidget(self.hero_input)
        
        self.fetch_btn = QPushButton("Fetch Data")
        self.fetch_btn.clicked.connect(self.fetch_data)
        input_layout.addWidget(self.fetch_btn)
        
        layout.addLayout(input_layout)
        
        # Results section
        results_layout = QHBoxLayout()
        
        # Winrate
        winrate_frame = QFrame()
        winrate_frame.setFrameStyle(QFrame.Box)
        winrate_layout = QVBoxLayout()
        
        winrate_title = QLabel("Winrate")
        winrate_title.setFont(QFont("Arial", 10, QFont.Bold))
        winrate_title.setAlignment(Qt.AlignCenter)
        winrate_layout.addWidget(winrate_title)
        
        self.winrate_label = QLabel("N/A")
        self.winrate_label.setFont(QFont("Arial", 12))
        self.winrate_label.setAlignment(Qt.AlignCenter)
        self.winrate_label.setStyleSheet("color: #FFD700;")
        winrate_layout.addWidget(self.winrate_label)
        
        winrate_frame.setLayout(winrate_layout)
        results_layout.addWidget(winrate_frame)
        
        # Counters
        counters_frame = QFrame()
        counters_frame.setFrameStyle(QFrame.Box)
        counters_layout = QVBoxLayout()
        
        counters_title = QLabel("Countered by")
        counters_title.setFont(QFont("Arial", 10, QFont.Bold))
        counters_title.setAlignment(Qt.AlignCenter)
        counters_layout.addWidget(counters_title)
        
        self.counters_list = QListWidget()
        self.counters_list.setMaximumHeight(100)
        counters_layout.addWidget(self.counters_list)
        
        counters_frame.setLayout(counters_layout)
        results_layout.addWidget(counters_frame)
        
        # Countered by
        countered_frame = QFrame()
        countered_frame.setFrameStyle(QFrame.Box)
        countered_layout = QVBoxLayout()
        
        countered_title = QLabel("Counters")
        countered_title.setFont(QFont("Arial", 10, QFont.Bold))
        countered_title.setAlignment(Qt.AlignCenter)
        countered_layout.addWidget(countered_title)
        
        self.countered_list = QListWidget()
        self.countered_list.setMaximumHeight(100)
        countered_layout.addWidget(self.countered_list)
        
        countered_frame.setLayout(countered_layout)
        results_layout.addWidget(countered_frame)
        
        layout.addLayout(results_layout)
        
        # Overlay controls
        overlay_layout = QHBoxLayout()
        
        self.overlay_toggle = QCheckBox("Show Overlay")
        self.overlay_toggle.stateChanged.connect(self.toggle_overlay)
        overlay_layout.addWidget(self.overlay_toggle)
        
        overlay_layout.addStretch()
        
        self.update_overlay_btn = QPushButton("Update Overlay")
        self.update_overlay_btn.clicked.connect(self.update_overlay)
        overlay_layout.addWidget(self.update_overlay_btn)
        
        layout.addLayout(overlay_layout)
        
        central_widget.setLayout(layout)
        
    def apply_theme(self):
        theme = self.settings.value("theme", "Dark")
        
        if theme == "Dark":
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            self.setPalette(dark_palette)
        elif theme == "Light":
            self.setPalette(QApplication.style().standardPalette())
        
    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.apply_theme()
            if self.overlay:
                self.overlay.apply_theme()
                # Resize overlay if needed
                width = self.settings.value("overlay_width", 300, type=int)
                height = self.settings.value("overlay_height", 400, type=int)
                self.overlay.resize(width, height)
        
    def fetch_data(self, hero_name=None):
        if not hero_name:
            hero_name = self.hero_input.currentText().strip()
            
        if not hero_name:
            return
        
        # Show progress bar and disable UI
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.set_ui_enabled(False)
        
        # Create and start worker thread
        self.worker = FetchWorker(hero_name, self.hero_mapper, self.secure_data)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_data_fetched)
        self.worker.start()
    
    def on_data_fetched(self, hero_info, hero_image):
        # Hide progress bar and enable UI
        self.progress_bar.setVisible(False)
        self.set_ui_enabled(True)
        
        if not hero_info:
            QMessageBox.warning(self, "Error", "Failed to fetch data. Please try again.")
            return
            
        # Update main UI - use the winrate from hero_info directly
        self.winrate_label.setText(hero_info.get("Winrate", "N/A"))
        
        self.counters_list.clear()
        for counter in hero_info.get("Counter peeks", []):
            if counter:
                self.counters_list.addItem(counter)
                
        self.countered_list.clear()
        for countered in hero_info.get("Countered by", []):
            if countered:
                self.countered_list.addItem(countered)
                
        # Update overlay if it exists
        if self.overlay and self.overlay.isVisible():
            hero_name = self.hero_input.currentText().strip()
            self.overlay.update_data(
                hero_name, 
                hero_info.get("Winrate", "N/A"), 
                hero_info.get("Counter peeks", []), 
                hero_info.get("Countered by", []),
                hero_image
            )
    
    def set_ui_enabled(self, enabled):
        self.fetch_btn.setEnabled(enabled)
        self.hero_input.setEnabled(enabled)
        self.settings_btn.setEnabled(enabled)
        self.overlay_toggle.setEnabled(enabled)
        self.update_overlay_btn.setEnabled(enabled)
            
    def toggle_overlay(self, state):
        if state == Qt.Checked:
            if not self.overlay:
                self.overlay = OverlayWindow()
            self.overlay.show()
            self.update_overlay()
        else:
            if self.overlay:
                self.overlay.hide()
                
    def update_overlay(self):
        if self.overlay and self.overlay.isVisible():
            hero_name = self.hero_input.currentText().strip()
            winrate = self.winrate_label.text()
            
            counters = []
            for i in range(self.counters_list.count()):
                counters.append(self.counters_list.item(i).text())
                
            countered_by = []
            for i in range(self.countered_list.count()):
                countered_by.append(self.countered_list.item(i).text())
                
            # Get hero image from cache
            hero_image = self.image_cache.get_image(hero_name, self.hero_mapper, self.secure_data)
                
            self.overlay.update_data(hero_name, winrate, counters, countered_by, hero_image)
            
    def closeEvent(self, event):
        # Clean up any running threads
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
        
        event.accept()