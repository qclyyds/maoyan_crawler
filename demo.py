from io import BytesIO
import ddddocr
from PIL import ImageFont
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont

def font_to_img(_code, font_path):
    """
    将每个字体画成图片
    :param _code: 字体的数字码点
    :param font_path: 字体文件路径
    :return: 每个字体图片对象
    """
    img_size = 1024
    img = Image.new('1', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, int(img_size * 0.7))
    txt = chr(_code)
    bbox = draw.textbbox((0, 0), txt, font=font)
    x = bbox[2] - bbox[0]
    y = bbox[3] - bbox[1]
    draw.text(((img_size - x) // 2, (img_size - y) // 7), txt, font=font, fill=0)
    return img

def identify_word(font_path):
    font = TTFont(font_path)
    ocr = ddddocr.DdddOcr(beta=True)  # beta=True, ocr=True
    
    font_mapping = {}
    for cmap_code, glyph_name in font.getBestCmap().items():
        bytes_io = BytesIO()
        pil = font_to_img(cmap_code, font_path)
        pil.save(bytes_io, format="PNG")
        word = ocr.classification(bytes_io.getvalue())  # 识别字体
        
        # 构建字体印射规则
        font_mapping[cmap_code] = word
    
    """大陆字体印射识别为空的键值对"""
    # 根据分析，字体加密的数据中数字和符号没有加密，ddddocr对于符号识别失败的情况，因此需要去掉这部分数据
    del_key = []  # 收集要删除的键
    for key, value in font_mapping.items():
        if not value:
            del_key.append(key)
    
    # 删除识别为空的键
    for key in del_key:
        del font_mapping[key]
    
    return font_mapping
