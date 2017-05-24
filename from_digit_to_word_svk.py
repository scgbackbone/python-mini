
def name_digit_matcher(digit, iterabulous, superpower=1):
    """takes in digit and iterable which may be generator object or
    any other iterable consisting of tuples forex( (1, 'one'),(20, 'twenty'), )
    ==> and returns  matching element - only 1st(not zeroeth) inner tuple index"""
    result = ""
    for i in enumerate(iterabulous, start=superpower):
        if i[0] == int(digit):
            result = i[1]
            break
    return result


def from_number_to_text(number):
    desiatky = ["desať", "dvadsať", "tridsať", "štyridsať", "päťdesiat", "šesťdesiat", "sedemdesiat", "osemdesiat", "deväťdesiat"]
    medzi10_20 = ["jedenásť", "dvanásť", "trinásť", "štrnásť", "pätnásť", "šestnásť", "sedemnásť", "osemnásť", "devätnásť"]
    stovky = ["sto", "dvesto", "tristo", "štyristo", "päťsto", "šesťsto", "sedemsto", "osemsto", "deväťsto"]
    tisicky = ["tisíc", "dvetisíc", "tritisíc", "štyritisíc", "päťtisíc", "šesťtisíc", "sedemtisíc", "osemtisíc", "deväťtisíc"]
    jednotky = ["jeden", "dva", "tri", "štyri", "päť", "šesť", "sedem", "osem", "deväť", "desať"]
    jednotky_len1 = ["jedno", "dve", "tri", "štyri", "päť", "šesť", "sedem", "osem", "deväť", "desať"]

    result = ""
    number = str(number)
    try:
        eur, cent = number.split(".")
    except ValueError as e:
        print(e)
        eur = number
        cent = "00"
    if len(eur) > 4:
        return("nooooooooooooooooot implemented")
    elif len(eur) == 4:
        result = name_digit_matcher(eur[0], tisicky)
        result = result + name_digit_matcher(eur[1], stovky)
        if int(eur[2:]) > 10 and int(eur[2:]) < 20:
            result = result + name_digit_matcher(eur[2:], medzi10_20, superpower=11)
        else:
            result = result + name_digit_matcher(eur[2], desiatky)
            result = result + name_digit_matcher(eur[3], jednotky)
    elif len(eur) == 3:
        result = result + name_digit_matcher(eur[0], stovky)
        if int(eur[1:]) > 10 and int(eur[1:]) < 20:
            result = result + name_digit_matcher(eur[1:], medzi10_20, superpower=11)
        else:
            result = result + name_digit_matcher(eur[1], desiatky)
            result = result + name_digit_matcher(eur[2], jednotky)
    elif len(eur) == 2:
        if int(eur) > 10 and int(eur) < 20:
            result = result + name_digit_matcher(eur, medzi10_20, superpower=11)
        else:
            result = result + name_digit_matcher(eur[0], desiatky)
            result = result + name_digit_matcher(eur[1], jednotky)
    elif len(eur) == 1:
        result = result + name_digit_matcher(eur, jednotky_len1)
    result = result + " eurá " if (len(eur) == 1 and (eur == "2" or eur == "3" or eur == "4")) else result + " eur "
    if len(cent) > 2:
        return("not implmented")
    elif len(cent) == 2:
        if cent == "00":
            return result
        elif int(cent) > 10 and int(cent) < 20:
            result = result + "a " + name_digit_matcher(cent, medzi10_20, superpower=11)
        else:
            result = result + "a " + name_digit_matcher(cent[0], desiatky)
            result = result + name_digit_matcher(cent[1], jednotky)
    elif len(cent) == 1:
        if cent == "0":
            return result
        elif cent == "5":
            return result + "a päťdesiat centov"
        result = result + "a " + name_digit_matcher(cent[0], jednotky)

    return result + " centov"
