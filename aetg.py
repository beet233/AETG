#coding=gbk
import csv
import random

def test_jingdong():
    options = ['品牌', '能效等级', '支持IPv6', '类型', '处理器', '厚度', '机身材质', '内存容量', '屏幕尺寸', 'Pairs']
    # options = ['品牌', '能效等级', '支持IPv6', '类型', 'Pairs']
    brand = ['hp', 'thinkpad', 'lenovo', 'huawei', 'apple', 'dell', 'asus', 'haier', 'honor', 'acer', 'mi', 'mechrevo']
    power = ['一级能效', '二级能效', '三级能效', '五级能效']
    ipv6_support = ['yes', 'no']
    laptop_type = ['轻薄本', '游戏本', '高端轻薄本', '高端游戏本', '高性能轻薄本']
    cpu = ['麒麟', 'AMD 速龙', 'intel i5', '兆芯', '飞腾', '龙芯', 'Apple M2', 'intel i7', 'intel i9', 'intel i3', 'AMD R5',
           'AMD R7', 'AMD R9', 'AMD R3', '高通', 'Apple M1', 'Apple M1 Pro', 'Apple M1 Max', 'intel 赛扬', 'intel 至强', 'intel 奔腾']
    thickness = ['15.0mm 及以下', '15.1-18.0mm', '18.1-20.0mm', '20.0mm 以上']
    material = ['金属', '金属+复合材质', '复合材质', '含碳纤维']
    memory = ['4GB', '6GB', '48GB', '8GB', '12GB', '16GB', '20GB', '24GB', '32GB', '36GB', '40GB', '64GB', '128GB']
    size = ['13.0英寸以下', '13.0-13.9英寸', '14.0-14.9英寸', '15.0-15.9英寸', '16.0-16.9英寸', '17英寸', '17.3英寸', '18.4英寸']

    params = [len(brand), len(power), len(ipv6_support), len(laptop_type), len(cpu), len(thickness), len(material), len(memory), len(size)]
    # params = [len(brand), len(power), len(ipv6_support), len(laptop_type)]

    print("params: " + str(params))

    cover_array, cover_count_array = AETG(params, 2)

    print("cover_array: " + str(cover_array))

    jingdong_csv = open("jingdong.csv", "w+", encoding='gbk', newline='')
    jingdong_writer = csv.writer(jingdong_csv)
    jingdong_writer.writerow(options)

    for idx, combination in enumerate(cover_array):
        transfered_combination = []
        transfered_combination.append(brand[combination[0]])
        transfered_combination.append(power[combination[1]])
        transfered_combination.append(ipv6_support[combination[2]])
        transfered_combination.append(laptop_type[combination[3]])
        transfered_combination.append(cpu[combination[4]])
        transfered_combination.append(thickness[combination[5]])
        transfered_combination.append(material[combination[6]])
        transfered_combination.append(memory[combination[7]])
        transfered_combination.append(size[combination[8]])
        transfered_combination.append(cover_count_array[idx])
        jingdong_writer.writerow(transfered_combination)

    jingdong_csv.close()

def test_xiecheng():
    options = ['出发地', '目的地', '仅看直飞', '舱型', '乘客类型']
    start = ['国内', '国际·中国港澳台热门', '亚洲', '欧洲', '美洲', '非洲', '大洋洲']
    end = ['国内', '国际·中国港澳台热门', '亚洲', '欧洲', '美洲', '非洲', '大洋洲']
    direct_only = ['yes', 'no']
    board_type = ['经济/超经舱', '公务/头等舱', '公务舱', '头等舱']
    customer = ['仅成人', '成人与儿童', '成人与婴儿', '成人与儿童与婴儿']

    params = [len(start), len(end), len(direct_only), len(board_type), len(customer)]

    print("params: " + str(params))

    cover_array, cover_count_array = AETG(params, 3)

    print("cover_array: " + str(cover_array))

    xiecheng_csv = open("xiecheng.csv", "w+", encoding='gbk', newline='')
    xiecheng_writer = csv.writer(xiecheng_csv)
    xiecheng_writer.writerow(options)

    for idx, combination in enumerate(cover_array):
        transfered_combination = []
        transfered_combination.append(start[combination[0]])
        transfered_combination.append(end[combination[1]])
        transfered_combination.append(direct_only[combination[2]])
        transfered_combination.append(board_type[combination[3]])
        transfered_combination.append(customer[combination[4]])
        transfered_combination.append(cover_count_array[idx])
        xiecheng_writer.writerow(transfered_combination)

    xiecheng_csv.close()

