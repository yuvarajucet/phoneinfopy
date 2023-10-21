import requests
from pprint import pprint
import json
import random
import argparse

def main():
    parser = argparse.ArgumentParser(usage="\n Phoneinfo.py -i [number] (Command to search phone number)")
    parser.add_argument("-l","--login", metavar="string", dest="loginNumber", help="Login into truecaller [7892xxxxxx]")
    parser.add_argument("-c", "--countrycode", metavar="string", dest="code", help="Country code [+91]")
    parser.add_argument("-i", "--info", metavar="string", dest="targetNumber", help="Phone number to search [98xxxxxxxx]")

    args = parser.parse_args()

    if args.loginNumber and args.code:
        phone_number = args.code + args.loginNumber
        register_phone_number(phone_number, True)

    elif args.targetNumber and args.code:
        get_phone_info(args.targetNumber, args.code, None, True)

    elif args.loginNumber or args.targetNumber or args.code:
        print("[+] Please use like this : phoneinfo.py -l 98xxxxxxxx -c +91")
    
    else:
        print("[+] please use phoneinfo -h")



# Truecaller API handlers

def register_phone_number(phoneNumber, isCLI = False):
    NUMS = '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    LETTS = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    json = {'countryCode':'','dialingCode':None,'installationDetails':{'app':{'buildVersion':5,'majorVersion':11,'minorVersion':75, 'store':'GOOGLE_PLAY'},'device':{'deviceId':''.join(random.choices(NUMS+LETTS, k=16)),'language':'en','manufacturer':'Xiaomi','mobileServices':['GMS'],'model':'M2010J19SG','osName':'Android','osVersion':'10','simSerials':[''.join(random.choices(NUMS, k=19)), ''.join(random.choices(NUMS, k=20))]},'language':'en','sims':[{'imsi':''.join(random.choices(NUMS, k=15)),'mcc':'413','mnc':'2','operator':None}]},'phoneNumber':phoneNumber,'region':'region-2','sequenceNo':2}
    headers = {'content-type':'application/json; charset=UTF-8','accept-encoding':'gzip','user-agent':'Truecaller/11.75.5 (Android;10)','clientsecret':'lvc22mp3l1sfv6ujg83rd17btt'}

    try:
        response = requests.post('https://account-asia-south1.truecaller.com/v2/sendOnboardingOtp', headers=headers, json=json)
        requestId = response.json()["requestId"]
        if not isCLI:
            if response.json()['status'] == 1 or response.json()['status'] == 9:
                return {
                    "status": True,
                    "message": f"Sent an OTP for {phoneNumber}",
                    "requestId": requestId
                }
            else:
                return {
                    "status": False,
                    "message": response.json()['message'],
                    "requestId": None
                }
        #  For CLI users
        else:
            if response.json()['status'] == 1 or response.json()['status'] == 9:
                otp = str(input("\n[+] Please Enter OTP ==>  : "))
                otp_validate_status = validate_OTP(phoneNumber, otp, requestId, True)
                if otp_validate_status:
                    pass
                else:
                    print("\n[-] Please try again!")

            else:
                print("\n [-] Failed to sent OTP!\n [-] Reason: "+ response.json()["message"])

    except Exception as ex:
        if not isCLI:
            return {
                "status": False,
                "message": "Failed to send OTP! Exception occured : " + str(ex),
                "requestId": None
            }
        else:
            print("\n[-] Exception occured : Exception ==> "+ str(ex))

def validate_OTP(phoneNumber, OTP, requestId, isCLI = False):
    json = {
            'countryCode':'',
            'dialingCode':None,
            'phoneNumber':phoneNumber,
            'requestId': requestId,
            'token':OTP
        }

    headers = {
        'content-type':'application/json; charset=UTF-8',
        'accept-encoding':'gzip',
        'user-agent':'Truecaller/11.75.5 (Android;10)',
        'clientsecret':'lvc22mp3l1sfv6ujg83rd17btt'
    }

    try:
        response = requests.post('https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp', headers=headers, json=json)

        if response.json()['status'] == 11:
            if isCLI:
                print("\n[-] OTP Code is Invalid")
                return False
            else:
                return {
                    "status": False,
                    "message": "OTP code is Invalid"
                }
        
        elif response.json()['status'] == 2 and response.json()['suspended']:
            if isCLI:
                print("\n[-] Oops!.. Your account got suspended. Try another number :(")
                return False
            else:
                return {
                    "status": False,
                    "message": "Opps!... Your account got suspended. Try another number :("
                }
        else:
            if isCLI:
                with open(".token", "w") as file:
                    file.write(response.json()["installationId"])
                print("\n[+] Validation success!")
                return True

            else:
                return {
                    "status": True,
                    "message": "Validation success!",
                    "access_token": response.json()["installationId"]
                }
        
    except Exception as ex:
        if isCLI:
            print("\n[-] Exception occurred : ==> " + str(ex))
        else:
            return {
                "status": False,
                "message": "Failed to validate OTP! Exception : "+ str(ex)
            }

def get_phone_info(phoeNumber, countryCode, authToken, isCLI = False):
    if authToken == None and isCLI:
        with open(".token", "r") as file:
            data = file.read()
            authToken = data

    if authToken == None or authToken == "":
        print("[-] Please Login and try again!")
        return 0

    params = {
        'q':phoeNumber,
        'countryCode':countryCode,
        'type':'4',
        'locAddr':'',
        'placement':'SEARCHRESULTS,HISTORY,DETAILS',
        'encoding':'json'
    }

    headers = {
        'content-type':'application/json; charset=UTF-8',
        'accept-encoding':'gzip',
        'user-agent':'Truecaller/11.75.5 (Android;10)',
        'clientsecret':'lvc22mp3l1sfv6ujg83rd17btt',
        'authorization':'Bearer ' + authToken
    }

    try:
        response = requests.get("https://search5-noneu.truecaller.com/v2/search", headers=headers, params=params)

        if not isCLI:
            if response.json().get('status'):
                return {
                    "status": False,
                    "message": "Failed to get user info"
                }
            else:
                return {
                    "status": True,
                    "message": "User details found",
                    "data": json.loads(response.content)
                }

        else:
            if response.json().get('status'):
                print("\n[+] Failed to get user data")
            else:
                with open(".data","w") as file:
                    json.dump(response.json(), file, indent=4)
                with open(".data", "r") as file:
                    data = json.load(file)
                pprint(data)

    except Exception as ex:
        if isCLI:
            print("[-] Exception occurred : ==> "+ str(ex))
        else:
            return {
                "status": False,
                "message": "Failed to get user details, Exception : "+ str(ex)
            }
        

if __name__ == "__main__":
    main()