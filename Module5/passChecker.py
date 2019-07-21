#Simple password checker that relies on the entropy of the password rather than complex rules.
#It will also check to see if the password has appeared in past breaches and warn the user if so.
#The zxcvbn library gives feedback on the password based on databases of top password, dictionary words,
#	names, etc.  The database it uses can be extended for more specific purposes if needed.

#https://pypi.org/project/password-strength/
#https://github.com/dwolfhub/zxcvbn-python
#https://haveibeenpwned.com/API/v2

import getpass
import hashlib
import requests
from password_strength import PasswordStats
from zxcvbn import zxcvbn
	
	#Get the password that the user wants to check.
	#getpass will allow the password to be entered in a discrete
	#	manner, without the characters/length/etc being shown.
print('Please enter the password you would like to check.')
print('The password will not be stored outside of this program.')
pword = getpass.getpass('Password: ')


	#Convert the password into its sha-1 hash and then its hexform to be checked via the
	#	haveibeenpwned API.
	#We make it uppercase for each comparison with the responses we get back.
phash = hashlib.sha1(bytes(pword, encoding='utf-8'))
phash = phash.hexdigest().upper()

	#First thing is to check if the password has been found in a breach before.
	#If it has been found, then it would likely be better to not use it.
hibp = 'https://api.pwnedpasswords.com/range/'

	#One part of what we get back is how many times a hash was found in a breach
foundNum = 0

	#We check haveibeenpwned's password list using just the first 5 digits of the
	#	sha-1 version of the password.
	#This ensures the entire password hash isn't ever sent, because we will only get
	#	the other characters of matching hashes back.
	#We have to include a User Agent (in this case, our program) to use the API.
check = requests.get(hibp + phash[:5], headers={'User-Agent':'passChecker'})
	
	#Status code 200 means we got a proper response from haveibeenpwned.
	#Per the API, we should always get back 200 when checking for passwords assuming the
	#	URL request was formatted correctly with our User Agent.
	#The hash we get back does not include the first 5 digits we sent to the API.
if check.status_code == 200:
		
		#Treat the data we got back as text data
	data = check.text
	
		#We will split up the data we get back into individual lines.
		#Each line will contain a single hash and the number of breaches it was found in.
	data = data.splitlines()
	
		#Check each line of our data
	for line in data:
		#If we find a match, then make note of how many times it was found.
		if line[0:35] == phash[5:]:
			foundNum = line[36:]
	
	#Now we have gone through all of the hashes returned and seen if we found a match.
		
	#If for some reason we did not get a status code of 200, we will print an error message and the
	#	status code we actually got back.
	#In most situations this will not occur.
else:
	print('Error contacting haveibeenpwned. Received status code of: ' + check.status_code)
	
#Now we will check the 'strength' of the password.
	
	#Make a rating based on the entropy strength of the password.
	#A judgement based on the strength is given as part of the feedback below.
strength = PasswordStats(pword).strength()

	#Just printing a break before we start giving results.
print('\n'+'='*20+'\n')

	#Using the zxcvbn library, we get some stats for the password.
	#We will be using the time it would take the crack the password
	#	in different situations and the feedback that is provided by it.
	#Additionally, we will use the entropy strength calculated earlier and
	#	the number of breaches the password was found in here to give additional
	#	feedback on the given password.
results = zxcvbn(pword)
	
	#Start going through all the key:value pairs returned to us.
	#We will format the output to make it a bit easier to read and digest.
for key,value in results.items():
		
		#The feedback key includes warnings and suggestions related to the given password.
		#If there is more than one value for a piece of the feedback section, we will break that up.
		#We check to see if the value in our feedback in a string, meaning we only have one item, 
		#	or if not then we get a list of several items.
	if key is 'feedback':
		print('Feedback for checked password:')
		for k,v in value.items():
			if len(v) > 0:
				print('\t', end='')
				print(str(k).capitalize())
			if isinstance(v, str):
				print('\t\t'+str(v))
			else:
				for item in v:
					print('\t\t'+str(item))
				
					
			#In addition to the feedback from zxcvbn, we will add some extra based on the
			#	entropy complexity from earlier.
			#Per the library, stronger passwords start at a 0.66 value.
		print('\tStrength of your password based on complexity: ')
		if strength <= 0.33:
			print('\t\tYour password is not complex enough.')
		elif strength <= 0.66:
			print('\t\tYour password is fairly complex, but could be better.')
		else:
			print('\t\tYour password is quite complex.')
		
			#Assuming we got information from haveibeenpwned, then we print the number of breaches it was found in.
		if check.status_code is 200:
			print('\tThis password was found in '+str(foundNum)+' breaches.')
			
			#We will also use our result from haveibeenpwned here.
			#If our count isn't 0, then we did find a match from haveibeenpwned.
		if foundNum is not 0:
			print('\t\tYou should reconsider using this password.')
	
		#Before the feedback, we will print out an estimate of how long it would take to
		#	crack the password in a more readable format.  The keys are swapped to something more
		#	understandable, and the times given in this section are based on units of time rather than
		#	more specific timings.
		#Also going to include the estimate of the number of guesses taken to crack the password here.
	elif key is 'crack_times_display':
		print('Time to potentially crack your password is: ')
		print('(Note: For a common password, this will be much faster.)')
		for k,v in value.items():
			print('\t', end='')
			if k is 'online_throttling_100_per_hour':
				print('Online cracking slowed by throttling (100 attempts per hour)')
			elif k is 'online_no_throttling_10_per_second':
				print('Online cracking with no throttling (10 attempts per second)')
			elif k is 'offline_slow_hashing_1e4_per_second':
				print('Offline cracking of a slow hashed password (1e4 attempts per second)')
			elif k is 'offline_fast_hashing_1e10_per_second':
				print('Offline cracking of a fast hashed password (1e10 attempts per second)')
			print('\t\t', end='')
			print(str(v))
		print('The number of guesses used to crack the password used would be roughly: ' + guessNum + ' for a non-common password.')
	
		#Grab the number of guesses that zxcvbn thinks it would take to get the password.
	elif key is 'guesses':
		guessNum = str(value)