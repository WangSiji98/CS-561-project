

def output(path_list, output_file_name):
    output_file = open(output_file_name, 'w')
    for path_str in path_list:
        output_file.write(path_str)
        output_file.write('\n')
    output_file.close()



