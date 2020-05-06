#!/usr/bin/python3
import os
import re
import sys
import subprocess


versions = []


def success_message(string):
    print('\n\033[92m %s \033[0m \n' % (string))


def error_message(string):
    print('\033[91m %s \033[0m \n' % (string))


def runCommand(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, shell=True)
        while(True):
            retcode = process.poll()
            yield process.stdout.readline()
            if retcode is not None:
                break
    except Exception as e:
        error_message(str(e))
        exit()


def get_current_version():
    match = re.search(r"^PHP\s+(.+?)\-.+?",
                      str(subprocess.check_output('php -v', shell=True).decode('utf-8')))
    if match:
        return match.group(1)
    else:
        return ''


def get_versions():
    global versions

    if len(versions) == 0:
        for response in runCommand('sudo update-alternatives --list php'):
            search = re.search(r"php([0-9]\.?([0-9])?)",
                               response.decode('utf-8'))
            if search:
                versions.append(search.group(1))
    return versions


def show_versions():
    print("Existing versions\n\n")
    for version in get_versions():
        print(" [%s]" % (version))


def switch_version(switcher_version=False):
    while True:
        if not switcher_version:
            print("----------------------------------------")
            version = input(' version :')
            print("----------------------------------------")
        else:
            version = switcher_version

        if version in get_versions():
            try:
                os.system(
                    "sudo update-alternatives --set php /usr/bin/php"+version)
                os.system(
                    "sudo update-alternatives --set phar /usr/bin/phar"+version)
                os.system(
                    "sudo update-alternatives --set phar.phar /usr/bin/phar.phar"+version)
                os.system(
                    "sudo update-alternatives --set phpize /usr/bin/phpize"+version)
                os.system(
                    "sudo update-alternatives --set php-config /usr/bin/php-config"+version)
                print("----------------------------------------")
                os.system('php -v')
                success_message('Selected version '+version)
            except Exception as e:
                error_message('Error! Something went wrong :(')
                error_message('Error message:'+str(e))
                exit()
            finally:
                break
        else:
            error_message("Please select the correct version\n")
            if switcher_version:
                exit()


def run():
    try:
        switch_version(sys.argv[1])
    except IndexError:
        show_versions()
        switch_version()
        print("Running php version: %s \n\n" % (get_current_version()))


try:
    run()
except KeyboardInterrupt:
    success_message('Bye')
    exit()
