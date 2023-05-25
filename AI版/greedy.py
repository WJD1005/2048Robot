import copy
import random


def try_move_up(map):
    """
    尝试向上移动，计算总分数。
    :param map: 地图
    :return: 是否有效, 移动获得的分数
    """
    is_valid = False
    score = 0
    map_temp = copy.deepcopy(map)  # 副本
    # 提取一列
    for j in range(4):
        # 遍历前方块
        for i in range(3):
            # 寻找下一个非0
            for next in range(i + 1, 4):
                if map_temp[next][j] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map_temp[i][j] == 0:
                        map_temp[i][j] = map_temp[next][j]
                        map_temp[next][j] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map_temp[i][j] == map_temp[next][j]:
                        map_temp[i][j] *= 2
                        map_temp[next][j] = 0
                        score += map_temp[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这列可以结束了
            else:
                break
    score += adjacent_check(map_temp)  # 计算相邻方块对分数
    return is_valid, score


def try_move_down(map):
    """
    尝试向下移动，计算总分数。
    :param map: 地图
    :return: 是否有效, 移动获得的分数
    """
    is_valid = False
    score = 0
    map_temp = copy.deepcopy(map)  # 副本
    # 提取一列
    for j in range(4):
        # 遍历前方块
        for i in range(3, 0, -1):
            # 寻找下一个非0
            for next in range(i - 1, -1, -1):
                if map_temp[next][j] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map_temp[i][j] == 0:
                        map_temp[i][j] = map_temp[next][j]
                        map_temp[next][j] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map_temp[i][j] == map_temp[next][j]:
                        map_temp[i][j] *= 2
                        map_temp[next][j] = 0
                        score += map_temp[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这列可以结束了
            else:
                break
    score += adjacent_check(map_temp)  # 计算相邻方块对分数
    return is_valid, score


def try_move_left(map):
    """
    尝试向左移动，计算总分数。
    :param map: 地图
    :return: 是否有效, 移动获得的分数
    """
    is_valid = False
    score = 0
    map_temp = copy.deepcopy(map)  # 副本
    # 提取一行
    for i in range(4):
        # 遍历前方块
        for j in range(3):
            # 寻找下一个非0
            for next in range(j + 1, 4):
                if map_temp[i][next] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map_temp[i][j] == 0:
                        map_temp[i][j] = map_temp[i][next]
                        map_temp[i][next] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map_temp[i][j] == map_temp[i][next]:
                        map_temp[i][j] *= 2
                        map_temp[i][next] = 0
                        score += map_temp[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这行可以结束了
            else:
                break
    score += adjacent_check(map_temp)  # 计算相邻方块对分数
    return is_valid, score


def try_move_right(map):
    """
    尝试向右移动，计算总分数。
    :param map: 地图
    :return: 是否有效, 移动获得的分数
    """
    is_valid = False
    score = 0
    map_temp = copy.deepcopy(map)  # 副本
    # 提取一行
    for i in range(4):
        # 遍历前方块
        for j in range(3, 0, -1):
            # 寻找下一个非0
            for next in range(j - 1, -1, -1):
                if map_temp[i][next] != 0:
                    # 如果前方块是0则移动，并继续往后看
                    if map_temp[i][j] == 0:
                        map_temp[i][j] = map_temp[i][next]
                        map_temp[i][next] = 0
                        is_valid = True
                    # 如果和前方块相等则合并并跳出不再找下一个避免重复合并
                    elif map_temp[i][j] == map_temp[i][next]:
                        map_temp[i][j] *= 2
                        map_temp[i][next] = 0
                        score += map_temp[i][j]
                        is_valid = True
                        break
                    # 如果和前方块不相等则直接跳出
                    else:
                        break
            # 后面没有非0了这行可以结束了
            else:
                break
    score += adjacent_check(map_temp)  # 计算相邻方块对分数
    return is_valid, score


try_move_list = [try_move_up, try_move_down, try_move_left, try_move_right]  # 移动函数列表


def adjacent_check(map):
    """
    检查相邻方块配对，一对相邻方块加方块数字的分数（合成的一半）。
    :param map: 地图
    :return: 相邻方块对分数
    """
    score = 0
    # 检查行有无2个相邻相同方块
    for i in range(4):
        j = 0
        while j < 3:
            if map[i][j] == map[i][j + 1]:
                score += map[i][j]
                j += 2  # 两两配对都跳过
            else:
                j += 1
    # 检查列有无2个相邻相同方块
    for j in range(4):
        i = 0
        while i < 3:
            if map[i][j] == map[i + 1][j]:
                score += map[i][j]
                i += 2  # 两两配对都跳过
            else:
                i += 1
    return score


def greedy_one_step(map):
    """
    输出贪心算法的结果。
    :param map: 地图
    :return: 移动方向，0:up, 1:down, 2:left, 3:right
    """
    max_score = 0
    max_score_direction = -1
    valid_direction = []
    # 遍历四个方向（不考虑移动后新增的方块）
    # 0:up, 1:down, 2:left, 3:right
    for direction in range(4):
        is_valid, score = try_move_list[direction](map)
        if is_valid:
            valid_direction.append(direction)
            if score > max_score:
                max_score = score
                max_score_direction = direction
    if max_score != 0:
        return max_score_direction
    # 无分数则随机一个有效移动方向
    else:
        return random.choice(valid_direction)  # 若已不能继续此处会报错，所以要避免不能继续时进来
