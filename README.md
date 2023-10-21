# PhoneInfopy

PhoneInfopy is a python tool to directly make request to Truecaller API's and get response. This module will allow you to register your number, validate OTP while registering and search information about a phone number.

**Table to Contents**
- [PhoneInfoPy](#PhoneInfoPy)
    - [Requirements](#requirements)
    - [Command Line Usage](#Command-line)
        - [Installation](#Install)
        - [Login](#Login)
        - [Search Number](#search-number)
    - [Module usage](#Module-usage)
        - [Installation](#install)
        - [Register](#register)
        - [Validate OTP](#OTP-validation)
        - [Search phone number](#Search-number)

## Requirements
To use PhoneInfopy module you need below pre requirements.
- valid mobile number
- python
- truecaller auth token [This token will get by login/register process]

## Command Line usage
You can install PhoneInfopy package using pip

- `phoneinfopy -h [--help]` for help
- `phoneinfopy -l [--login]` for login [Need to mention country code]
- `phoneinfopy -c [--code]` for country code
- `phoneinfopy -i [--info]` for search mobile number [Need to mention country code]

### Installation
```bash
pip install phoneinfopy
```

### Login
```bash
phoneinfopy -c <countryCode> -l <phoneNumber>
```
#### Example
```bash
phoneinfopy -c +91 -l 98xxxxxxxx
```

## Search Number
You can search phone number by using below command
```bash
phoneinfo -c +91 -i 98xxxxxxxx
```

## Module usage:
You can install the phoneinfopy moudle using pip:
```bash
pip install phoneinfopy
```

## Register
```python
from phoneinfopy import register_phone_number

number = "+9198xxxxxxxx"
response = register_phone_number(number)

# register_phone_number method will return json object
# example:
# {
#   status : bool,
#   message: str
#   requestId: str
# }
```

## Validate OTP:
Once you get success response from register method next you need to verify the OTP to get access token.


```python
from phoneinfopy import validate_OTP

number = "+9198xxxxxxxx"
OTP = "123456"
requestId = "<you get this ID while register process>"
response = validate_OTP(number, OTP, requestId)

# validate_OTP method will return json object
# {
#   status: bool
#   message: str
#   access_token: str  [If OTP validatino is success]
# }
```

## Search Phone Number
You need to get user information using phone number you can use like this..
```python
from phoneinfopy import get_phone_info

target_number = "98xxxxxxxx"
country_code = "+91"
access_token = "a10--******" ["you get this token while validating OTP"]

response = get_phone_info(target_number, country_code, access_token)

# get_phone_info will return json object 
#{
#   status: bool
#   message: str
#   data: object [if user info found]
# }
```

## Contribution

Contributions to the phoneinfopy package are welcome!...
If you faced any issue or you have good idea to improve please open a issue or submit a pull request.

## Let's Connect:
- [Instagram](https://www.instagram.com/mr_3rr0r_501/)
- [LinkedIn](https://www.linkedin.com/in/yuvaraj-a-57a103171)
- [Youtube](https://youtube.com/@Mr3rr0r501)
