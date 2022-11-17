import socket, smtplib, re, dns.resolver
import pandas as pd
from verify_email import verify_email  # third party verification library
import time
from .models import EmailValidations
from django.contrib.auth.models import User


class EmailProcess:

    def __init__(self, email=None, supplier_id=None, supplier_name=None, status_type=None):
        self.addressToVerify = email
        print("Checking...", email)
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.status_type = status_type

    def checkEmail(self):
        try:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                             self.addressToVerify)
            if match is None:
                # return False
                return {
                    'id': self.supplier_id,
                    'name': self.supplier_name,
                    'email': self.addressToVerify,
                    "type": "",
                    "status": "false",
                    "message": "match is None",
                    "code": ""
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
                        'id': self.supplier_id,
                        'name': self.supplier_name,
                        'email': self.addressToVerify,
                        "type": "red",
                        "status": "false",
                        "message": message.decode('utf-8'),
                        "code": str(code)
                    }
                else:
                    if code == 250:
                        return {
                            'id': self.supplier_id,
                            'name': self.supplier_name,
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
                            'id': self.supplier_id,
                            'name': self.supplier_name,
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
                'id': self.supplier_id,
                'name': self.supplier_name,
                'email': self.addressToVerify,
                "type": "orange",
                "status": "false",
                "message": str(e),
                "code": ""
            }

    def third_party_verification(self):
        status_type = self.status_type
        timeout = time.time() + 60 * 5  # 5 minutes from now
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


if __name__ == '__main__':
    model = EmailValidations
    final_list = []

    csv_file_path = f"/home/adarsh/D_Mart/media/files/{EmailValidations.input_file}.csv"
    df = pd.read_csv(csv_file_path)

    for ins, i in df.iterrows():
        row = dict(i)

        # supplier_id = row['id']
        # print("supplier_id ::", supplier_id)
        # supplier_name = row['name']
        # print("supplier_name ::", supplier_name)
        supplier_email = row['email']
        # print("email ::", supplier_email)
        # print("*"*50)

        EmailProcess_obj = EmailProcess(supplier_id=None, supplier_name=None, email=supplier_email)
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
        EmailProcess_obj = EmailProcess(supplier_id=None, supplier_name=None, email=email, status_type=status_type)
        third_party_obj = EmailProcess_obj.third_party_verification()
        final_list_third_party.append(third_party_obj)

    print("final_list_third_party : ", final_list_third_party)

    new_df = pd.DataFrame(final_list_third_party)
    new_df.to_csv(f"OutputFile-{EmailValidations.taskName}.csv")
    print("File generated done .. !")


