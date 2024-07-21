
#   Copyright (C) 2024 by Bruno Cardoso <contato@brunocardosofm.com.br>

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon

current_path = sys.argv[0].replace("main.py", "")

import resources.resources
from styles.globalstyle import globalStyle

class Leftmenu(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__()
        self.setFixedWidth(220)

        self.setObjectName("leftMenu")

        policy = self.sizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(policy)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.btnProg = QtWidgets.QPushButton("Programação", self)
        self.btnComercial = QtWidgets.QPushButton("Comercial", self)
        self.btnFinance = QtWidgets.QPushButton("Financeiro", self)
        self.btnCatalog = QtWidgets.QPushButton("Catálogo", self)
        self.btnReports = QtWidgets.QPushButton("Relatórios", self)
        self.btnSettings = QtWidgets.QPushButton("Configurações", self)
        self.btnUsers = QtWidgets.QPushButton("Usuários", self)

        self.btnAbout = QtWidgets.QPushButton("Sobre", self)

        self.bottomSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout.addWidget(self.btnCatalog)
        self.layout.addWidget(self.btnProg)
        self.layout.addWidget(self.btnComercial)
        self.layout.addWidget(self.btnFinance)
        self.layout.addWidget(self.btnReports)

        self.layout.addItem(self.bottomSpacer)
        
        self.layout.addWidget(self.btnUsers)
        self.layout.addWidget(self.btnSettings)
        self.layout.addWidget(self.btnAbout)


# Criando a janela principal
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, isDarkMode: type=bool):
        super().__init__()
        
        # Definindo os parametros da janela
        self.setWindowTitle("NaxiStudio Control")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setWindowIcon(QIcon(":/images/icons/icon.ico"))

        # Criando o Widget principal da janela
        self.container = QtWidgets.QWidget(self)
        self.container.setObjectName("centralwidget")
        self.container.setStyleSheet(globalStyle)

        # Criando o layout do widget principal
        self.layout = QtWidgets.QHBoxLayout(self.container)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.leftMenu = Leftmenu(self)

        self.content = QtWidgets.QGroupBox(self)
        self.content.setObjectName("content")
        self.content.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.contentLayout = QtWidgets.QHBoxLayout(self.content)

        self.layout.addWidget(self.leftMenu)
        self.layout.addWidget(self.content)

        # Adicionando container como widget principal
        self.setCentralWidget(self.container)

        # Chamadas das funções

    @QtCore.Slot()
    # Verificar se a janela principal foi fechada e encerrar o programa
    def closeEvent(self, event):
        sys.exit(app.exec())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

    # Obtém a cor da janela
    colorWindow = app.palette().color(QtGui.QPalette.Window)

    # Verifica o modo de aparência com base na luminosidade da cor da janela
    isDarkMode = False if colorWindow.lightnessF() > 0.5 else True

    # Instanciando a janela principal
    window = MainWindow(isDarkMode)

    # Definindo o tamanho inicial da janela
    window.resize(800, 500)
    # Mostrando a janela principal
    window.show()

    sys.exit(app.exec())