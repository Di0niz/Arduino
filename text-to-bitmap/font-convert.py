# -*- coding: utf-8 -*-
#!/usr/bin/python


import struct


def main():

    fin = open("begun-hi.bmp", "rb")

    BITMAPFILEHEADER = struct.unpack('<2cIHHI', fin.read(14))

    print BITMAPFILEHEADER
    
    DIBHEADER = struct.unpack('<IIIHHIIIIII', fin.read(40))

    print DIBHEADER


    x_max = 140
    y_max = 21
    pic_size = DIBHEADER[6]

    fin.seek(0)
    fin.seek(BITMAPFILEHEADER[5])
    bite = struct.unpack(str(pic_size)+'B', fin.read(pic_size))
    
    segment = 2

    for y in reversed(range(segment*7+ 0,segment*7 + 7)):
        for x in range(0,x_max):

            i = y*x_max + x
            #print i,
            print ('1' if bite[i]==0 else ' '),
        print ""
 

    print
    rus_dic  = [u'А',u'Б',u'В',u'Г',u'Д',u'Е',u'Ж',u'З',u'И',u'К',u'Л',u'М',u'Н',u'О',u'П',u'Р',u'С',u'Т',u'Ч',u'Ф',u'Х',u'Ц',u'Ч',u'Ш',u'Щ',u'Ъ',u'Ы',u'Э',u'Ю',u'Я']
    dictionary = get_dictionary (bite, 2, rus_dic, x_max, y_max)

    print dictionary
    dictionary[u' '] = [0,0]
    dictionary[u'!'] = [158]

    print dictionary

    command =  print_command (u"С НОВЫМ ГОДОМ!", dictionary)

    print_result (command)

    for h in command:
      print "0x%X,"%h,
    print

    digit_dic = ['1','2','3','4','5','6','7','8','9','0','/','(',')','!','?','%','@']
    dictionary = get_dictionary (bite, 0, digit_dic, x_max, y_max)

    print dictionary
    return



    pass


def print_result (l):

    for i in range (8):

        for x in l :
            print ('1' if ( x & 1<<i) else ' '),    

        print

    pass

def print_command(templates, vocab):

    l = []
    new = True
    for t in templates:
        for x in vocab[t]:
            l.append(x if new ==False else (x <<8))

        new = False

        if ( t == u' '):
            new = True

        l.append (0x0)

    l.append (0x0)
    l.append (0x0)
    l.append (0x0)
    l.append (0x0)
    l.append (0x0)
    l.append (0x0)
    l.append (0x0)

    return l
    pass


def get_dictionary(bites, segment, dictionary, x_max, y_max):
    ret_dic ={}
    print len(dictionary)
    for i in range(len(dictionary)):
        ret_dic[dictionary[i]] = []


    digits = []
    for x in range(0,x_max):
        h = 0x0
        for y in reversed(range(segment*7+0,segment*7+7)):
            i = y*x_max + x
            b = 1 if bites[i]==0 else 0
            h = h | (b << (7 + segment*7 -y ))

        print "0x%X"%h,
        digits.append(h)



    current_index = 0; prev_x = 0
    for x in digits:

        if (x == 0 and prev_x != x):
            current_index = current_index + 1
            print 
            
        elif (x != 0 and current_index < len(dictionary) ):
            ret_dic[dictionary[current_index]].append(x)
            print current_index,

        prev_x = x

    return ret_dic
    pass


if __name__ == '__main__':
    main()