from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
                                QTabWidget, QGroupBox, QSpinBox, QColorDialog, QFormLayout, 
                                QMessageBox, QLabel, QComboBox, QWidget)
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor
from models.secure_data import SecureDataManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(500, 500)
        
        self.settings = QSettings("Dota2Overlay", "Settings")
        self.secure_data = SecureDataManager()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # API Settings tab
        api_tab = QWidget()
        api_layout = QFormLayout()
        
        self.steam_key_edit = QLineEdit()
        self.steam_key_edit.setEchoMode(QLineEdit.Password)
        
        api_layout.addRow("Steam API Key:", self.steam_key_edit)
        
        api_tab.setLayout(api_layout)
        tabs.addTab(api_tab, "API Settings")
        
        # Appearance tab
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout()
        
        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Custom"])
        theme_layout.addWidget(self.theme_combo)
        
        self.custom_color_btn = QPushButton("Select Custom Color")
        self.custom_color_btn.clicked.connect(self.select_custom_color)
        theme_layout.addWidget(self.custom_color_btn)
        
        theme_group.setLayout(theme_layout)
        appearance_layout.addWidget(theme_group)
        
        # Opacity settings
        opacity_group = QGroupBox("Opacity")
        opacity_layout = QVBoxLayout()
        
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(10, 100)
        self.opacity_spin.setSuffix("%")
        opacity_layout.addWidget(QLabel("Overlay Opacity:"))
        opacity_layout.addWidget(self.opacity_spin)
        
        opacity_group.setLayout(opacity_layout)
        appearance_layout.addWidget(opacity_group)
        
        # Overlay size settings
        size_group = QGroupBox("Overlay Size")
        size_layout = QFormLayout()
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(200, 800)
        self.width_spin.setSuffix("px")
        self.width_spin.setValue(300)
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 1000)
        self.height_spin.setSuffix("px")
        self.height_spin.setValue(400)
        
        size_layout.addRow("Width:", self.width_spin)
        size_layout.addRow("Height:", self.height_spin)
        
        size_group.setLayout(size_layout)
        appearance_layout.addWidget(size_group)
        
        appearance_layout.addStretch()
        appearance_tab.setLayout(appearance_layout)
        tabs.addTab(appearance_tab, "Appearance")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def select_custom_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_color = color
            self.custom_color_btn.setStyleSheet(f"background-color: {color.name()};")
            
    def load_settings(self):
        # Load API keys from secure storage
        self.steam_key_edit.setText(self.secure_data.retrieve_data("steam_api_key"))
        
        # Load theme settings
        theme = self.settings.value("theme", "Dark")
        self.theme_combo.setCurrentText(theme)
        
        # Load opacity
        opacity = self.settings.value("overlay_opacity", 80, type=int)
        self.opacity_spin.setValue(opacity)
        
        # Load custom color
        custom_color = self.settings.value("custom_color", QColor(30, 30, 30))
        self.custom_color = custom_color
        self.custom_color_btn.setStyleSheet(f"background-color: {custom_color.name()};")
        
        # Load overlay size
        width = self.settings.value("overlay_width", 300, type=int)
        height = self.settings.value("overlay_height", 400, type=int)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        
    def save_settings(self):
        # Save API keys to secure storage
        self.secure_data.store_data("steam_api_key", self.steam_key_edit.text())
        
        # Save theme settings
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("overlay_opacity", self.opacity_spin.value())
        self.settings.setValue("custom_color", self.custom_color)
        
        # Save overlay size
        self.settings.setValue("overlay_width", self.width_spin.value())
        self.settings.setValue("overlay_height", self.height_spin.value())
        
        self.accept()
        QMessageBox.information(self, "Settings", "Settings saved. Restart the application for changes to take effect.")