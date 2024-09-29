'''
pattern:
sy otp totp:sha1:base32:WZWAD7BYIBWZTFZ57PFGJNU5T4:sy:xxx *
'''
import time

from User import User
import os
import shutil


class UserSecretFile:
    filename = None

    def __init__(self, filename):
        self.filename = filename
        print(f'{self.filename}: ')

    def show(self):
        pwd = os.curdir

        with open(self.filename, 'r') as f:
            lines = f.readlines()
            print(lines)

    def search_user(self, user):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            user_line = None
            for l in lines:
                if l is None or l.strip() == '':
                    continue
                else:
                    # print(f'read line: {l}')
                    arr = l.split(r' ')
                    if arr[0] == user:
                        print(f'user {user} found')
                        user_line = l
                        break
                    print(arr)

            if user_line is None:
                print(f'user {user} not found !!!!')
                return None
            else:
                user = User.new_from_text(user_line)
                print(f'user {user} found.  {user}')
                return user
            # print(lines)

    def change_password(self, username, old_password, new_password):

        # check new password
        err = User.check_password_rule(new_password)
        if err is not None:
            return False, err

        # 遍历文件，查找账号并修改密码，存入contents列表；
        # 备份文件；
        # contents列表内容写入新文件；
        contents = []
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if l is None or l.strip() == '':
                    continue
                else:
                    # print(f'read line: {l}')
                    arr = l.split(r' ')
                    if arr[0] == username:
                        # 修改密码
                        user = User.new_from_text(l)
                        # print(f'user {otp_user.user_to_line()} found. new_password={new_password}')
                        if user.passwd != old_password:
                            return False, '用户名密码错误'
                        user.passwd = new_password
                        # new_line = f'{otp_user.user} otp totp:sha1:base32:{otp_user.secret}:{new_password}:xxx *\n'
                        new_line = user.user_to_line()
                        contents.append(new_line)
                    else:
                        # 原样输出
                        contents.append(l)
                    # print(arr)

        lock_result = self.lock_file()
        if lock_result:
            try:
                # backup file
                bak_file = f'{self.filename}_bak'
                print(f'change_password. backup filename is {bak_file}')
                if os.path.exists(bak_file):
                    print(f'change_password. remove old bak file. {bak_file}')
                    os.remove(bak_file)
                # print(f'change_password. rename {self.filename} {bak_file}')
                # os.rename(self.filename, bak_file)
                print(f'change_password. copyfile {self.filename} {bak_file}')
                shutil.copyfile(self.filename, bak_file)
                print(f'change_password. write file {self.filename}')
                with open(self.filename, 'w') as f2:
                    f2.writelines(contents)
            finally:
                print(f'un_lock_file')
                self.un_lock_file()
        else:
            print(f'lock file failed')
            return False, '其它进程正在更新密码文件，请稍后再试'

        return True, 'ok'

    def lock_file(self):
        lockfile = f'{self.filename}.lock'
        retry_cnt = 5
        while os.path.exists(lockfile):
            print(f'warn. lockfile {lockfile} exist. wait for release. retry_cnt={retry_cnt}')
            retry_cnt = retry_cnt - 1
            if retry_cnt <= 0:
                print(f'failed. lockfile {lockfile} exist.')
                return False
            time.sleep(1)
        print(f'create lock file {lockfile}')
        f = open(lockfile, 'w')
        f.close()
        return True

    def un_lock_file(self):
        lockfile = f'{self.filename}.lock'
        if os.path.exists(lockfile):
            print(f'remove lock file {lockfile}')
            os.remove(lockfile)


def test_lock():
    filename = 'user_secret_file'
    f = UserSecretFile(filename)
    f.show()

    print(f'lock_file')
    lock_result = f.lock_file()
    if lock_result:
        try:
            # do something
            pass
        finally:
            print(f'un_lock_file')
            f.un_lock_file()
    else:
        print(f'lock file failed')


def test():
    filename = 'user_secret_file'
    f = UserSecretFile(filename)
    f.show()
    res = f.change_password('bbbb', '1234', '22222')
    f.show()
    return res


if __name__ == '__main__':
    res = test()
    print(f'res: {res}')
