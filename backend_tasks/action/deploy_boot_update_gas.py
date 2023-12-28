import sys
sys.path.append('../../')

if __name__ == '__main__':
    cur_path = sys.path[0]
    print("Working Path is:", cur_path)

    exec_lines = []
    tmpl = open("%s/boot_update_gas.sh.tmpl" % cur_path, mode='r')
    while True:
        line = tmpl.readline()
        if not line:
            break
        exec_lines.append(line.replace("[CUR_PATH]", cur_path))
    tmpl.close()

    target_file = open("%s/boot_update_gas.sh" % cur_path, mode='w')
    target_file.writelines(exec_lines)
    target_file.close()

    print("Note: boot_update_gas.sh should be generated at that Path, ")
    print("please make it excuteable, such as chmod a+x boot_update_gas.sh. ")
    print("and then put it into crontab for periodically invoke!")
    print("Crontab eg: ")
    print("  */1 * * * * /working_path/boot_update_gas.sh > /dev/null")

