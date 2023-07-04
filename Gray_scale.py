from PIL import Image, ImageDraw
import os

input_path = "E:\\python\\Image\\txt"       # 源文件路径
output_path = "E:\\python\\Image\\image"    # 输出文件路径
save_format = "png"                         # 输出文件格式

#自动根据输入文件大小设置图像大小
def find_best_size(input_length: int) -> tuple:
    # 预定义的图像大小列表
    sizes = [
        (9,   18),
        (11,  18),
        (12,  20),
        (48,  48),
        (20,  20),
        (48,  48),
        (96,  96),
        (160, 120),
        (176, 144),
        (240, 176),
        (240, 240),
        (320, 240),
        (400, 296),
        (480, 320),
        (640, 480)
    ]

    # 初始化最小差值和最佳大小
    min_diff = float('inf')
    best_size = (0, 0)

    # 遍历预定义的大小列表，找到与输入长度最接近的大小
    for size in sizes:
        w, h = size
        diff = abs(input_length - w * h)
        
        # 如果当前差值小于最小差值，则更新最小差值和最佳大小
        if diff < min_diff:
            min_diff = diff
            best_size = size

    # 返回找到的最佳大小
    return best_size

# 此函数将8bit灰度值转换为RGB888格式的颜色值
def convert_gray8_to_rgb888(gray_value: int) -> tuple:
    return gray_value, gray_value, gray_value

def main():
    #如果输出目录不存在，则创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #遍历输入目录中的所有文件
    for file_name in os.listdir(input_path):

        #对于每个文件，生成输入和输出文件的完整路径
        input_file = os.path.join(input_path, file_name)
        output_file = os.path.join(output_path, file_name[:-4] + "." + save_format)

        # 获取输出目录中的所有文件名（不包括扩展名）
        output_files_without_ext = {os.path.splitext(f)[0] for f in os.listdir(output_path)}

        # 如果输出文件已存在（不考虑扩展名），则跳过处理
        input_file_name_without_ext = os.path.splitext(file_name)[0]
        if input_file_name_without_ext in output_files_without_ext:
            #print(f"已跳过存在的图像文件的输入文件: {input_file}")
            continue

        ## 如果输出文件已存在，则跳过处理
        #if os.path.exists(output_file):  
        #    print(f"跳过已存在的输出文件: {output_file}")
        #    continue

        #读取输入文件的内容，并去除空格
        with open(input_file, encoding="utf-8") as f:
            file_content = f.read().replace(" ", "")

        #计算输入文件的长度，并输出文件信息
        input_length = len(file_content) // 2
        w, h = find_best_size(input_length)
        #w = 120
        #h = 120
        print(f"定义图像大小: {w * h}, 输入文件大小: {input_length}")
        print(f"正在合成来自 {input_file} 的图像数据，合成为 {w} * {h} 的图像")

        # 将输入文件中的8bit灰度值颜色信息转换为RGB888格式
        rgb_values = [convert_gray8_to_rgb888(int(file_content[i*2:i*2+2], 16)) for i in range(input_length)]
        
        #创建一个新的图像对象
        image = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        #使用RGB888编码的颜色信息填充像素
        for i, (x, y) in enumerate((x, y) for y in range(h) for x in range(w)):
            draw.point((x, y), fill=rgb_values[i] if i < input_length else (255, 255, 255))

        #保存生成的JPEG图像并显示
        image.save(output_file, save_format)
        image.show()

#程序的入口点
if __name__ == "__main__":
    main()
