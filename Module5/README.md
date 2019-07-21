# Module 5 - passChecker

Simple password checker that relies on the entropy of the password rather than complex rules.
It will also check to see if the password has appeared in past breaches and warn the user if so.
The zxcvbn library gives feedback on the password based on databases of top password, dictionary words,
	names, etc.  The database it uses can be extended for more specific purposes if needed.

## Tested With:

- Python 2 and 3
- Windows 10 OS

## Requirements:

- Python 2 or 3
- password_strength, zxcvbn, requests

## Usage:

```bash
python passChecker.py
```

## Current Limitations:

- Only uses the default database of zxcvbn.
- Doesn't allow for specific password requirements to be specified.

## Future Work:

- Allow for a password policy to be set (required length/length limitation, capitals, etc)
- Allow for custom items to be added to what is checked by zxcvbn.
- Could be implemented as a browser extention for quick password checking.
- Could include checking of emails from haveibeenpwned in addition to passwords.
