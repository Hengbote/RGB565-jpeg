from PIL import Image, ImageDraw
import os

# 定义图像大小 输入和输出路径
w = 320    # 宽
h = 240    # 高
input_path = "E:\\python\\txt"      # 源文件路径
output_path = "E:\\python\\image"   # 输出文件路径

# 此函数将RGB565格式的颜色值转换为RGB888格式的颜色值
def convert_rgb565_to_rgb888(hex_value: int) -> tuple:
    r = (hex_value & 0xF800) >> 8
    g = (hex_value & 0x07E0) >> 3
    b = (hex_value & 0x001F) << 3
    return r, g, b

def main():
    #如果输出目录不存在，则创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #遍历输入目录中的所有文件
    for file_name in os.listdir(input_path):

        #对于每个文件，生成输入和输出文件的完整路径
        input_file = os.path.join(input_path, file_name)
        output_file = os.path.join(output_path, file_name[:-4] + ".jpeg")

        # 如果输出文件已存在，则跳过处理
        if os.path.exists(output_file):  
            print(f"跳过已存在的输出文件: {output_file}")
            continue

        #读取输入文件的内容，并去除空格
        with open(input_file, encoding="utf-8") as f:
            file_content = f.read().replace(" ", "")

        #计算输入文件的长度，并输出文件信息
        input_length = len(file_content) // 4
        print(f"定义图像大小: {w * h}, 输入文件大小: {input_length}")
        print(f"正在合成来自 {input_file} 的图像数据，合成为 {w} * {h} 的图像")

        # 将输入文件中的RGB565格式的颜色信息转换为RGB888格式
        rgb_values = [convert_rgb565_to_rgb888(int(file_content[i*4:i*4+4], 16)) for i in range(input_length)]

        #创建一个新的图像对象
        image = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        #使用RGB888编码的颜色信息填充像素
        for i, (x, y) in enumerate((x, y) for y in range(h) for x in range(w)):
            draw.point((x, y), fill=rgb_values[i] if i < input_length else (255, 255, 255))

        #保存生成的JPEG图像并显示
        image.save(output_file, 'jpeg')
        image.show()

#程序的入口点
if __name__ == "__main__":
    main()
