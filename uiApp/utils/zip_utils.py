import os
import zipfile


def get_zip_file(input_path, result):
    """
    对目录进行深度优先遍历
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


def zip_file_path(input_path, output_path, output_name):
    """
    压缩文件
    :param input_path: 压缩的文件夹路径
    :param output_path: 解压（输出）的路径
    :param output_name: 压缩包名称
    :return:
    """
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    file_lists = []
    get_zip_file(input_path, file_lists)
    for file in file_lists:
        f.write(file)
    # 调用了close方法才会保证完成压缩
    f.close()


def unzip_file(zip_file_name,output_dir):
    """
    解压文件
    :param zip_file_name: 压缩包名称
    :param output_dir: 输出地址
    :return:
    """
    # 查看文件是否存在
    if not os.path.exists(zip_file_name):
        return
    zf = zipfile.ZipFile(zip_file_name)
    for name in zf.namelist():
        name.replace('\\','/')
        if name.endswith('/'):
            if not os.path.exists(os.path.join(output_dir,name)):
                os.mkdir(os.path.join(output_dir,name))
        else:
            ext_filename = os.path.join(output_dir,name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir,mode=777)
            out_file = open(ext_filename,'wb')
            out_file.write(zf.read(name))
            out_file.close()