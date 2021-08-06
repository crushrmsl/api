# -*- coding: utf-8 -*-


import openpyxl
from common.logger import output_log


# pip install openpyxl


class Case(object):
    # 用这个类来存储用例
    def __init__(self, attrs):
        """
        初始化用例
        :param attrs: zip类型--> [（key1,value1),（key2,value2)....]
        """
        for item in attrs:
            # print(item)
            setattr(self, item[0], item[1])


class ReadExcel(object):
    """
    读取Excel数据
    """

    def __init__(self, file_path, sheet_name):
        """
        初始化读取对象
        :param file_path: 文件名，测试用例文件--> str
        :param sheet_name: 表单名--> str
        """
        self.file_path = file_path
        self.sheet_name = sheet_name

    def open(self):
        output_log.info(f"正在读取excel数据, file_path--> {self.file_path}, sheet_name--> {self.sheet_name}")
        # 打开工作簿，传入的指定文件名
        self.wb = openpyxl.load_workbook(self.file_path)
        # 选取表单，传入的指定表单
        self.sheet = self.wb[self.sheet_name]

    def close(self):
        """
        关闭工作簿
        :return: None
        """
        output_log.info(f'正在关闭工作簿, file_path--> {self.file_path}, sheet_name--> {self.sheet_name}')
        self.wb.close()

    def read_line_data(self):
        """
        执行读取数据
        :return: list
        """
        # 打开工作簿
        self.open()
        # 按行获取数据转换成列表
        res = self.sheet.rows
        # print(res)
        # print(type(res))
        rows_data = list(self.sheet.rows)
        # print(rows_data)

        # 获取表单的表头信息
        titles = []
        for title in rows_data[0]:
            # 对title是否为空进行过滤，容错机制
            if title.value:
                titles.append(title.value)

        # print(titles)

        # 定义一个空列表用来存储所有的用例
        cases = []
        # 从第2行开始，就是测试用例数据了
        for case in rows_data[1:]:
            # data用来临时存放每行的用例数据
            data = []
            for cell in case:
                data.append(cell.value)
            # print(data)
            # 将title与测试用例数据组合，形成每行测试用例,一行行读取数据，无需加list
            case_data = zip(titles, data)
            # 创建一个Case类的对象，用来保存用例数据，
            case_obj = Case(case_data)
            # 将该条数据放入cases中
            cases.append(case_obj)
        # 关闭工作簿,并返回读取的数据-->list
        self.close()
        return cases

    def read_line_data_by_column_value(self, column, value):
        """
        按指定列的value来读取数据 如只获取第3列值为login的用例的所有数据
        :param column: 指定列
        :param value: 指定列中指定value
        :return: 读取指定列中指定value的用例的所有数据 list-object
        """
        # 打开工作簿
        self.open()
        # 按行获取数据转换成列表
        rows_data = list(self.sheet.rows)

        # 获取表单的表头信息
        titles = []
        for title in rows_data[0]:
            # 对title是否为空进行过滤，容错机制
            if title.value:
                titles.append(title.value)

        # 定义一个空列表用来存储所有的用例
        cases = []
        # 从第2行开始，就是测试用例数据了
        for case in rows_data[1:]:
            # 过滤数据 只读取指定api_name的数据
            # 判断每行的第4个数据(api_name) 不是指定的api_name 就跳过本次循环 达到不读取不存储非指定api_name的数据的效果
            if case[column-1].value != value:
                continue
            # data用例临时存放每行的用例数据
            data = []
            for cell in case:
                if cell.value:
                    data.append(cell.value)
            else:
                pass
            # 在组装之前 筛选api_name的测试用例数据
            # if api_name in data:
            # 将title与测试用例数据组合，形成每行测试用例,一行行读取数据，无需加list
            case_data = zip(titles, data)
            # 创建一个Case类的对象，用来保存用例数据，
            case_obj = Case(case_data)
            # 将该条数据放入cases中
            cases.append(case_obj)
        # 关闭工作簿,并返回读取的数据-->list
        self.close()
        return cases

    def read_line_data_by_title_value(self, t, value):
        """
        依据指定title的value来读取数据 如只获取title-> api_name value-> login的用例的所有数据
        :param t: 指定title
        :param value: 指定列中指定value
        :return: 读取指定列中指定value的用例的所有数据 list-object
        """
        # 打开工作簿
        self.open()
        # 按行获取数据转换成列表
        rows_data = list(self.sheet.rows)

        # 获取表单的表头信息
        titles = []
        for title in rows_data[0]:
            # 对title是否为空进行过滤，容错机制
            if title.value:
                titles.append(title.value)

        # 获取title对应的列
        title_column = titles.index(t)

        # 定义一个空列表用来存储所有的用例
        cases = []
        # 从第2行开始，就是测试用例数据了
        for case in rows_data[1:]:
            # 过滤数据 只读取指定api_name的数据
            # 判断每行的第4个数据(api_name) 不是指定的api_name 就跳过本次循环 达到不读取不存储非指定api_name的数据的效果
            if case[title_column].value != value:
                continue
            # data用例临时存放每行的用例数据
            data = []
            for cell in case:
                if cell.value:
                    data.append(cell.value)
            else:
                pass
            # 在组装之前 筛选api_name的测试用例数据
            # if api_name in data:
            # 将title与测试用例数据组合，形成每行测试用例,一行行读取数据，无需加list
            case_data = zip(titles, data)
            # 创建一个Case类的对象，用来保存用例数据，
            case_obj = Case(case_data)
            # 将该条数据放入cases中
            cases.append(case_obj)
        # 关闭工作簿,并返回读取的数据-->list
        self.close()
        return cases

    def write_data(self, row, column, value):
        # 打开工作簿
        self.open()
        output_log.info(f'正在写入数据, row--> {row}, column--> {column}, value--> {value}')
        # 指定位置写入数据
        self.sheet.cell(row=row, column=column, value=value)
        # 保存数据
        self.wb.save(self.file_path)
        # 关闭工作簿
        self.close()


if __name__ == '__main__':

    import os
    from api_automation_ebuy.common.constant import DATA_DIR

    # wb = ReadExcel(os.path.join(DATA_DIR, 'demo.xlsx'), "login")
    # # 先拿到要修改的数据 如excel的第一条数据
    # case = wb.read_line_data()[0]
    # # 获取要修改的字段对应的值    {'headers': $time}
    # data = case.headers
    #
    # # 获取当前时间
    # time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    # # 将$time替换获取的当前时间
    # data = data.replace('$time', time_now)
    # # 将数据回写到excel
    # wb.write_data(row=2, column=1, value=data)

    # wb = ReadExcel(os.path.join(DATA_DIR, 'api_automation_course.xlsx'), "login")
    # cases = wb.read_line_data_by_api_name('login')
    # for case in cases:
    #     print(case.title, case.api_name)

    wb = ReadExcel(os.path.join(DATA_DIR, 'api_automation_course.xlsx'), "login")
    # cases = wb.read_line_data_by_column_value(column=5, value='GET')
    # for case in cases:
    #     print(case.case_id)

    # cases = wb.read_line_data_by_title_value('title', '新增项目')
    # for case in cases:
    #     print(case.case_id, case.title)
    #
    # wb.write_data(row=10, column=10, value='ttt')

    cases = wb.read_line_data()
    # print(cases)
    for case in cases:
        print(case.case_id, case.title, case.request_data, type(case.request_data))

    # wb.write_data(row=10, column=10, value='测试')


