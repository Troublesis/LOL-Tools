import pyperclip

while True:

    lv1 = int(input("Please input start lv1 cd"))
    lv5 = int(input("Please input start lv5 cd"))

    n = (lv1 - lv5) / 4

    cd ="{}/{}/{}/{}/{}".format(lv1,lv1-n,lv1-2*n,lv1-3*n,lv1-4*n)

    print('''
==============================
    
    
{}    
    
    
==============================
'''.format(cd))

    pyperclip.copy(cd)