# t-way AETG
def AETG(params, t):
    params_num = len(params)
    expected_candidate_group = 20
    uncovered_pairs = []
    # 先生成 params 的 index 中取 t 个的所有结果，再对这些结果中的每个项目的可能取值做回溯遍历
    t_size_tuples = []
    generate_all_t_size_tuples(len(params), t, [], t_size_tuples, 0)
    # print("t_size_tuples: " + str(t_size_tuples))
    generate_all_t_size_combinations(params, t_size_tuples, uncovered_pairs)
    print("uncovered_pairs: " + str(uncovered_pairs))
    covered_pairs = []
    # first_param_index, first_value = find_most_popular_param_value_in(uncovered_pairs, params)
    # print(first_param_index, first_value)
    cover_array = []
    cover_count_array = []
    while len(uncovered_pairs) > 0:
        most_new_cover_candidate_group = []
        most_new_cover_candidate_group_covered_pairs = []
        # 需要 expected_candidate_group 个候选组
        for i in range(expected_candidate_group):
            # 新建一个空的候选组，初始化为全 -1 表暂无有效参数
            candidate_group = [-1] * len(params)
            # 对于第一个参数，我们从 ucps 里找到出现频率最高的值（一个 index 和一个 value 唯一确定一个值）
            # print("uncovered_pairs: " + str(uncovered_pairs))
            first_param_index, first_value = find_most_popular_param_value_in(uncovered_pairs, params)
            # print("first_param_index: " + str(first_param_index) + " first_value: " + str(first_value))
            candidate_group[first_param_index] = first_value
            print("candidate_group: " + str(candidate_group))
            # 用固定的循环规律确定剩下的 param value
            while True:
                not_selected_param = []
                selected_param = []
                for param_index, param_value in enumerate(candidate_group):
                    if param_value == -1:
                        not_selected_param.append(param_index)
                    else:
                        selected_param.append(param_index)
                if len(not_selected_param) == 0:
                    break
                # print("selected_param: " + str(selected_param))
                # print("not_selected_param: " + str(not_selected_param))
                # 从 not_selected_param 中随机选择下一个处理的 param
                next_param_index = random.choice(not_selected_param)
                if len(selected_param) < t:
                    max_ucps_included_count = 0
                    max_param_values = []
                    for j in range(params[next_param_index]):
                        candidate_group[next_param_index] = j
                        # 计算这个 candiate_group 目前被多少 ucps 包括
                        ucps_included_count = 0
                        for uncovered_pair in uncovered_pairs:
                            included = True
                            for k in range(len(params)):
                                if uncovered_pair[k] != candidate_group[k] and candidate_group[k] != -1:
                                    included = False
                            if included:
                                ucps_included_count += 1
                        # 如果是最大的，那么记录
                        if ucps_included_count > max_ucps_included_count:
                            # print("update max_ucps_included_count to " + str(ucps_included_count))
                            # print("max_param_value: " + str(j))
                            max_ucps_included_count = ucps_included_count
                            max_param_values = [j]
                        elif ucps_included_count == max_ucps_included_count:
                            max_param_values.append(j)
                        candidate_group[next_param_index] = -1
                    # 将最大的赋值给 candidate_group[next_param_index]
                    candidate_group[next_param_index] = random.choice(max_param_values)
                    print("term1 candidate_group: " + str(candidate_group))
                else:
                    # 获取所有从 selected param 里选 t - 1 个的组合
                    t_minus_one_size_selected_index_tuples = []
                    # 先获取到所有可能的 t - 1 个 selected_param_index
                    # 注意，下一行生成的是 在 seleted_param 这个列表里的 index，还要从里面取成真正的 param_index
                    generate_all_t_size_tuples(len(selected_param), t - 1, [], t_minus_one_size_selected_index_tuples, 0)
                    t_minus_one_size_param_index_tuples = []
                    for selected_index_tuple in t_minus_one_size_selected_index_tuples:
                        param_index_tuple = []
                        for selected_index in selected_index_tuple:
                            param_index_tuple.append(selected_param[selected_index])
                        t_minus_one_size_param_index_tuples.append(param_index_tuple)
                    # 再用 param_index 生成完整的 combination
                    combinations = []
                    for tuple in t_minus_one_size_param_index_tuples:
                        combination = [-1] * len(params)
                        for param_index in tuple:
                            combination[param_index] = candidate_group[param_index]
                        combinations.append(combination)
                    # 至此，combinations 内包含所有 [-1,-1,-1,8,-1,9,-1,-1,-1] 这样完整形式的 t - 1 个 param 被 select 的组合
                    max_same_ucps_count = 0
                    max_param_values = []
                    for j in range(params[next_param_index]):
                        same_ucps_count = 0
                        # 遍历所有 t - 1 个的组合
                        for combination in combinations:
                            # 和 next_param_index 组合
                            combination[next_param_index] = j
                            # 如果组合后是一个 ucps，那么计数加一
                            same = True
                            for k in range(len(params)):
                                if uncovered_pair[k] != combination[k]:
                                    same = False
                            if same:
                                same_ucps_count += 1
                            combination[next_param_index] = -1
                        # 如果计数是最大的，那么记录
                        if same_ucps_count > max_same_ucps_count:
                            max_same_ucps_count = same_ucps_count
                            max_param_values = [j]
                        elif same_ucps_count == max_same_ucps_count:
                            max_param_values.append(j)
                    # 将最大的赋值给 candidate_group[next_param_index]
                    candidate_group[next_param_index] = random.choice(max_param_values)
                    print("term2 candidate_group: " + str(candidate_group))
            # 计算这次生成的 candidate_group 包含了多少个 uncovered_pairs，如果超过最大值，则记录
            new_covered_pairs = []
            for uncovered_pair in uncovered_pairs:
                covered = True
                for j in range(len(params)):
                    if uncovered_pair[j] != -1 and uncovered_pair[j] != candidate_group[j]:
                        covered = False
                if covered:
                    new_covered_pairs.append(uncovered_pair)
            if len(new_covered_pairs) >= len(most_new_cover_candidate_group_covered_pairs):
                most_new_cover_candidate_group = candidate_group
                most_new_cover_candidate_group_covered_pairs = new_covered_pairs
            # print("this cover array: " + str(candidate_group))
            # print("this covered pairs: " + str(len(new_covered_pairs)))
        # 将包含了最多 uncovered_pairs 的 candidate_group 加入 cover_array
        print("new cover array: " + str(most_new_cover_candidate_group))
        print("new covered pairs: " + str(len(most_new_cover_candidate_group_covered_pairs)))
        cover_array.append(most_new_cover_candidate_group)
        cover_count_array.append(len(most_new_cover_candidate_group_covered_pairs))
        # 更新 ucps 和 cps，从 ucps 中移除 most_new_cover_candidate_group_covered_pairs 中的 pair，加入到 cps
        covered_pairs.extend(most_new_cover_candidate_group_covered_pairs)
        i = 0
        while i < (len(uncovered_pairs)):
            for new_covered_pair in most_new_cover_candidate_group_covered_pairs:
                same = True
                for j in range(len(params)):
                    if new_covered_pair[j] != uncovered_pairs[i][j]:
                        same = False
                if same:
                    uncovered_pairs.pop(i)
                    i -= 1
                    break
            i += 1
        print("left uncovered pairs: " + str(len(uncovered_pairs)))
    return cover_array, cover_count_array

