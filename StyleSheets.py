"""
This file is intended to consolidate all the CSS StyleSheets being used in Alchemical Finances. This will allow for
re-use and also ease of reading. Ass this adds unnecessary bulk to the core python code.
"""


# --- Universal --------------------------------------------------------------------------------------------------------
UniversalStyleSheet = """
QMainWindow{
    background-color: #f5fbef;
    font: 14px;
}

QDialog{
    background-color: #f5fbef;
}

QLabel#label{
    font-size: 10px;
}

QLineEdit{
    border: 1px solid #748b75;
    border-radius: 2px;
    font-size: 10px;
}

QLineEdit:Disabled{
    border: 1px solid #748b75;
    background-color: rgba(211, 211, 211, 0.4);
    border-radius: 2px;
    font-size: 10px;
}

QLineEdit#lineEditReceiptL1{
    background: rgba(211, 211, 211, 0.4);
    font-size: 10px;
}

QListWidget{
    border: 1px solid #748b75;
    border-radius: 2px;
    font-size: 10px;
}

QTextEdit{
    border: 1px solid #748b75;
    border-radius: 2px;
    font-size: 10px;
}

QPushButton{
    border: 1px solid #748b75;
    background-color: #D3D3D3;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
    padding: 2px;
    padding-right: 5px;
    padding-left: 5px;
}

QPushButton:pressed{
    border: 2px solid #748b75;
    background-color: #9acd32;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
    padding: 2px;
    padding-right: 5px;
    padding-left: 5px;
}

QPushButton:hover{
    border: 2px solid #748b75;
    background-color: #9acd32;
    font-size: 8px;
    font-weight: bold;
    padding: 2px;
    padding-right: 5px;
    padding-left: 5px;
}

QPushButton:disabled{
    border: 1px solid #748b75;
    background-color: #ADADAD;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
    padding: 2px;
    padding-right: 5px;
    padding-left: 5px;
}

QComboBox{
    background-color: #748b75;
    color: white;
    font-size: 10px;
}

QComboBox:hover{
    background-color: #9acd32;
    font-size: 10px;
}

QComboBox:disabled{
    background-color: #ADADAD;
    color: #D7D7D7;
    font-size: 10px;
}

QComboBox QAbstractItemView{
    border: 1px solid #748b75;
    selection-background-color: #D3D3D3;
    selection-color: black;
    font-size: 10px;
}

QComboBox:selection{
    background: white;
    font-size: 10px;
}

QDateEdit{
    border: 1px solid #748b75;
    background-color: #748b75;
    color: white;
    font-size: 10px;
}

QDateEdit:hover{
    background-color: #9acd32;
    font-size: 10px;
}

QDateEdit QAbstractItemView{
    border: 1px solid #748b75;
    selection-background-color: #D3D3D3;
    selection-color: black;
    font-size: 10px;
}

QInputDialog{
    background-color: #f5fbef;
}

QSpinBox{
   height: 25px;
}

QSpinBox::QAbstractItemVIew {
    font-size: 10px;
}

QScrollBar:vertical {
    border: 1px solid #748b75;
    background: #D3D3D3;
    width: 15px;
    margin: 22px 0 20px 0;
}
QScrollBar::handle:vertical {
    background: #748b75;
    min-height: 20px;
}
QScrollBar::add-line:vertical {
    border: 1.5px solid #748b75;
    background: #f5fbef;
    height: 20px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: 1.5px solid #748b75;
    background: #f5fbef;
    height: 20px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    border: 1px dashed #748b75;
    width: 5px;
    height: 5px;
    background: #92ad94;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #748b75;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 2px solid #748b75;
    border-bottom-color: #f5fbef; /* same as the pane color */
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
    min-width: 8px;
    padding: 2px;
    font-size: 10px;
    color: #748b75;
    font-weight: bold;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
}

QTabBar::tab:selected {
    border-color: #748b75;
    border-bottom-color: #f5fbef; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */
}
"""

