import os
import pyarrow.parquet as pq


def convert_parquet_to_csv(parquet_file_path, csv_file_path):
    """
    将 Parquet 文件转换为 CSV 文件，解决中文乱码问题
    :param parquet_file_path: 输入 Parquet 文件路径
    :param csv_file_path: 输出 CSV 文件路径
    """
    try:
        # 1. 读取 Parquet 文件
        table = pq.read_table(parquet_file_path)
        # 2. 转换为 Pandas DataFrame
        df = table.to_pandas()

        # 3. 确保输出目录存在
        output_dir = os.path.dirname(csv_file_path)
        os.makedirs(output_dir, exist_ok=True)

        # 4. 写入 CSV 时指定编码（关键！解决乱码）
        #    utf-8-sig：带 BOM 头，让 Excel 正确识别 UTF-8 编码
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

        print(f"✅ 转换成功！文件已保存至：{csv_file_path}")

    except Exception as e:
        print(f"❌ 转换失败：{e}")


if __name__ == "__main__":
    # 定义根目录下的 data 文件夹（自动适配项目路径）
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    # 输入和输出文件路径
    input_parquet = os.path.join(data_dir, 'input2.parquet')
    output_csv = os.path.join(data_dir, 'output2.csv')

    # 执行转换
    convert_parquet_to_csv(input_parquet, output_csv)