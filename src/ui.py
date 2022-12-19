import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class GameUI(QWidget):
    def __init__(self):
        super().__init__()

        # 创建按钮
        self.status_button = QPushButton("状态")
        self.items_button = QPushButton("物品")
        self.equipment_button = QPushButton("装备")
        self.skills_button = QPushButton("技能")
        self.magic_button = QPushButton("魔法")
        self.settings_button = QPushButton("设置")

        # 创建水平布局，将按钮添加到布局中
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.status_button)
        h_layout.addWidget(self.items_button)
        h_layout.addWidget(self.equipment_button)
        h_layout.addWidget(self.skills_button)
        h_layout.addWidget(self.magic_button)

        # 创建垂直布局，将水平布局和设置按钮添加到布局中
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.settings_button, alignment=Qt.AlignRight)

        # 设置窗口布局
        self.setLayout(v_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GameUI()
    ui.show()
    sys.exit(app.exec_())