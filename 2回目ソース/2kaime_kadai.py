import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image

# CGHシミュレーション関数
def simulate_cgh(width, height, focal_length, wave_length, pixel_pitch):
    
    xlist = np.array([[i for i in range(width)] for j in range(height)], dtype=int)
    ylist = np.array([[j for i in range(width)] for j in range(height)], dtype=int)

    r = np.sqrt((height/2 - ylist) ** 2 + (width/2 - xlist) ** 2)

    r_SLM = r * pixel_pitch

    # Masking (Max calculation region)
    maxR = (wave_length * focal_length) / (2 * pixel_pitch)
    r_SLM[r_SLM > maxR] = 255

    # Calculating of Phase Fresnel lens
    l_phase = -1 * (np.pi * (r_SLM ** 2) / (focal_length * wave_length))
    l_phase = np.fmod(l_phase, 2 * np.pi)

    return l_phase


# CGHをBMP画像として保存する関数
def save_cgh_as_bmp(cgh_data, filename='cgh_image.bmp'):
    # CGHデータを画像として保存
    #Image.fromarray()を使えば、加工した配列から画像を生成することができる
    image = Image.fromarray(np.uint8(cgh_data / (2 * np.pi) * 255), 'L') 
     # データを0-255のグレースケールに変換
    image.save(filename)

# GUIアプリケーション
class CGHApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CGH Generator')

        # パラメータ入力用のフィールド
        self.create_input_fields()

        # 生成ボタンの設定
        self.generate_button = tk.Button(self, text='Generate and Save', command=self.generate_cgh)
        self.generate_button.pack()

    def create_input_fields(self):
        # パラメータ入力用のラベルとエントリーを作成
        self.width_entry = self.create_entry('Width:', '512')
        self.height_entry = self.create_entry('Height:', '512')
        self.focal_length_entry = self.create_entry('Focal Length (mm):', '1000')
        self.wave_length_entry = self.create_entry('Wavelength (nm):', '633')
        self.pixel_pitch_entry = self.create_entry('Pixel Pitch (um):', '20')

    def create_entry(self, label, default):
        frame = tk.Frame()
        frame.pack()
        tk.Label(frame, text=label).pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default)
        return entry

    def generate_cgh(self):
        # ユーザーからの入力を取得
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        focal_length = float(self.focal_length_entry.get())
        wave_length = float(self.wave_length_entry.get()) * 10**-6  # nm to mm conversion
        pixel_pitch = float(self.pixel_pitch_entry.get()) * 10**-3  # um to mm conversion

        # CGHシミュレーションの実行
        cgh_data = simulate_cgh(width, height, focal_length, wave_length, pixel_pitch)

        # ユーザーが保存するファイル名を選択
        filename = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("Bitmap Image", "*.bmp")])
        if not filename:  # ユーザーがキャンセルした場合は何もしない
            return

        # CGHをBMP画像として保存
        save_cgh_as_bmp(cgh_data, filename)

        # 完了メッセージ
        messagebox.showinfo("Success", f"CGH has been saved as BMP: {filename}")

if __name__ == '__main__':
    app = CGHApp()
    app.mainloop()


