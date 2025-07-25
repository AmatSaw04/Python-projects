#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp


with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()


placeholder  = "[name]"

with open("./Input/Letters/starting_letter.txt", mode= "r") as text:
    place = text.read()

    for name in names:
        strip_name = name.strip()
        new_letter = place.replace(placeholder, strip_name)

        with open(f"./Output/ReadyToSend/invited_{strip_name}.txt", mode="w") as complete_letter:
            complete_letter.write(new_letter)
            print(complete_letter)


