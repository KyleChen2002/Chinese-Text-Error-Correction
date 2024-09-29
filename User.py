
class User:
    user = None
    type = 'otp'
    passwd = None
    secret = None

    @staticmethod
    def new_from_text(s):
        otpUser = User()

        arr1 = s.split(' ')
        otpUser.user = arr1[0]
        otpUser.type = arr1[1]
        part3 = arr1[2]
        part4 = arr1[3]

        arr2 = part3.split(':')
        otpUser.secret = arr2[3]
        otpUser.passwd = arr2[4]

        # print(f'from_text. user: {otpUser.user}, type: {otpUser.type}, passwd: {otpUser.passwd}, secret: {otpUser.secret}')

        return otpUser

    def from_text(self, s):
        arr1 = s.split(' ')
        self.user = arr1[0]
        self.type = arr1[1]
        part3 = arr1[2]
        part4 = arr1[3]

        arr2 = part3.split(':')
        self.secret = arr2[3]
        self.passwd = arr2[4]

        # print(f'from_text. user: {self.user}, type: {self.type}, passwd: {self.passwd}, secret: {self.secret}')

    @staticmethod
    def check_password_rule(password):
        err_msg = '密码规则： 4~20字符，不能包含冒号、回车换行'
        # length 4 ~ 20
        if len(password) < 4 or len(password) > 20:
            return err_msg
        # not contain \n :
        if ':' in password or '\n' in password:
            return err_msg

    def user_to_line(self):
        new_line = f'{self.user} otp totp:sha1:base32:{self.secret}:{self.passwd}:xxx *\n'
        return new_line