uFrameStyleSheet = """
QFrame{
    border: 1px dashed #9acd32;
    border-top: 3px solid #9acd32;
    border-bottom: 3px solid #9acd32;
    border-radius: 5px;
    background-color: #92ad94;
}
"""

uTitleStyleSheet = """
QLabel{
    font-size: 12px;
    font-weight: bold;
}
"""

# --- UserLogin --------------------------------------------------------------------------------------------------------

loginStyleSheet = """
QDialog{
    background-color: #f5fbef;
}

QLineEdit{
    border: 1px solid #748b75;
    border-radius: 2px;
    font-size: 10px;
}

QPushButton{
    border: 1px solid #748b75;
    background-color: #D3D3D3;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
}

QPushButton:pressed{
    border: 2px solid #748b75;
    background-color: #9acd32;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
}

QPushButton:hover{
    border: 2px solid #748b75;
    background-color: #9acd32;
    border-radius: 2px;
    font-size: 8px;
    font-weight: bold;
}

QFrame{
    border: 1px solid #D3D3D3;
    border-top: 3px solid #9acd32;
    border-bottom: 3px solid #9acd32;
    border-radius: 5px;
    background-color: #92ad94;
}

QLabel{
    border: none;
    background-color: none;
    font-weight: bold;
    font-size: 10px;
}
"""

titleStyleSheet = """
QLabel{
    font-size: 18px;
}
"""

subtitleStyleSheet = """
QLabel{
    font-size: 10px;
    font-style: italic;
}
"""

# --- WelcomeMessage ---------------------------------------------------------------------------------------------------
welcomeStylesheet = """
QFrame{
    border: 2px solid #748b75;
    border-right: 2px dashed #748b75;
    border-left: 2px dashed #748b75;
    background-color: rgba(211, 211, 211, 0.4);
    
}

QLabel{
    border: none;
    background-color: none;
}
"""

# --- Summary ----------------------------------------------------------------------------------------------------------
messagesheet = """
QLabel{
    background-color: #9ACD32;
    border: 1px solid #748B75;
    border-left: 3px solid #FF6347;
    border-right: 3px solid #FF6347;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
}
"""

innerframesheet = """
QFrame{
    border: 0px solid #D3D3D3;
}
"""

progressSheet = """
QWidget{
    background-color: #f5fbef;
    border: none;
}


QProgressBar{
    border: 2px solid gray;
    border-radius: 5px;
    height: 5px;
    text-align: center;
    color: black;
    font-size: 10px;
    font-weight: bold;

}

QProgressBar::chunk {
    background-color: #9ACD32;
    border-radius: 2px;
    width: 2 px;
    margin: 1px;
}
"""

parentypeSheet = """
QLabel{
    background-color: #92AD94;
    border: 1px solid #9ACD32;
    border-radius: 5px;
    border-left: 3px solid #9ACD32;
    border-right: 3px solid #9ACD32;
    height: 40px;
}
"""

colheadersheet = """
QLabel{
    background-color: #D3D3D3;
    border: 1px solid #9ACD32;
    border-left: 3px solid #9ACD32;
    border-right: 3px solid #9ACD32;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
"""

subtotalsheet = """
QLabel{
    background-color: #9ACD32;
    border: 1px solid black;
    border-left: 3px solid black;
    border-right: 3px solid black;
    border-radius: 4px;
    font-weight: bold;
}
"""

accountsheet = """
QLabel{
    border: 0px solid #92AD94;
    border-top: 2px dashed #748b75;
}
"""

# --- About ------------------------------------------------------------------------------------------------------------
aboutFrame = """
QFrame{
    background-color: #D3D3D3;
    border: 2px solid #748b75;
    border-right: 2px solid #92ad94;
    border-bottom: 2px solid #92ad94;    
}

QLabel{
    border: none;
}
"""

# --- Error ------------------------------------------------------------------------------------------------------------
generalError = """
QLineEdit{
    border: 2px solid #D35858;
    border-radius: 2px;
}

QLabel{
    color: #D35858;
}
"""