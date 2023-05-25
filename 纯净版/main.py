import pygame
import sys
import random

# region 游戏核心数据
map = []
score = 0
best_score = 0
step = 0
# endregion

# region UI数据
screen_width, screen_height = 575, 725  # 窗口尺寸
padding = 50  # 窗口内边距
text_width, text_height = 160, 30
info_width, info_height = 90, 50  # 信息块尺寸
button_width, button_height = 90, 30  # 按钮尺寸
horizontal_margin = 10  # 水平边距
vertical_margin = 20  # 垂直边距
block_size = 100  # 方块尺寸
block_margin = 15  # 方块外边距
map_size = block_size * 4 + block_margin * 5  # 地图大小
background_color = '#faf8ef'  # 背景色
map_background_color = '#bbada0'  # 地图背景色
info_background_color = '#bbada0'  # 信息块背景色
button_background_color = '#8f7a66'  # 按钮背景色
font_color_dark = '#776e65'  # 字体深色
font_color_light = '#f9f6f2'  # 字体浅色
font_color_info = '#eee4da'  # 信息块文本字体颜色
# 方块样式，[背景色, 字体颜色, 字号]
block_style = {
    0: '#cdc1b4',
    2: ['#eee4da', '#776e65', 60],
    4: ['#ede0c8', '#776e65', 60],
    8: ['#f2b179', '#f9f6f2', 60],
    16: ['#f59563', '#f9f6f2', 60],
    32: ['#f67c5f', '#f9f6f2', 60],
    64: ['#f65e3b', '#f9f6f2', 60],
    128: ['#edcf72', '#f9f6f2', 50],
    256: ['#edcc61', '#f9f6f2', 50],
    512: ['#edc850', '#f9f6f2', 50],
    1024: ['#edc53f', '#f9f6f2', 40],
    2048: ['#edc22e', '#f9f6f2', 40],
    4096: ['#3c3a32', '#f9f6f2', 40],
    8192: ['#3c3a32', '#f9f6f2', 40],
    'super': ['#3c3a32', '#f9f6f2', 30],
}
# endregion


# region 按钮类
class Button(object):
    def __init__(self, x, y, width, height, color, text, font, font_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_surface = pygame.Surface((width, height), flags=pygame.HWSURFACE)
        self.button_surface.fill(color)
        text_render = font.render(text, True, font_color)
        text_rect = text_render.get_rect()
        text_rect.center = (width / 2, height / 2)
        self.button_surface.blit(text_render, text_rect)

    def display(self, screen):
        screen.blit(self.button_surface, (self.x, self.y))

    def click_check(self, click_position):
        # 检查传入的点击坐标是否是按钮坐标
        if self.x < click_position[0] < self.x + self.width and self.y < click_position[1] < self.y + self.height:
            return True
        else:
            return False


button_dic = {}
# endregion


def game_init():
    """
    游戏初始化。
    :return: 窗口对象
    """
    global best_score, button_dic
    # 设置窗口
    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)  # 创建窗口
    pygame.display.set_caption('2048 By 星云质心')  # 设置窗口标题
    screen.fill(pygame.Color(background_color))  # 窗口背景色
    # 显示logo
    font = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', 70)
    logo = font.render('2048', True, font_color_dark)
    logo_rect = logo.get_rect()
    logo_rect.x = padding
    logo_rect.y = padding - logo_rect.height + 70  # 去除字体上方空位的影响
    screen.blit(logo, logo_rect)
    # 创建并显示按钮
    font = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', 20)  # 按钮字体，直接传入
    new_game_button = Button(screen_width - padding - button_width, padding + info_height + vertical_margin,
                             button_width, button_height, button_background_color, '新游戏', font, font_color_light)
    new_game_button.display(screen)
    button_dic['new_game_button'] = new_game_button  # 保存到字典
    # 读取最好成绩
    with open('BestScore.txt', 'r') as f:
        best_score = int(f.readline())
    return screen


def get_empty():
    """
    获取空格子索引。
    :return: 空格子索引列表
    """
    global map
    empty_list = []
    for i in range(4):
        for j in range(4):
            if map[i][j] == 0:
                empty_list.append((i, j))
    return empty_list


def create_init_block():
    """
    创建初始化的2个方块。
    :return: 无
    """
    global map
    for i in range(2):
        block = random.choice(get_empty())  # 取一随机空格
        map[block[0]][block[1]] = 2


def create_block():
    """
    创建新的方块。
    :return: 无
    """
    global map
    empty_list = get_empty()
    block = random.choice(empty_list)  # 取一随机空格
    map[block[0]][block[1]] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])  # 出现2的概率是4的9倍


def game_start(screen):
    """
    游戏开始。
    :param screen: 窗口对象
    :return: 无
    """
    global map, score, step
    # 清空数据
    map = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    score = 0
    step = 0
    create_init_block()  # 创建初始两方块
    # 显示初始内容
    show_text(screen, '关注星云质心谢谢喵')  # 显示logo下方可变文本
    draw_map(screen)  # 画地图
    show_info(screen)  # 显示信息


