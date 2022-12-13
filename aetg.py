#coding=gbk
import csv
import random

def test_jingdong():
    options = ['Ʒ��', '��Ч�ȼ�', '֧��IPv6', '����', '������', '���', '�������', '�ڴ�����', '��Ļ�ߴ�', 'Pairs']
    # options = ['Ʒ��', '��Ч�ȼ�', '֧��IPv6', '����', 'Pairs']
    brand = ['hp', 'thinkpad', 'lenovo', 'huawei', 'apple', 'dell', 'asus', 'haier', 'honor', 'acer', 'mi', 'mechrevo']
    power = ['һ����Ч', '������Ч', '������Ч', '�弶��Ч']
    ipv6_support = ['yes', 'no']
    laptop_type = ['�ᱡ��', '��Ϸ��', '�߶��ᱡ��', '�߶���Ϸ��', '�������ᱡ��']
    cpu = ['����', 'AMD ����', 'intel i5', '��о', '����', '��о', 'Apple M2', 'intel i7', 'intel i9', 'intel i3', 'AMD R5',
           'AMD R7', 'AMD R9', 'AMD R3', '��ͨ', 'Apple M1', 'Apple M1 Pro', 'Apple M1 Max', 'intel ����', 'intel ��ǿ', 'intel ����']
    thickness = ['15.0mm ������', '15.1-18.0mm', '18.1-20.0mm', '20.0mm ����']
    material = ['����', '����+���ϲ���', '���ϲ���', '��̼��ά']
    memory = ['4GB', '6GB', '48GB', '8GB', '12GB', '16GB', '20GB', '24GB', '32GB', '36GB', '40GB', '64GB', '128GB']
    size = ['13.0Ӣ������', '13.0-13.9Ӣ��', '14.0-14.9Ӣ��', '15.0-15.9Ӣ��', '16.0-16.9Ӣ��', '17Ӣ��', '17.3Ӣ��', '18.4Ӣ��']

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
    options = ['������', 'Ŀ�ĵ�', '����ֱ��', '����', '�˿�����']
    start = ['����', '���ʡ��й��۰�̨����', '����', 'ŷ��', '����', '����', '������']
    end = ['����', '���ʡ��й��۰�̨����', '����', 'ŷ��', '����', '����', '������']
    direct_only = ['yes', 'no']
    board_type = ['����/������', '����/ͷ�Ȳ�', '�����', 'ͷ�Ȳ�']
    customer = ['������', '�������ͯ', '������Ӥ��', '�������ͯ��Ӥ��']

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
    # ������ params �� index ��ȡ t �������н�����ٶ���Щ����е�ÿ����Ŀ�Ŀ���ȡֵ�����ݱ���
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
        # ��Ҫ expected_candidate_group ����ѡ��
        for i in range(expected_candidate_group):
            # �½�һ���յĺ�ѡ�飬��ʼ��Ϊȫ -1 ��������Ч����
            candidate_group = [-1] * len(params)
            # ���ڵ�һ�����������Ǵ� ucps ���ҵ�����Ƶ����ߵ�ֵ��һ�� index ��һ�� value Ψһȷ��һ��ֵ��
            # print("uncovered_pairs: " + str(uncovered_pairs))
            first_param_index, first_value = find_most_popular_param_value_in(uncovered_pairs, params)
            # print("first_param_index: " + str(first_param_index) + " first_value: " + str(first_value))
            candidate_group[first_param_index] = first_value
            print("candidate_group: " + str(candidate_group))
            # �ù̶���ѭ������ȷ��ʣ�µ� param value
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
                # �� not_selected_param �����ѡ����һ������� param
                next_param_index = random.choice(not_selected_param)
                if len(selected_param) < t:
                    max_ucps_included_count = 0
                    max_param_values = []
                    for j in range(params[next_param_index]):
                        candidate_group[next_param_index] = j
                        # ������� candiate_group Ŀǰ������ ucps ����
                        ucps_included_count = 0
                        for uncovered_pair in uncovered_pairs:
                            included = True
                            for k in range(len(params)):
                                if uncovered_pair[k] != candidate_group[k] and candidate_group[k] != -1:
                                    included = False
                            if included:
                                ucps_included_count += 1
                        # ��������ģ���ô��¼
                        if ucps_included_count > max_ucps_included_count:
                            # print("update max_ucps_included_count to " + str(ucps_included_count))
                            # print("max_param_value: " + str(j))
                            max_ucps_included_count = ucps_included_count
                            max_param_values = [j]
                        elif ucps_included_count == max_ucps_included_count:
                            max_param_values.append(j)
                        candidate_group[next_param_index] = -1
                    # �����ĸ�ֵ�� candidate_group[next_param_index]
                    candidate_group[next_param_index] = random.choice(max_param_values)
                    print("term1 candidate_group: " + str(candidate_group))
                else:
                    # ��ȡ���д� selected param ��ѡ t - 1 �������
                    t_minus_one_size_selected_index_tuples = []
                    # �Ȼ�ȡ�����п��ܵ� t - 1 �� selected_param_index
                    # ע�⣬��һ�����ɵ��� �� seleted_param ����б���� index����Ҫ������ȡ�������� param_index
                    generate_all_t_size_tuples(len(selected_param), t - 1, [], t_minus_one_size_selected_index_tuples, 0)
                    t_minus_one_size_param_index_tuples = []
                    for selected_index_tuple in t_minus_one_size_selected_index_tuples:
                        param_index_tuple = []
                        for selected_index in selected_index_tuple:
                            param_index_tuple.append(selected_param[selected_index])
                        t_minus_one_size_param_index_tuples.append(param_index_tuple)
                    # ���� param_index ���������� combination
                    combinations = []
                    for tuple in t_minus_one_size_param_index_tuples:
                        combination = [-1] * len(params)
                        for param_index in tuple:
                            combination[param_index] = candidate_group[param_index]
                        combinations.append(combination)
                    # ���ˣ�combinations �ڰ������� [-1,-1,-1,8,-1,9,-1,-1,-1] ����������ʽ�� t - 1 �� param �� select �����
                    max_same_ucps_count = 0
                    max_param_values = []
                    for j in range(params[next_param_index]):
                        same_ucps_count = 0
                        # �������� t - 1 �������
                        for combination in combinations:
                            # �� next_param_index ���
                            combination[next_param_index] = j
                            # �����Ϻ���һ�� ucps����ô������һ
                            same = True
                            for k in range(len(params)):
                                if uncovered_pair[k] != combination[k]:
                                    same = False
                            if same:
                                same_ucps_count += 1
                            combination[next_param_index] = -1
                        # ������������ģ���ô��¼
                        if same_ucps_count > max_same_ucps_count:
                            max_same_ucps_count = same_ucps_count
                            max_param_values = [j]
                        elif same_ucps_count == max_same_ucps_count:
                            max_param_values.append(j)
                    # �����ĸ�ֵ�� candidate_group[next_param_index]
                    candidate_group[next_param_index] = random.choice(max_param_values)
                    print("term2 candidate_group: " + str(candidate_group))
            # ����������ɵ� candidate_group �����˶��ٸ� uncovered_pairs������������ֵ�����¼
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
        # ����������� uncovered_pairs �� candidate_group ���� cover_array
        print("new cover array: " + str(most_new_cover_candidate_group))
        print("new covered pairs: " + str(len(most_new_cover_candidate_group_covered_pairs)))
        cover_array.append(most_new_cover_candidate_group)
        cover_count_array.append(len(most_new_cover_candidate_group_covered_pairs))
        # ���� ucps �� cps���� ucps ���Ƴ� most_new_cover_candidate_group_covered_pairs �е� pair�����뵽 cps
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
