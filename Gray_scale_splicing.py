import os
from PIL import Image, ImageDraw

input_path = "E:\\python\\txt"      # 输入文件路径
output_path = "E:\\python\\image"   # 输出文件路径
save_format = "png"                 # 输出文件格式

width_per_image = 11
height_per_image = 18
images_per_row = 86
images_per_column = 78

def process_single_file(file_name, width_per_image, height_per_image, images_per_row, images_per_column):
    # 构建输入文件和输出文件的完整路径
    input_file = os.path.join(input_path, file_name)
    file_name_without_extension = file_name.rsplit('.', 1)[0]
    output_file_name = f"{file_name_without_extension}.{save_format}"
    output_file = os.path.join(output_path, output_file_name)

    # 如果输出文件已存在，跳过处理
    if os.path.exists(output_file):
        return

    # 创建一个空白的大图像，用于存放小图像
    big_image = Image.new('RGB', (width_per_image * images_per_row, height_per_image * images_per_column), (255, 255, 255))

    counter_x = 0
    counter_y = 0

    # 读取输入文件内容并去除空格
    with open(input_file, encoding="utf-8") as f:
        file_content = f.read().replace(" ", "")

    input_length = len(file_content) // 2
    total_images = input_length // (width_per_image * height_per_image)

    # 遍历文件内容，创建和处理小图像
    for img_index in range(total_images):
        # 获取RGB值列表
        rgb_values = [int(file_content[i*2+img_index*2*width_per_image*height_per_image:i*2+2+img_index*2*width_per_image*height_per_image], 16) for i in range(width_per_image * height_per_image)]
        rgb_values = [(v, v, v) if i < len(rgb_values) else (0, 0, 0) for i, v in enumerate(rgb_values)]

        # 创建一个新的小图像并绘制像素点
        image = Image.new('RGB', (width_per_image, height_per_image), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 使用RGB编码的颜色信息填充像素
        for y in range(height_per_image):
            for x in range(width_per_image):
                i = y * width_per_image + x
                draw.point((x, y), fill=rgb_values[i])

        # 将当前小图像粘贴到大图像上
        big_image.paste(image, (width_per_image * counter_x, height_per_image * counter_y))

        # 更新计数器
        counter_x += 1
        if counter_x == images_per_row:
            counter_x = 0
            counter_y += 1

    # 保存生成的大图像并显示
    big_image.save(output_file, save_format)
    big_image.show()

def main():
    # 如果输出目录不存在，则创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 遍历输入目录的所有文件并处理
    for file_name in os.listdir(input_path):
        process_single_file(file_name, width_per_image, height_per_image, images_per_row, images_per_column)

    print("结束")

if __name__ == "__main__":
    main()