def move_up():
    """
    向上移动。
    :return: True：移动有效，False：移动无效
    """
    global map, score
    is_valid = False  # 是否有效移动标记
    # 提取一列
    for j in range(4):
        # 遍历前方块
        for i in range(3):
            # 寻找下一个非0
            for next in range(i + 1, 4):
                if map[next][j] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map[i][j] == 0:
                        map[i][j] = map[next][j]
                        map[next][j] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map[i][j] == map[next][j]:
                        map[i][j] *= 2
                        map[next][j] = 0
                        score += map[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这列可以结束了
            else:
                break
    return is_valid


def move_down():
    """
    向下移动。
    :return: True：移动有效，False：移动无效
    """
    global map, score
    is_valid = False  # 是否有效移动标记
    # 提取一列
    for j in range(4):
        # 遍历前方块
        for i in range(3, 0, -1):
            # 寻找下一个非0
            for next in range(i - 1, -1, -1):
                if map[next][j] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map[i][j] == 0:
                        map[i][j] = map[next][j]
                        map[next][j] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map[i][j] == map[next][j]:
                        map[i][j] *= 2
                        map[next][j] = 0
                        score += map[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这列可以结束了
            else:
                break
    return is_valid


def move_left():
    """
    向左移动。
    :return: True：移动有效，False：移动无效
    """
    global map, score
    is_valid = False  # 是否有效移动标记
    # 提取一行
    for i in range(4):
        # 遍历前方块
        for j in range(3):
            # 寻找下一个非0
            for next in range(j + 1, 4):
                if map[i][next] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map[i][j] == 0:
                        map[i][j] = map[i][next]
                        map[i][next] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map[i][j] == map[i][next]:
                        map[i][j] *= 2
                        map[i][next] = 0
                        score += map[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这行可以结束了
            else:
                break
    return is_valid


def move_right():
    """
    向右移动。
    :return: True：移动有效，False：移动无效
    """
    global map, score
    is_valid = False  # 是否有效移动标记
    # 提取一行
    for i in range(4):
        # 遍历前方块
        for j in range(3, 0, -1):
            # 寻找下一个非0
            for next in range(j - 1, -1, -1):
                if map[i][next] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map[i][j] == 0:
                        map[i][j] = map[i][next]
                        map[i][next] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map[i][j] == map[i][next]:
                        map[i][j] *= 2
                        map[i][next] = 0
                        score += map[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这行可以结束了
            else:
                break
    return is_valid


move_list = [move_up, move_down, move_left, move_right]  # 移动函数列表


def judge():
    """
    判断游戏是否可以继续进行。
    :return: True：可以继续，False：不可继续
    """
    global map
    empty_list = get_empty()
    # 如果未满
    if len(empty_list) != 0:
        return True
    # 检查行有无相邻相同方块
    for i in range(4):
        for j in range(3):
            if map[i][j] == map[i][j + 1]:
                return True
    # 检查列有无相邻相同方块
    for j in range(4):
        for i in range(3):
            if map[i][j] == map[i + 1][j]:
                return True
    # 满了且无相邻相同方块，失败
    return False


def game_over(screen):
    """
    游戏结束。
    :param screen: 窗口对象
    :return: 无
    """
    global score, best_score
    # 显示失败
    show_text(screen, '已经结束啦！')
    # 判断是否超过最高分并记录
    if score > best_score:
        best_score = score
        show_info(screen)
        with open('BestScore.txt', 'w') as f:
            f.write(str(best_score))


def draw_map(screen):
    """
    画地图。
    :param screen: 窗口对象
    :return: 无
    """
    global map
    map_surface = pygame.Surface((map_size, map_size), flags=pygame.HWSURFACE)  # 创建地图对象
    map_surface.fill(pygame.Color(map_background_color))  # 填充地图背景色
    # 在地图上画方块
    for i in range(4):
        for j in range(4):
            block = pygame.Surface((block_size, block_size), flags=pygame.HWSURFACE)  # 方块对象
            num = map[i][j]  # 方块数字
            if num == 0:
                block.fill(pygame.Color(block_style[0]))  # 填充方块背景色
            elif 0 < num <= 8192:
                block.fill(pygame.Color(block_style[num][0]))  # 填充方块背景色
                font = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', block_style[num][2])  # 字体
                num = font.render(str(num), True, block_style[num][1])  # 数字对象
                num_rect = num.get_rect()  # 数字rect区域大小
                num_rect.center = (block_size / 2, block_size / 2)  # 将数字rect区域设置到方块中间（相对block的坐标）
                block.blit(num, num_rect)  # 在方块中间写数字
            else:
                block.fill(pygame.Color(block_style['super'][0]))  # 填充方块背景色
                font = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', block_style['super'][2])  # 字体
                num = font.render(str(num), True, block_style['super'][1])  # 数字对象
                num_rect = num.get_rect()  # 数字rect区域大小
                num_rect.center = (block_size / 2, block_size / 2)  # 将数字rect区域设置到方块中间（相对block的坐标）
                block.blit(num, num_rect)  # 在方块中间写数字
            map_surface.blit(block, (
                j * block_size + (j + 1) * block_margin, i * block_size + (i + 1) * block_margin))  # 把方块画到地图上
    screen.blit(map_surface, (padding, screen_height - padding - map_size))  # 把地图画到窗口上


def show_info(screen):
    """
    显示游戏信息（分数、步数、最高分）。
    :param screen: 窗口对象
    :return: 无
    """
    global score, step, best_score
    # 加载字体
    font_text = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', 15)
    font_num = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', 25)
    # 分数
    score_surface = pygame.Surface((info_width, info_height), flags=pygame.HWSURFACE)
    score_surface.fill(pygame.Color(info_background_color))
    score_text = font_text.render('分数', True, font_color_info)
    score_num = font_num.render(str(score), True, font_color_light)
    score_text_rect = score_text.get_rect()
    score_num_rect = score_num.get_rect()
    score_text_rect.centerx = 45
    score_text_rect.y = 5
    score_num_rect.centerx = 45
    score_num_rect.y = 20
    score_surface.blit(score_text, score_text_rect)
    score_surface.blit(score_num, score_num_rect)
    screen.blit(score_surface, (screen_width - padding - info_width * 3 - horizontal_margin * 2, padding))
    # 步数
    step_surface = pygame.Surface((info_width, info_height), flags=pygame.HWSURFACE)
    step_surface.fill(pygame.Color(info_background_color))
    step_text = font_text.render('步数', True, font_color_info)
    step_num = font_num.render(str(step), True, font_color_light)
    step_text_rect = step_text.get_rect()
    step_num_rect = step_num.get_rect()
    step_text_rect.centerx = 45
    step_text_rect.y = 5
    step_num_rect.centerx = 45
    step_num_rect.y = 20
    step_surface.blit(step_text, step_text_rect)
    step_surface.blit(step_num, step_num_rect)
    screen.blit(step_surface, (screen_width - padding - info_width * 2 - horizontal_margin * 1, padding))
    # 最高分
    best_score_surface = pygame.Surface((info_width, info_height), flags=pygame.HWSURFACE)
    best_score_surface.fill(pygame.Color(info_background_color))
    best_score_text = font_text.render('最高分', True, font_color_info)
    best_score_num = font_num.render(str(best_score), True, font_color_light)
    best_score_text_rect = best_score_text.get_rect()
    best_score_num_rect = best_score_num.get_rect()
    best_score_text_rect.centerx = 45
    best_score_text_rect.y = 5
    best_score_num_rect.centerx = 45
    best_score_num_rect.y = 20
    best_score_surface.blit(best_score_text, best_score_text_rect)
    best_score_surface.blit(best_score_num, best_score_num_rect)
    screen.blit(best_score_surface, (screen_width - padding - info_width, padding))


def show_text(screen, text):
    """
    显示logo下方的文本信息。
    :param screen: 窗口对象
    :param text: 文本
    :return: 无
    """
    # 定死字体，故文本不要太长
    font = pygame.font.Font('Fonts/HarmonyOS_Sans_SC_Black.ttf', 15)
    text_surface = pygame.Surface((text_width, text_height), flags=pygame.HWSURFACE)
    text_surface.fill(pygame.Color(background_color))
    text_render = font.render(text, True, font_color_dark)
    text_rect = text_render.get_rect()
    text_rect.centery = text_height / 2
    text_surface.blit(text_render, text_rect)
    screen.blit(text_surface, (padding, padding + info_height + vertical_margin))


def game_run(screen):
    """
    游戏运行主函数。
    :param screen: 窗口对象
    :return: 无
    """
    global step, button_dic
    game_start(screen)
    restart_flag = False
    while not restart_flag:
        # 循环获取事件，监听事件状态
        for event in pygame.event.get():
            # 判断是否点击关闭
            if event.type == pygame.QUIT:
                pygame.quit()  # 卸载所有模块
                sys.exit()  # 终止程序，确保退出程序
            # 键盘
            elif event.type == pygame.KEYDOWN:
                # 上下左右
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    direction = -1
                    if event.key == pygame.K_UP:
                        direction = 0
                    elif event.key == pygame.K_DOWN:
                        direction = 1
                    elif event.key == pygame.K_LEFT:
                        direction = 2
                    elif event.key == pygame.K_RIGHT:
                        direction = 3
                    # 移动有效才进行创建新方块、更新画面、判断是否可以继续
                    if move_list[direction]():
                        step += 1
                        create_block()  # 移动后创建新方块
                        draw_map(screen)  # 画地图
                        show_info(screen)  # 显示信息
                        # 判断游戏是否可以继续
                        if not judge():
                            game_over(screen)  # 游戏结束
                # R重开
                elif event.key == pygame.K_r:
                    restart_flag = True
                    break
            # 鼠标
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 新游戏按钮
                if button_dic['new_game_button'].click_check(event.pos):
                    restart_flag = True
                    break

        pygame.display.flip()  # 更新屏幕内容


def main():
    global map, score, step, best_score
    screen = game_init()  # 初始化游戏
    # 局循环
    while True:
        game_run(screen)  # 游戏运行


if __name__ == '__main__':
    main()