# generate all tuples with t items
def generate_all_t_size_tuples(length, t, tuple, t_size_tuples, offset):
    if t > 1:
        for param_index in range(length - offset):
            if param_index > length - offset - t:
                break
            tuple.append(param_index + offset)
            generate_all_t_size_tuples(length, t - 1, tuple, t_size_tuples, param_index + offset + 1)
            tuple.pop()
    elif t == 1:
        for param_index in range(length - offset):
            tuple.append(param_index + offset)
            t_size_tuples.append(tuple[:])
            tuple.pop()
    else:
        raise Exception("t == 0")

# a t-sized combination seem like [-1,-1,-1,8,-1,9,-1,-1,3], 8,9,3 means useful params' values.
def generate_all_t_size_combinations(params, t_size_tuples, t_size_combinations):
    for tuple in t_size_tuples:
        combination = [-1] * len(params)
        combinations = []
        t_size_tuple_to_combinations(params, tuple, combination, combinations)
        # print(combinations)
        t_size_combinations.extend(combinations)
        # print(t_size_combinations)

def t_size_tuple_to_combinations(params, tuple, combination, combinations):
    for i in range(params[tuple[0]]):
        combination[tuple[0]] = i
        if len(tuple) > 1:
            t_size_tuple_to_combinations(params, tuple[1:], combination, combinations)
        else:
            combinations.append(combination[:])
        combination[tuple[0]] = -1

def find_most_popular_param_value_in(uncovered_pairs, params):
    count_map = []
    for param in params:
        count_map.append([0] * param)
    for pair in uncovered_pairs:
        for index, value in enumerate(pair):
            if value > -1:
                count_map[index][value] += 1
    # print("count_map: " + str(count_map))
    max_count = 0
    max_param_index = -1
    max_value = -1
    for param_index, single_param_count_map in enumerate(count_map):
        for value, single_value_count in enumerate(single_param_count_map):
            if single_value_count >= max_count:
                max_param_index = param_index
                max_value = value
                max_count = single_value_count
    return max_param_index, max_value

if __name__ == '__main__':
    # test_jingdong()
    test_xiecheng()
