## poem變項內容擷取自鄭愁予《錯誤》

poem = """
東風不來，三月的柳絮不飛
你的心如小小寂寞的城
恰若青石的街道向晚
跫音不響，三月的春帷不揭
你的心是小小的窗扉緊掩
"""

layout_dict = {
    "心": '❤️', '城': '🏰', '晚': '🌙',
    "小": 'drift', "向": 'drift',
    "的": 'drift', "月": 'drift'
}

formatted_poem = ""

for char in poem:

    if char in ("\n", "，"):
        formatted_poem += "\n"
    else:
        if char in layout_dict:
            formatted_poem += (layout_dict[char] + " ") if layout_dict[char] != "drift" else (" " + char)
        else:
            formatted_poem += char

print(formatted_poem)