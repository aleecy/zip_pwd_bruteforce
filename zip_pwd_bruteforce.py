import zipfile # to unzip
import string # to encode the password string (I still don't understand why we had to do that)
import os # to navigate through the files
import zlib # I had to import this library as the cracking operation was producing a "zlib.error" that I couldn't "except" without loading this library

pwd_path = os.path.join("Passwords")
zip_path = os.path.join("ZippedFiles")
loot_path = os.path.join("Loot") # For more clarity, I decided to create a Loot folder where I will extract all the cracked zipfiles and store the found password in a txt file
pwddecrypt = "" # variable that will store the value of the password list file to use
success = "y" # condition used to loop

def pwdlist(): # select the password list you want to use
        
        for root, dirs, files in os.walk(pwd_path):
                for filename in files:
                        current_pwd_path = os.path.join(root, filename)
                        print(current_pwd_path) # print the available lists
                selection = input("What Password list would you like to use (enter full name and don't forget the .txt)\n")
                while os.path.isfile(pwd_path+"/"+selection) == False:
                    selection = input("This file doesn't exist or has been incorrectly written, please try again\n")
                pwdfile = open(pwd_path+"/"+selection)
                pwdread = pwdfile.read()
                pwddecrypt = pwdread.split("\n")
                return pwddecrypt # return the path of the password list to be used outside of the function
                pwdfile.close()

def ziplist(): #select the zipfile you want to crack
        for root1, dirs1, files1 in os.walk(zip_path):
                for zfile in files1:
                        current_zip_path = os.path.join(root1, zfile)
                        print(current_zip_path) # print the list of zip files available
                selectedzip = input("What Zip file would you like to crack ? (enter full name and don't forget the .zip)\n")
                while os.path.isfile(zip_path+"/"+selectedzip) == False:
                    selectedzip = input("This file doesn't exist or has been incorrectly written, please try again\n")
                zip2crack = os.path.join(zip_path, selectedzip)
                return zip2crack # return the path of the zipfile to crack outside the function
                
def crackit(pwddecrypt, zip2crack): # function that uses the 2 variables previously selected
        print("Let's try to crack it :")
        finalzip = zipfile.ZipFile(zip2crack) # open the zipfile
        stored = "2" # variable used as a condition to verify if the password has been cracked, hopefully the cracked password will not be "2" otherwise... 
        for passw in pwddecrypt: # extract all the passwords available
                passwencode = passw.encode("cp850", "replace") # encode them the right way ... why ???
                print(passw)
                try: # exception handling, used with "except" allows us not to break the program
                        finalzip.extractall(path=loot_path,pwd=passwencode) # extract the zipfile using the given password
                        print("Password found ! : " + str(passw))
                        stored = passw
                        collected_pwd = open(loot_path+"/collected_password.txt", "a") # store the password in an external txt file
                        collected_pwd.write("The Password for " + str(zip2crack) + " is " + str(stored) +"\n")
                        collected_pwd.close()
                        break                                
                except (RuntimeError, zlib.error): # RuntimeError is to prevent wrong passwords, zlib.error was needed as I encountered this error for a reason I don't get by now
                        print("Wrong Password")
        if stored != "2":
                print("Files have been extracted in the \"Loot\" folder")
                print("Password has been written in the \"Loot/collected_password.txt\"")
                print("Enjoy !")
                success = input("Press \"y\" to crack another zipfile or press another key to exit\n")
                if success != "y":
                        print("Bye !")
                return success
        else:
                print("It didn't work...")
                success = input("Press \"y\" to try another combo or press another key to exit\n")
                if success != "y":
                        print("Bye !")
                        print("PS : Don't forget to promote the rookie that coded this :)")
                return success

while success == "y":
        pwddecrypt = pwdlist()
        zip2crack = ziplist()
        success = crackit(pwddecrypt, zip2crack)

# Improvements possible : 
# Create a "Hail Mary" option that will use all the available lists and/or crack all/one file(s) at the same time 
# Being able to write the exact path of both files if the script is not located in the correct folder
# Find a different condition value than "2" in order to avoid a conflict if the real password is "2" but probabilities are low
# Add an os.walk to display the extracted files
# Create the folder/file that will store the password if it doesn't exist or has been inadvertently deleted ? How ?