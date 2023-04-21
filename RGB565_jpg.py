from PIL import Image, ImageDraw
import os

# 定义图像大小
w = 320     # 宽
h = 240     # 高

input_path = os.getcwd() + "\\2.txt"  # 源文件路径
output_path = os.getcwd() + "\\out.jpeg"  # 输出文件名称

# 此函数将RGB565格式的颜色值转换为RGB888格式的颜色值
def convert_rgb565_to_rgb888(hex_value: int) -> tuple:
    r = (hex_value & 0xF800) >> 8
    g = (hex_value & 0x07E0) >> 3
    b = (hex_value & 0x001F) << 3
    return r, g, b

#读取输入文件的内容，并去除空格
with open(input_path, encoding="utf-8") as f:
    file_content = f.read().replace(" ", "")

#计算输入文件的长度，并输出文件信息
input_length = (len(file_content) // 4)  # 输入文件大小
print(f"定义图像大小: {w * h}, 输入文件大小: {input_length}")
print(f"正在合成来自 {input_path} 的图像数据，合成为 {w} * {h} 的图像")

# 将输入文件中的RGB565格式的颜色信息转换为RGB888格式
rgb_values = [convert_rgb565_to_rgb888(int(file_content[i*4:i*4+4], 16)) for i in range(input_length)]

#创建一个新的图像对象
image = Image.new('RGB', (w, h), (255, 255, 255))  
draw = ImageDraw.Draw(image)  

# 使用RGB888编码的颜色信息填充像素
for i, (x, y) in enumerate((x, y) for y in range(h) for x in range(w)):
    draw.point((x, y), fill=rgb_values[i] if i < input_length else (255, 255, 255))

#保存生成的JPEG图像并显示
image.save(output_path, 'jpeg')
image.show()
