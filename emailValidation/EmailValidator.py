import socket, smtplib, re, dns.resolver, requests
import pandas as pd
from verify_email import verify_email  # third party verification library
import time
from D_Mart.db_connect import DATABASE as MONGO_DATABASE


class EmailProcess:

    def __init__(self, email=None, status_type=None, task_export_id=None,
                 code=None):
        self.addressToVerify = email
        print("Checking...", email)

        self.status_type = status_type
        self.task_export_id = task_export_id
        self.code = code

    def checkEmail(self):
        try:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                             self.addressToVerify)
            if match is None:
                # return False
                return {
                    'task id': self.task_export_id,
                    'email': self.addressToVerify,
                    "type": "",
                    "status": "false",
                    "message": "match is None",
                    "code": "",
                }
            else:
                domain_name = self.addressToVerify.split('@')[1]
                records = dns.resolver.resolve(domain_name, 'MX')
                mxRecord = records[0].exchange
                mxRecord = str(mxRecord)
                host = socket.gethostname()
                server = smtplib.SMTP(timeout=60)
                server.set_debuglevel(0)
                server.connect(mxRecord)
                server.helo(host)
                server.mail('me@domain.com')
                code, message = server.rcpt(str(self.addressToVerify))
                server.quit()
                # print("Message ::", message.decode('utf-8'))
                # print("Code ::", str(code))
                if str(message) == """b'2.1.5 Recipient OK'""":
                    print("A1")
                    # return False
                    return {
                        'task id': self.task_export_id,
                        'email': self.addressToVerify,
                        "type": "red",
                        "status": "false",
                        "message": message.decode('utf-8'),
                        "code": str(code),
                    }
                else:
                    if code == 250:
                        return {
                            'task id': self.task_export_id,
                            'email': self.addressToVerify,
                            "type": "green",
                            "status": "true",
                            "message": message.decode('utf-8'),
                            "code": str(code)
                        }
                        # self.final_list.append(mydict)
                    else:
                        print("A2")
                        # return False
                        return {
                            'task id': self.task_export_id,
                            'email': self.addressToVerify,
                            "type": "yellow",
                            "status": "false",
                            "message": message.decode('utf-8'),
                            "code": str(code)
                        }
        except Exception as e:
            print("A3")
            # return False
            return {
                'task id': self.task_export_id,
                'email': self.addressToVerify,
                "type": "orange",
                "status": "false",
                "message": str(e),
                "code": ""
            }

    def third_party_verification(self):
        status_type = self.status_type
        timeout = time.time() + 60 * 2  # 5 minutes from now
        if status_type != 'green':
            email = row['email']
            # print("email ::", email)
            if time.time() > timeout:
                Value = verify_email(email)
                row.update({"thrid_party_verify": Value})
            else:
                row.update({"thrid_party_verify": "false"})

        elif status_type == 'green':
            row.update({"thrid_party_verify": "true"})

        return row

    def final_result(self):

        status_type = self.status_type
        code = row['code']
        prefix = "http://"
        email = row['email']
        url = prefix + email.split('@')[1]
        print('checking url: ', url)
        row.update({'Http status code': ''})

        if status_type == 'green' and code == '250':
            row.update({'final status': 'verified'})
            # row.update({'domain_active': ''})

        elif status_type == 'red' and code == '250':
            row.update({'final status': 'extrapolated'})

            try:
                res = requests.get(url, timeout=10.0)
                result = res.status_code
                print(result)
                row.update({'Http status code': result})

                if str(result) == '200':
                    row.update({'domain_active': 'True'})
                elif str(result) == '':
                    row.update({'domain_active': 'False'})
                else:
                    row.update({'domain_active': 'False'})

            except requests.Timeout as err:
                print(err.strerror)
            except requests.RequestException as errs:
                print(errs.errno)

        else:
            row.update({'final status': 'not verified'})
            # row.update({'domain_active': ''})

        return row


def export_runner(task_export_id, email_file_path):
    final_list = []
    db_obj = MONGO_DATABASE()

    global row
    df = pd.read_csv(email_file_path)
    df = df.dropna(how='any', subset=['email'], axis=0)
    for ins, i in df.iterrows():
        row = dict(i)

        email = row['email']
        # print("*"*50)

        EmailProcess_obj = EmailProcess(

            email=email,
            task_export_id=task_export_id
        )
        result = EmailProcess_obj.checkEmail()
        final_list.append(result)

    # print("final_list ::", final_list)

    fdf = pd.DataFrame(final_list)

    final_list_third_party = []
    for ins, i in fdf.iterrows():
        row = dict(i)
        status_type = row['type']
        # print("status_type ::", status_type)
        email = row['email']
        EmailProcess_obj = EmailProcess(

            email=email,
            status_type=status_type,
            task_export_id=task_export_id
        )

        third_party_obj = EmailProcess_obj.third_party_verification()
        final_list_third_party.append(third_party_obj)

    final_verified_list = []
    ndf = pd.DataFrame(final_list_third_party)

    for ins, i in ndf.iterrows():
        row = dict(i)
        status_type = row['type']
        code = row['code']
        EmailProcess_obj = EmailProcess(

            email=email,
            status_type=status_type,
            task_export_id=task_export_id,
            code=code
        )
        final_result_obj = EmailProcess_obj.final_result()
        final_verified_list.append(final_result_obj)
        db_obj.email_validation_exports.insert_one(final_result_obj)

    print("final_list_result : ", final_verified_list)
    db_obj.client.close()

    print("File generated done .. !")
