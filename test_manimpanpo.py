import manimpango
import tempfile

# 文本内容
text = "Hello, World!"

# 调用 manimpango 的 text2svg 函数，使用关键字参数
class _Alignment:
    VAL_DICT = {
        "LEFT": 0,
        "CENTER": 1,
        "RIGHT": 2
    }

    def __init__(self, s: str):
        self.value = _Alignment.VAL_DICT[s.upper()]
with tempfile.NamedTemporaryFile(suffix='.svg',mode='w+',delete=False) as tmp:
    svg_content = manimpango.MarkupUtils.text2svg(
        text=text,                       # 文本内容
        font="",                         # 字体路径，可以指定系统字体路径或留空
        slant="NORMAL",                  # 文本斜体风格
        weight="NORMAL",                 # 文本粗细风格
        size=1,
        _=0,                          # 字体大小
        disable_liga=False,              # 禁用 ligature（字体连字）
        file_name=tmp.name,
        START_X=0,                       # 起始 x 坐标
        START_Y=0,                       # 起始 y 坐标
        width=200,                       # SVG 宽度
        height=100,                      # SVG 高度
        justify=False,                  # 文本对齐方式
        indent=0,                        # 首行缩进
        line_spacing=None,               # 行间距
        alignment=_Alignment("CENTER"),              # 文本对齐方式
        pango_width=None                 # Pango 宽度
    )
    tmp.write(svg_content)
    tmp.seek(0)
    print(f"Temporary SVG file created at: {tmp.name}")

# 打印输出（可以用适当的路径保存到文件）
# print(svg_content)

