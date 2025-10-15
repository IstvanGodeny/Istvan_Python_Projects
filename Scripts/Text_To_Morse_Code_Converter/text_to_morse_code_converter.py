morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', '"': '._.._.', "'": '.____.',
}

print("This is a simple text to morse code converter. Just type the text and you will get the morse code of the text.")
run_app = True
while run_app:
    input_text = input("Text: ").upper()
    morse = []
    for i in input_text:
        if i in morse_code_dict:
            morse.append(morse_code_dict[i])
        elif i == " ":
            morse.append("/")
        else:
            pass

    morse_code = ' '.join(morse)

    print(morse_code)

