from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QColorDialog, QSlider, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QPixmap, QScreen
from PyQt5.QtCore import Qt, QPoint, QTimer, QDateTime
import sys


class Overlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_drawing = False
        self.is_laser_active = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.pen_width = 3

        # Lazer kalem için ek özellikler
        self.laser_path = []  # Her nokta için (position, timestamp) listesi, None ile yolları ayırır
        self.laser_color = Qt.red
        self.laser_timer = QTimer(self)
        self.laser_timer.timeout.connect(self.clear_old_laser_points)
        self.laser_timer.start(100)  # Zamanlayıcıyı periyodik olarak çalıştır (ör. 100 ms)

    def mousePressEvent(self, event):
        if self.is_laser_active:
            if event.button() == Qt.LeftButton:
                # Lazer modunda yeni bir yol başlat
                self.laser_path.append(None)  # Önceki yolu ayır
                self.laser_path.append((event.pos(), QDateTime.currentMSecsSinceEpoch()))
                self.update()
            return  # Lazer modunda diğer işlemleri yapma

        if self.is_drawing and event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_laser_active:
            # Lazer modu etkinse, lazer davranışını uygula
            self.laser_path.append((event.pos(), QDateTime.currentMSecsSinceEpoch()))
            self.update()
            return  # Lazer modunda diğer işlemleri yapma

        # Çizim modu kontrolü
        if self.is_drawing and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.parent().label.pixmap())
            pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            self.last_point = event.pos()
            self.parent().update()

    def mouseReleaseEvent(self, event):
        if self.is_laser_active:
            if event.button() == Qt.LeftButton:
                # Lazer modunda tıklama bitince yolu ayır
                self.laser_path.append(None)
            return  # Lazer modunda fare bırakıldığında başka işlem yapma

        if self.is_drawing and event.button() == Qt.LeftButton:
            self.last_point = QPoint()

    def paintEvent(self, event):
        if self.is_laser_active:
            painter = QPainter(self)

            # Dış (kırmızı parlak) çizgi
            outer_pen = QPen(Qt.red, 6, Qt.SolidLine)  # Kırmızı ve daha kalın bir çizgi
            painter.setPen(outer_pen)

            # Yolları çizerken None ile bölümleri ayır
            previous_point = None
            for point in self.laser_path:
                if point is None:
                    previous_point = None  # Yeni bir yol başlat
                elif previous_point is not None:
                    painter.drawLine(previous_point[0], point[0])
                previous_point = point

            # İç (beyaz) çizgi
            inner_pen = QPen(Qt.white, 2, Qt.SolidLine)  # Beyaz ve daha ince bir çizgi
            painter.setPen(inner_pen)

            previous_point = None
            for point in self.laser_path:
                if point is None:
                    previous_point = None  # Yeni bir yol başlat
                elif previous_point is not None:
                    painter.drawLine(previous_point[0], point[0])
                previous_point = point

    def clear_old_laser_points(self):
        """Lazer kalem yolundaki eski noktaları temizler."""
        current_time = QDateTime.currentMSecsSinceEpoch()
        new_laser_path = []
        for point in self.laser_path:
            if point is None or current_time - point[1] <= 2000:  # 2 saniyeden eski olmayan noktaları tut
                new_laser_path.append(point)
        self.laser_path = new_laser_path
        self.update()

    def set_drawing_mode(self, drawing):
        self.is_drawing = drawing

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width

    def toggle_laser(self, active):
        """Lazer kalem modunu aç/kapat."""
        self.is_laser_active = active
        if not active:
            self.laser_path.clear()
            self.update()


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Çizim Uygulaması")

        # Ekran boyutlarını dinamik olarak ayarla
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)  # Uygulamayı modal yap

        self.setAttribute(Qt.WA_TranslucentBackground)

        # Çizim alanı için QLabel
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.label.setPixmap(QPixmap(screen_geometry.width(), screen_geometry.height()))
        self.label.pixmap().fill(Qt.transparent)

        # Overlay widget
        self.overlay = Overlay(self)
        self.overlay.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.setStyleSheet("background: transparent;")

        # Araç çubuğu için bir widget
        self.toolbar = QWidget(self)
        self.toolbar.setGeometry(10, 10, 200, 200)
        self.toolbar.setStyleSheet("background-color: white; border: 1px solid black;")
        layout = QVBoxLayout(self.toolbar)

        # Renk değiştirme butonu
        self.color_button = QPushButton("Renk Seç", self.toolbar)
        self.color_button.clicked.connect(self.select_color)
        layout.addWidget(self.color_button)

        # Fırça boyutu ayarlama slider'ı
        self.brush_size_slider = QSlider(Qt.Horizontal, self.toolbar)
        self.brush_size_slider.setRange(1, 20)
        self.brush_size_slider.setValue(self.overlay.pen_width)
        self.brush_size_slider.valueChanged.connect(self.change_brush_size)
        layout.addWidget(self.brush_size_slider)

        # Çizim modunu aç/kapat butonu
        self.draw_mode_button = QPushButton("Çizim Modu: Kapalı", self.toolbar)
        self.draw_mode_button.clicked.connect(self.toggle_draw_mode)
        layout.addWidget(self.draw_mode_button)

        # Lazer kalem aç/kapat butonu
        self.laser_button = QPushButton("Lazer Kalem: Kapalı", self.toolbar)
        self.laser_button.clicked.connect(self.toggle_laser)
        layout.addWidget(self.laser_button)

        # Kaydetme butonu
        self.save_button = QPushButton("Kaydet", self.toolbar)
        self.save_button.clicked.connect(self.save_drawing)
        layout.addWidget(self.save_button)

        # Sağ üst köşeye kapatma butonu
        self.close_button = QPushButton("X", self)
        self.close_button.setGeometry(screen_geometry.width() - 50, 10, 40, 40)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("background-color: red; color: white; font-weight: bold; border: none;")

        # Fare tekerleği hareketi kontrolü için zamanlayıcı
        self.wheel_timer = QTimer(self)
        self.wheel_timer.timeout.connect(self.restart_drawing_mode)

    def keyPressEvent(self, event):
        """Klavye tuşlarını kontrol eder."""
        if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            # CTRL + A: Çizim modunu aç/kapat
            self.toggle_draw_mode()
        elif event.key() == Qt.Key_L and event.modifiers() == Qt.ControlModifier:
            # CTRL + L: Lazer modunu aç/kapat
            self.toggle_laser()

    def wheelEvent(self, event):
        """Fare tekerleği çevrildiğinde çizim modunu kapat."""
        if self.overlay.is_drawing:
            self.toggle_draw_mode()  # Çizim modunu kapat
            self.wheel_timer.start(1000)  # 1 saniyelik bir zamanlayıcı başlat

    def restart_drawing_mode(self):
        """Fare tekerleği hareketi durduğunda çizim modunu yeniden başlat."""
        self.wheel_timer.stop()
        if not self.overlay.is_drawing:
            self.toggle_draw_mode()  # Çizim modunu yeniden aç

    def capture_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            screenshot = screen.grabWindow(0)  # Tüm ekranın görüntüsünü al
            self.label.setPixmap(screenshot)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.overlay.set_pen_color(color)

    def change_brush_size(self, size):
        self.overlay.set_pen_width(size)

    def toggle_draw_mode(self):
        self.overlay.set_drawing_mode(not self.overlay.is_drawing)
        if self.overlay.is_drawing:
            self.draw_mode_button.setText("Çizim Modu: Açık")
            self.setCursor(Qt.CrossCursor)  # Çizim modunda özel bir işaretçi ayarla
            self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)

            # Çizim modunu açarken ekran görüntüsü al
            self.capture_screen()
        else:
            self.draw_mode_button.setText("Çizim Modu: Kapalı")
            self.setCursor(Qt.ArrowCursor)  # Varsayılan işaretçiye geri dön
            self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)

            # Çizimi temizle ancak uygulamayı kapatma
            self.label.pixmap().fill(Qt.transparent)
            self.update()  # Ekranı güncelle

    def toggle_laser(self):
        is_active = not self.overlay.is_laser_active
        self.overlay.toggle_laser(is_active)
        if is_active:
            self.laser_button.setText("Lazer Kalem: Açık")
        else:
            self.laser_button.setText("Lazer Kalem: Kapalı")

    def save_drawing(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Çizimi Kaydet", "", "PNG Dosyaları (*.png);;Tüm Dosyalar (*)")
        if file_path:
            if not file_path.endswith(".png"):
                file_path += ".png"
            if not self.label.pixmap().save(file_path):
                QMessageBox.critical(self, "Hata", "Çizim kaydedilemedi!")
            else:
                QMessageBox.information(self, "Başarılı", "Çizim başarıyla kaydedildi!")


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)  # Yüksek DPI desteğini etkinleştir
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()