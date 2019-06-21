import random
import os
import configparser
import Operation_system_path as ops


def main():
    # read config file with local path
    config = configparser.ConfigParser()
    config_file = ops.get_local_path('ConfigFile.ini')
    config.read(config_file)
    file = ops.get_local_path(config['FILES']['RAW_DATA'])
    data_file = ops.get_local_path(config['FILES']['DATA_FILE'])
    with open(data_file, "w") as d_file:
        with open(file) as raw_data_file:
            for line in raw_data_file:  # read rest of lines
                clean_line = ' '.join(line.split())   # join multiple spaces into one
                clean_line = clean_line.replace(' ', '\t')  # replace spaces with tab
                clean_line = clean_line.replace('"', '')    # remove '"' from string
                clean_line = clean_line + "\n"
                d_file.write(clean_line)
        raw_data_file.close()
    d_file.close()


if __name__ == "__main__":
    main()
