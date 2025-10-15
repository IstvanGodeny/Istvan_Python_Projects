morse_letters = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', ' -.',
                 '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
morse_numbers = ['.----', '..---', '...--', '....-', '.....', '-.....', '--...', '---..', '----.', '-----']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
morse_sign = ['._._._', '__..__', '..__..', '_.__._', '_.__.', '.____.', '_._._.', '___...', '._.._.', '_...._',
              '_.._.']
signs = ['.', ',', '?', ')', '(', "'", ';', ':', '"', '-', '/']

print("This is a simple text to morse code converter. Just type the text and you will get the morse code of the text.")

input_text = input("Text: ").lower()
text = []
morse = []
for i in input_text:
    if i in letters:
        morse.append(morse_letters[letters.index(i)])
    elif i in numbers:
        morse.append(morse_numbers[numbers.index(i)])
    elif i in signs:
        morse.append(morse_sign[signs.index(i)])
    elif i == " ":
        morse.append('/')
    else:
        pass

morse_code = ' '.join(morse)

print(morse_code)
