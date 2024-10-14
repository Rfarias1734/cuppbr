#!/usr/bin/python3

import argparse
import configparser
import csv
import functools
import gzip
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import time
import re

from webob import year

__author__ = "Newton Vicente/Ramon Neves"
__license__ = ""
__version__ = "2.0"

CONFIG = {}


def read_config(filename):
    """Leia o arquivo de configuração fornecido e atualize as variáveis ​​globais para fazer alterações (CONFIG)."""

    if os.path.isfile(filename):

        # global CONFIG

        # Reading configuration file
        config = configparser.ConfigParser()
        config.read(filename)

        CONFIG["global"] = {
            "years": config.get("years", "years").split(","),
            "chars": config.get("specialchars", "chars").split(","),
            "numfrom": config.getint("nums", "from"),
            "numto": config.getint("nums", "to"),
            "wcfrom": config.getint("nums", "wcfrom"),
            "wcto": config.getint("nums", "wcto"),
            "threshold": config.getint("nums", "threshold"),
            "alectourl": config.get("alecto", "alectourl"),
            "dicturl": config.get("downloader", "dicturl"),
        }

        # 1337 mode configs, well you can add more lines if you add it to the
        # config file too.
        leet = functools.partial(config.get, "leet")
        leetc = {}
        letters = {"a", "i", "e", "t", "o", "s", "g", "z"}

        for letter in letters:
            leetc[letter] = config.get("leet", letter)

        CONFIG["LEET"] = leetc

        return True

    else:
        print("Arquivo de configuração " + filename + " não encontrado!")
        sys.exit("Exiting.")

        return False


def make_leet(x):
    """converter string em leet"""
    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x


# for concatenations...
def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)


# for sorting and making combinations...
def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1


# print list to file counting words

def print_to_file(filename, unique_list_finished):
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f.close()
    f = open(filename, "r")
    lines = 0
    for line in f:
        lines += 1
    f.close()
    print(
        "[+] Salvando o dicionário para \033[1;31m"
        + filename
        + "\033[1;m, contando \033[1;31m"
        + str(lines)
        + " palavras.\033[1;m"
    )
    inspect = input("> Mostrar o dicionário agora? [s/n] : ").lower()
    if inspect == "s":
        try:
            with open(filename, "r+") as wlist:
                data = wlist.readlines()
                for line in data:
                    print("\033[1;32m[" + filename + "] \033[1;33m" + line)
                    time.sleep(0000.1)
                    os.system("clear")
        except Exception as e:
            print("[ERROR]: " + str(e))
    else:
        pass

    print(
        "[+] Agora use seu dicionário \033[1;31m"
        + filename
        + "\033[1;m Boa sorte!"
    )

def print_cow():
    print(" ___________ ")
    print(" \033[07m  CUPPBr.py! \033[27m              # \033[07mC\033[27mommon")
    print("      \                     # \033[07mU\033[27mser")
    print("       \   \033[1;32m,__,\033[1;m             # \033[07mP\033[27masswords")
    print(
        "        \  \033[1;32m(\033[1;moo\033[1;32m)____\033[1;m         # \033[07mP\033[27mrofiler"
    )
    print("           \033[1;32m(__)    )\ \033[1;m      # \033[07mBr\033[27masil"  )
    print(
        "           \033[1;33m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m ")
    print(28 * " " + "Criação de Wordlists adaptado para a realidade Brasileira!\r\n")
    print("	Feito/Adaptado por:")
    print("	- Nilton Vicente [Github: https://github.com/nextroid] ")
    print("	- Ramon Neves [Github: https://github.com/Rfarias1734] \r\n")
    print("	ATENÇÃO: Somos uma modificação da ferramenta original cupp.py para uso no Brasil\r\n")
    print("	Ferramenta original (cupp) : https://github.com/Mebus/cupp")
    print("	Referência: Mebus | https://github.com/Mebus/\r\n")
    print("	Seja consciente: Não utilize esta ferramenta para fins ilegais!\r\n")
    print("	Esperamos que goste :)\r\n")
    print("	\r\n")
    print("	Para iniciar com as perguntas, use: cuppybr.py -i \r\n")
    print("	\r\n")

def version():
    """Versão do Display"""

    print("	\033[1;31m CUPPBr - versão: " + __version__ + "\033[1;m\r\n")
    #jogar para a versão 2.0
    print("	Última data de atualização: 07/06/2024\r\n")
    print("	Dê uma olhada no arquivo ./README.md para mais informações sobre o programa.\r\n")


def improve_dictionary(file_to_open):
    """Opção -w: Melhore um dicionário por
    questionando interativamente o usuário."""

    kombinacija = {}
    komb_unique = {}

    if not os.path.isfile(file_to_open):
        exit("Erro: arquivo " + file_to_open + " não existe.")

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    fajl = open(file_to_open, "r")
    listic = fajl.readlines()
    listica = []
    for x in listic:
        listica += x.split()

    print("\r\n      *************************************************")
    print("      *                    \033[1;31mWARNING!!!\033[1;m                 *")
    print("      *         Usando listas de palavras grandes em alguns         *")
    print("      *       opções abaixo NÃO são recomendadas!      *")
    print("      *************************************************\r\n")

    conts = input(
        "> Deseja concatenar todas as palavras da lista de palavras? [s/n]: "
    ).lower()

    if conts == "s" and len(listic) > CONFIG["global"]["threshold"]:
        print(
            "\r\n[-] O número máximo de palavras para concatenação é "
            + str(CONFIG["global"]["threshold"])
        )
        print("[-] Verifique o arquivo de configuração para aumentar o número de palavras.\r\n")
        conts = input(
            "> Deseja concatenar todas as palavras da lista de palavras? [s/n]]: "
        ).lower()

    cont = [""]
    if conts == "s":
        for cont1 in listica:
            for cont2 in listica:
                if listica.index(cont1) != listica.index(cont2):
                    cont.append(cont1 + cont2)

    spechars = [""]
    spechars1 = input(
        "> Deseja adicionar caracteres especiais no final das palavras? [s/n]: "
    ).lower()
    if spechars1 == "s":
        for spec1 in chars:
            spechars.append(spec1)
            for spec2 in chars:
                spechars.append(spec1 + spec2)
                for spec3 in chars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> Deseja adicionar alguns números aleatórios no final das palavras? [s/n]:"
    ).lower()
    leetmode = input("> Modo Leet? (Ex.: Hacker = H4ck3r) [s/n]: ").lower()

    # init
    for i in range(6):
        kombinacija[i] = [""]

    kombinacija[0] = list(komb(listica, years))
    if conts == "s":
        kombinacija[1] = list(komb(cont, years))
    if spechars1 == "s":
        kombinacija[2] = list(komb(listica, spechars))
        if conts == "s":
            kombinacija[3] = list(komb(cont, spechars))
    if randnum == "s":
        kombinacija[4] = list(concats(listica, numfrom, numto))
        if conts == "s":
            kombinacija[5] = list(concats(cont, numfrom, numto))

    print("\r\n[+] Construindo um dicionário...")

    print("[+] Classificando lista e removendo duplicatas...")

    for i in range(6):
        komb_unique[i] = list(dict.fromkeys(kombinacija[i]).keys())

    komb_unique[6] = list(dict.fromkeys(listica).keys())
    komb_unique[7] = list(dict.fromkeys(cont).keys())

    # join the lists
    uniqlist = []
    for i in range(8):
        uniqlist += komb_unique[i]

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "s":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cuppbr.cfg too...
            x = make_leet(x)  # convert to leet
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []

    unique_list_finished = [
        x
        for x in unique_list
        if len(x) > CONFIG["global"]["wcfrom"] and len(x) < CONFIG["global"]["wcto"]
    ]

    print_to_file(file_to_open + ".cupp.txt", unique_list_finished)

    fajl.close()


def interactive():
    """Opção -i: Questione interativamente o usuário e
    crie um arquivo de dicionário de senha com base na resposta."""

    print("\r\n[+] Insira as informações sobre a vítima para fazer um dicionário")
    print("[+] Se você não souber todas as informações, apenas pressione Enter quando solicitado! ;)\r\n")

    # We need some information first!

    profile = {}

    name = input("> Primeiro nome: ").lower()
    while len(name) == 0 or name == " " or name == "  " or name == "   ":
        print("\r\n[-] Você deve inserir um nome pelo menos!")
        name = input("> Nome: ").lower()
    profile["name"] = str(name)

    profile["surname"] = input("> Sobrenome: ").lower()
    profile["nick"] = input("> Apelido: ").lower()
    birthdate = input("> Data de nascimento (DDMMAAAA): ")
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para o aniversário!")
        birthdate = input("> Data de nascimento (DDMMAAAA): ")
    profile["birthdate"] = str(birthdate)


    print("\r\n")

    profile["wife"] = input("> Esposa (o), nome: ").lower()
    profile["wifen"] = input("> Esposa (o), apelido: ").lower()
    wifeb = input("> Esposa (o), Data de nascimento (DDMMAAAA): ")
    while len(wifeb) != 0 and len(wifeb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para o aniversário!")
        wifeb = input("> Esposa (o), Data de nascimento (DDMMAAAA):: ")
    profile["wifeb"] = str(wifeb)
    print("\r\n")

    profile["kid"] = input("> Nome do filho(a): ").lower()
    profile["kidn"] = input("> Apelido do filho(a): ").lower()
    kidb = input("> Data de nascimento do filho(a) (DDMMAAAA): ")
    while len(kidb) != 0 and len(kidb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para o aniversário!")
        kidb = input("> Data de nascimento do filho(a) (DDMMAAAA): ")
    profile["kidb"] = str(kidb)
    print("\r\n")

#Inserção Familiares Mãe
    profile["mon"] = input("> Mãe, nome: ").lower()
    profile["monn"] = input("> Mãe, apelido: ").lower()
    monb = input("> Mãe, Data de nascimento (DDMMAAAA): ")
    while len(monb) != 0 and len(monb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para o aniversário!")
        monb = input("> Mãe, Data de nascimento (DDMMAAAA):: ")
    profile["monb"] = str(monb)
    print("\r\n")
  
#Inserção Familiares pai
    profile["dad"] = input("> Pai, nome: ").lower()
    profile["dadn"] = input("> Pai, apelido: ").lower()
    dadb = input("> Pai, Data de nascimento (DDMMAAAA): ")
    while len(dadb) != 0 and len(dadb) != 8:
        print("\r\n[-] Você deve inserir 8 dígitos para o aniversário!")
        dadb = input("> Pai, Data de nascimento (DDMMAAAA):: ")
    profile["dadb"] = str(dadb)
    print("\r\n")

    profile["pet"] = input("> Nome do animal de estimação: ").lower()
    
   #Inserção CPF
    cpfnum = re.sub('[^0-9]', '',(input("> CPF (apenas os digitos): ")))
    while len(cpfnum) != 0 and len(cpfnum) != 11:
        print("\r\n[-] Você deve inserir 11 dígitos para o CPF!")
        cpfnum = re.sub('[^0-9]', '',(input(">  CPF (12345678901): ")))
    profile["cpfnum"] = str(cpfnum)

    #Times de Futebol
    entrada_futebol = input(
        "> Deseja digitar Times de Futebol referente ao alvo? [s/n]:").lower()
    futebol = ""
    if entrada_futebol == "s":
        futebol = input(
      """> Digite os times, separados por vírgula. [Ex.: Vasco, PSG, Nova Iguacu] 
      Obs.: Os espaços serão removidos: """
        ).replace(" ", "").lower()
    profile["futebol"] = futebol.split(",")

    """
    Inclusão de hobbie / datas importantes
    """
    
    profile["hobbie"] = input("> Hobbie: ").lower()
    profile["company"] = input("> Nome da empresa: ").lower()
    profile["dataimportante"] = input("> Datas importantes (escreva sem espaços, até 05 dígitos -> ex: 07set ou 0709) : ").lower()

    print("\r\n")
    
    profile["words"] = [""]
    profile["words02"] = [""]

    # Marcação 3 inclusão de termos do ambiente de trabalho
    words4 = input(
        "> Deseja digitar palavras referente ao ambiente profissional? [s/n]:"
    ).lower()
    words3 = ""
    if words4 == "s":
        words3 = input(
      """> Digite as palavras, separadas por vírgula. [Ex.: contador, selva, photo] 
      Obs.: Os espaços serão removidos: """
        ).replace(" ", "")
    profile["words02"] = words3.split(",")

    #Marcação 4 inclusão de telefone semelhante ao aniversário
    telefone = input("> Telefone (Escreva conforme o exemplo: 061987654321 ): ")
    while len(telefone) != 0 and len(telefone) != 12:
        print("\r\n[-] Você deve inserir 12 dígitos para o telefone!")
        telefone = input(">  Telefone (DDD987654321): ")
    profile["telefone"] = str(telefone)

    words1 = input(
        "> Deseja adicionar algumas palavras-chave sobre a vítima? [s/n]: "
    ).lower()
    words2 = ""
    if words1 == "s":
        words2 = input(
      """> Digite as palavras, separadas por vírgula. [Ex.: hacker, suco, preto] 
      Obs.: Os espaços serão removidos: """
        ).replace(" ", "")
    profile["words"] = words2.split(",")

    profile["spechars1"] = input(
        "> Deseja adicionar caracteres especiais no final das palavras? [s/n]: "
    ).lower()

    profile["randnum"] = input(
        "> Deseja adicionar alguns números aleatórios no final das palavras? [s/n]:"
    ).lower()
    profile["leetmode"] = input("> Modo Leet? (Ex.: Hacker = H4ck3r) [s/n]: ").lower()

    generate_wordlist_from_profile(profile)  # generate the wordlist


def generate_wordlist_from_profile(profile):
    """ Generates a wordlist from a given profile """

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    #outras palavras da vítima
    profile["spechars"] = []

    if profile["spechars1"] == "s":
        for spec1 in chars:
            profile["spechars"].append(spec1)
            for spec2 in chars:
                profile["spechars"].append(spec1 + spec2)
                for spec3 in chars:
                    profile["spechars"].append(spec1 + spec2 + spec3)

    print("\r\n[+] Construindo um dicionário...")

    # Now me must do some string modifications...

    # Birthdays first

    birthdate_yy = profile["birthdate"][-2:]
    birthdate_yyy = profile["birthdate"][-3:]
    birthdate_yyyy = profile["birthdate"][-4:]
    birthdate_xd = profile["birthdate"][1:2]
    birthdate_xm = profile["birthdate"][3:4]
    birthdate_dd = profile["birthdate"][:2]
    birthdate_mm = profile["birthdate"][2:4]

    #CPF

    cpfnum_1a3 = profile["cpfnum"][0:3]
    cpfnum_4a6 = profile["cpfnum"][3:6]
    cpfnum_7a9 = profile["cpfnum"][6:9]
    cpfnum_2ul = profile["cpfnum"][-2:] 
    cpfnum_completo = profile["cpfnum"][0:]

    cpf = [
        cpfnum_1a3,
        cpfnum_4a6,
        cpfnum_7a9,
        cpfnum_2ul,
        cpfnum_completo
    ]



    # Telefone
    
    telefone_semddd = profile["telefone"][-9:]
    telefone_ult4 = profile["telefone"][-4:]
    telefone_9dig = profile["telefone"][3:12]
    telefone_sem9 = profile["telefone"][4:12] 

    tel = [
        telefone_semddd,
        telefone_ult4,
        telefone_9dig,
        telefone_sem9,
    ]

    wifeb_yy = profile["wifeb"][-2:]
    wifeb_yyy = profile["wifeb"][-3:]
    wifeb_yyyy = profile["wifeb"][-4:]
    wifeb_xd = profile["wifeb"][1:2]
    wifeb_xm = profile["wifeb"][3:4]
    wifeb_dd = profile["wifeb"][:2]
    wifeb_mm = profile["wifeb"][2:4]

    kidb_yy = profile["kidb"][-2:]
    kidb_yyy = profile["kidb"][-3:]
    kidb_yyyy = profile["kidb"][-4:]
    kidb_xd = profile["kidb"][1:2]
    kidb_xm = profile["kidb"][3:4]
    kidb_dd = profile["kidb"][:2]
    kidb_mm = profile["kidb"][2:4]

    #Inserção Familiares Mãe

    monb_yy = profile["monb"][-2:]
    monb_yyy = profile["monb"][-3:]
    monb_yyyy = profile["monb"][-4:]
    monb_xd = profile["monb"][1:2]
    monb_xm = profile["monb"][3:4]
    monb_dd = profile["monb"][:2]
    monb_mm = profile["monb"][2:4]

    #Inserção Familiares Pai

    dadb_yy = profile["dadb"][-2:]
    dadb_yyy = profile["dadb"][-3:]
    dadb_yyyy = profile["dadb"][-4:]
    dadb_xd = profile["dadb"][1:2]
    dadb_xm = profile["dadb"][3:4]
    dadb_dd = profile["dadb"][:2]
    dadb_mm = profile["dadb"][2:4]

    # Convert first letters to uppercase...

    nameup = profile["name"].title()
    surnameup = profile["surname"].title()
    nickup = profile["nick"].title()
    wifeup = profile["wife"].title()
    wifenup = profile["wifen"].title()
    kidup = profile["kid"].title()
    kidnup = profile["kidn"].title()
    petup = profile["pet"].title()

    #Inserção Familiares Mãe
    #Converção da primeira letra para maiuscula

    monup = profile["mon"].title()
    monnup = profile["monn"].title()

    #Inserção Familiares Pai
    #Converção da primeira letra para maiuscula

    dadup = profile["dad"].title()
    dadnup = profile["dadn"].title()


    """
    Marcação 2 para inclusão de novos contextos: hobbie data importante
    Converter a 1ª letra pra maiuscula
    """
    hobbieup = profile["hobbie"].title()
    companyup = profile["company"].title()
    dataimportanteup = profile["dataimportante"].title()
    
    wordsup = []
    wordsup = list(map(str.title, profile["words"]))
    wordsup2 = list(map(str.title, profile["words02"]))

    word = profile["words"] + wordsup
    word2 = profile["words02"] + wordsup2

    #Times de futebol

    futebolup = []
    futebolup = list(map(str.title, profile["futebol"]))

    fut = profile["futebol"] + futebolup

    # reverse a name

    rev_name = profile["name"][::-1]
    rev_nameup = nameup[::-1]
    rev_nick = profile["nick"][::-1]
    rev_nickup = nickup[::-1]
    rev_wife = profile["wife"][::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = profile["kid"][::-1]
    rev_kidup = kidup[::-1]

#Inserção Familiares Mãe
    rev_mon = profile["mon"][::-1]
    rev_monup = monup[::-1]

    #Inserção Familiares Pai
    rev_dad = profile["dad"][::-1]
    rev_dadup = dadup[::-1]


    rev_hobbie = profile["hobbie"][::-1]
    rev_hobbieup = profile["hobbie"][::-1]
    rev_dataimportante = profile["dataimportante"][::-1]
    rev_dataimportanteup = profile["dataimportante"][::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
        rev_hobbie,
        rev_hobbieup,
        rev_dataimportante,
        rev_dataimportanteup,

#Inserção Familiares Mãe
        rev_mon,
        rev_monup,

#Inserção Familiares Pai
        rev_dad,
        rev_dadup,

    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]

#Inserção Familiares Mãe
    rev_m = [rev_mon, rev_monup]

#Inserção Familiares Pai
    rev_d = [rev_dad, rev_dadup]

    rev_h = [rev_hobbie, rev_hobbieup]
    rev_di = [rev_dataimportante, rev_dataimportanteup]


    # Birthdays combinations

    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (
                        bds.index(bds1) != bds.index(bds2)
                        and bds.index(bds2) != bds.index(bds3)
                        and bds.index(bds1) != bds.index(bds3)
                    ):
                        bdss.append(bds1 + bds2 + bds3)

    tels = []

    for tel1 in tel:
        tels.append(tel1)
        for tel2 in tel:
            if tel.index(tel1) != tel.index(tel2):
                tels.append(tel1 + tel2)
                for tel3 in tel:
                    if (
                        tel.index(tel1) != tel.index(tel2)
                        and tel.index(tel2) != tel.index(tel3)
                        and tel.index(tel1) != tel.index(tel3)
                    ):
                        tels.append(tel1 + tel2 + tel3)

                # For a woman...
    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (
                        wbds.index(wbds1) != wbds.index(wbds2)
                        and wbds.index(wbds2) != wbds.index(wbds3)
                        and wbds.index(wbds1) != wbds.index(wbds3)
                    ):
                        wbdss.append(wbds1 + wbds2 + wbds3)

                # and a child...
    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (
                        kbds.index(kbds1) != kbds.index(kbds2)
                        and kbds.index(kbds2) != kbds.index(kbds3)
                        and kbds.index(kbds1) != kbds.index(kbds3)
                    ):
                        kbdss.append(kbds1 + kbds2 + kbds3)

#Inserção Familiares Mãe

    mbds = [monb_yy, monb_yyy, monb_yyyy, monb_xd, monb_xm, monb_dd, monb_mm]

    mbdss = []

    for mbds1 in mbds:
        mbdss.append(mbds1)
        for mbds2 in mbds:
            if mbds.index(mbds1) != mbds.index(mbds2):
                mbdss.append(mbds1 + mbds2)
                for mbds3 in mbds:
                    if (
                        mbds.index(mbds1) != mbds.index(mbds2)
                        and mbds.index(mbds2) != mbds.index(mbds3)
                        and mbds.index(mbds1) != mbds.index(mbds3)
                    ):
                        mbdss.append(mbds1 + mbds2 + mbds3)

#Inserção Familiares Pai

    dbds = [dadb_yy, dadb_yyy, dadb_yyyy, dadb_xd, dadb_xm, dadb_dd, dadb_mm]

    dbdss = []

    for dbds1 in dbds:
        dbdss.append(dbds1)
        for dbds2 in dbds:
            if dbds.index(dbds1) != dbds.index(dbds2):
                dbdss.append(dbds1 + dbds2)
                for dbds3 in dbds:
                    if (
                        dbds.index(dbds1) != dbds.index(dbds2)
                        and dbds.index(dbds2) != dbds.index(dbds3)
                        and dbds.index(dbds1) != dbds.index(dbds3)
                    ):
                        dbdss.append(dbds1 + dbds2 + dbds3)


                # string combinations....
    """
    Marcação 1 para inclusão de novos contextos: hobbie, datas importantes.
    """
    kombinaac = [
    	profile["pet"], petup, 
    	profile["company"], companyup, 
    	profile["hobbie"], hobbieup,  
        profile["dataimportante"], dataimportanteup,  
    ]

    kombina = [
        profile["name"],
        profile["surname"],
        profile["nick"],
        nameup,
        surnameup,
        nickup,
    ]

    kombinaw = [
        profile["wife"],
        profile["wifen"],
        wifeup,
        wifenup,
        profile["surname"],
        surnameup,
    ]

    kombinak = [
        profile["kid"],
        profile["kidn"],
        kidup,
        kidnup,
        profile["surname"],
        surnameup,
    ]

#Inserção Familiares Mãe
    kombinam = [
        profile["mon"],
        profile["monn"],
        monup,
        monnup,
        profile["surname"],
        surnameup,
    ]

#Inserção Familiares Pai
    kombinad = [
        profile["dad"],
        profile["dadn"],
        dadup,
        dadnup,
        profile["surname"],
        surnameup,
    ]

    kombinah = [
        profile["hobbie"],
        profile["kidn"],
        hobbieup,
        kidnup,
        profile["surname"],
        surnameup,
        nameup,
        nickup,
    ]

    kombinadi = [
        profile["dataimportante"],
        profile["surname"],
        dataimportanteup,
        kidnup,
        profile["surname"],
        surnameup,
        nameup,
        nickup,
    ]

    kombinatel = [
        profile["telefone"],
        profile["hobbie"],
        profile["kidn"],
        hobbieup,
        kidnup,
        profile["surname"],
        surnameup,
        nameup,
        nickup,
    ]

    #inserção CPF
    kombinacpf = [
        profile["telefone"],
        profile["hobbie"],
        profile["kid"],
        profile["kidn"],
        profile["surname"],
        profile["wifen"],
        profile["wife"],
        profile["wifen"],
        profile["mon"],
        profile["monn"],
        profile["pet"],
        profile["company"],
        profile["dataimportante"],
        hobbieup,
        kidup,
        kidnup,
        surnameup,
        nameup,
        nickup,
        wifeup,
        wifenup,
        monup,
        monnup,
        dataimportanteup,
        petup,
        companyup 
    ]


    kombinaatel = []
    for kombina1 in kombinatel:
        kombinaatel.append(kombina1)
        for kombina2 in kombinatel:
            if kombinatel.index(kombina1) != kombinatel.index(kombina2) and kombinatel.index(
                kombina1.title()
            ) != kombinatel.index(kombina2.title()):
                kombinaatel.append(kombina1 + kombina2)

    
    kombinaadi = []
    for kombina1 in kombinadi:
        kombinaadi.append(kombina1)
        for kombina2 in kombinadi:
            if kombinadi.index(kombina1) != kombinadi.index(kombina2) and kombinadi.index(
                kombina1.title()
            ) != kombinadi.index(kombina2.title()):
                kombinaadi.append(kombina1 + kombina2)


    kombinaah = []
    for kombina1 in kombinah:
        kombinaah.append(kombina1)
        for kombina2 in kombinah:
            if kombinah.index(kombina1) != kombinah.index(kombina2) and kombinah.index(
                kombina1.title()
            ) != kombinah.index(kombina2.title()):
                kombinaah.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(
                kombina1.title()
            ) != kombinak.index(kombina2.title()):
                kombinaak.append(kombina1 + kombina2)

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(
                kombina1.title()
            ) != kombina.index(kombina2.title()):
                kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(
                kombina1.title()
            ) != kombinaw.index(kombina2.title()):
                kombinaaw.append(kombina1 + kombina2)

#Inserção Familiares Mãe

    kombinaam = []
    for kombina1 in kombinam:
        kombinaam.append(kombina1)
        for kombina2 in kombinam:
            if kombinam.index(kombina1) != kombinam.index(kombina2) and kombinam.index(
                kombina1.title()
            ) != kombinam.index(kombina2.title()):
                kombinaam.append(kombina1 + kombina2)

#Inserção Familiares Pai

    kombinaad = []
    for kombina1 in kombinad:
        kombinaad.append(kombina1)
        for kombina2 in kombinad:
            if kombinad.index(kombina1) != kombinad.index(kombina2) and kombinad.index(
                kombina1.title()
            ) != kombinad.index(kombina2.title()):
                kombinaad.append(kombina1 + kombina2)


#inserção CPF

    kombinaacpf = []
    for kombina1 in kombinacpf:
        kombinaacpf.append(kombina1)
        for kombina2 in kombinacpf:
            if kombinacpf.index(kombina1) != kombinacpf.index(kombina2) and kombinacpf.index(
                kombina1.title()
            ) != kombinacpf.index(kombina2.title()):
                kombinaacpf.append(kombina1 + kombina2)


    kombi = {}
    kombi[1] = list(komb(kombinaa, bdss))
    kombi[1] += list(komb(kombinaa, bdss, "_"))
    kombi[206] = list(komb(kombinaah, bdss))
    kombi[206] += list(komb(kombinaah, bdss, "_"))
    kombi[207] = list(komb(kombinaatel, bdss))
    kombi[207] += list(komb(kombinaatel, bdss, "_"))
    kombi[208] = list(komb(kombinaadi, bdss))
    kombi[208] += list(komb(kombinaadi, bdss, "_"))
    kombi[209] = list(komb(kombinaam, bdss))
    kombi[209] += list(komb(kombinaam, bdss, "_"))

    kombi[210] = list(komb(kombinaad, bdss))
    kombi[210] += list(komb(kombinaad, bdss, "_"))

    kombi[2] = list(komb(kombinaaw, wbdss))
    kombi[2] += list(komb(kombinaaw, wbdss, "_"))
    kombi[216] = list(komb(kombinaah, wbdss))
    kombi[216] += list(komb(kombinaah, wbdss, "_"))
    kombi[217] = list(komb(kombinaatel, wbdss))
    kombi[217] += list(komb(kombinaatel, wbdss, "_"))
    kombi[218] = list(komb(kombinaadi, wbdss))
    kombi[218] += list(komb(kombinaadi, wbdss, "_"))
    kombi[219] = list(komb(kombinaam, wbdss))
    kombi[219] += list(komb(kombinaam, wbdss, "_"))
    kombi[220] = list(komb(kombinaad, wbdss))
    kombi[220] += list(komb(kombinaad, wbdss, "_"))



    kombi[3] = list(komb(kombinaak, kbdss))
    kombi[3] += list(komb(kombinaak, kbdss, "_"))
    kombi[226] = list(komb(kombinaah, kbdss))
    kombi[226] += list(komb(kombinaah, kbdss, "_"))
    kombi[227] = list(komb(kombinaatel, kbdss))
    kombi[227] += list(komb(kombinaatel, kbdss, "_"))
    kombi[228] = list(komb(kombinaadi, kbdss))
    kombi[228] += list(komb(kombinaadi, kbdss, "_"))
    kombi[229] = list(komb(kombinaam, kbdss))
    kombi[229] += list(komb(kombinaam, kbdss, "_"))
    kombi[230] = list(komb(kombinaad, kbdss))
    kombi[230] += list(komb(kombinaad, kbdss, "_"))


    kombi[4] = list(komb(kombinaam, mbdss))
    kombi[4] += list(komb(kombinaam, mbdss, "_"))
    kombi[236] = list(komb(kombinaak, mbdss))
    kombi[236] += list(komb(kombinaak, mbdss, "_"))
    kombi[237] = list(komb(kombinaah, mbdss))
    kombi[237] += list(komb(kombinaah, mbdss, "_"))
    kombi[238] = list(komb(kombinaatel, mbdss))
    kombi[238] += list(komb(kombinaatel, mbdss, "_"))
    kombi[239] = list(komb(kombinaadi, mbdss))
    kombi[239] += list(komb(kombinaadi, mbdss, "_"))
    kombi[240] = list(komb(kombinaad, mbdss))
    kombi[240] += list(komb(kombinaad, mbdss, "_"))
    
    kombi[5] = list(komb(kombinaad, dbdss))
    kombi[5] += list(komb(kombinaad, dbdss, "_"))
    kombi[246] = list(komb(kombinaak, dbdss))
    kombi[246] += list(komb(kombinaak, dbdss, "_"))
    kombi[247] = list(komb(kombinaah, dbdss))
    kombi[247] += list(komb(kombinaah, dbdss, "_"))
    kombi[248] = list(komb(kombinaatel, dbdss))
    kombi[248] += list(komb(kombinaatel, dbdss, "_"))
    kombi[249] = list(komb(kombinaadi, dbdss))
    kombi[249] += list(komb(kombinaadi, dbdss, "_"))
    kombi[250] = list(komb(kombinaam, dbdss))
    kombi[250] += list(komb(kombinaam, dbdss, "_"))

    kombi[6] = list(komb(kombinaa, years))
    kombi[6] += list(komb(kombinaa, years, "_"))
    kombi[256] = list(komb(kombinaah, years))
    kombi[256] += list(komb(kombinaah, years, "_"))
    kombi[257] = list(komb(kombinaadi, years))
    kombi[257] += list(komb(kombinaadi, years, "_"))
    kombi[258] = list(komb(kombinaatel, years))
    kombi[258] += list(komb(kombinaatel, years, "_"))
    kombi[259] = list(komb(kombinaam, years))
    kombi[259] += list(komb(kombinaam, years, "_"))
    kombi[260] = list(komb(kombinaad,years))
    kombi[260] += list(komb(kombinaad, years, "_"))

    
    kombi[7] = list(komb(kombinaac, years))
    kombi[7] += list(komb(kombinaac, years, "_"))
    kombi[8] = list(komb(kombinaaw, years))
    kombi[8] += list(komb(kombinaaw, years, "_"))
    kombi[9] = list(komb(kombinaak, years))
    kombi[9] += list(komb(kombinaak, years, "_"))
    kombi[10] = list(komb(kombinaam, years))
    kombi[10] += list(komb(kombinaam, years, "_"))
    kombi[11] = list(komb(kombinaad, years))
    kombi[11] += list(komb(kombinaad, years, "_"))
    kombi[12] = list(komb(word, bdss))
    kombi[12] += list(komb(word, bdss, "_"))
    kombi[13] = list(komb(word, wbdss))
    kombi[13] += list(komb(word, wbdss, "_"))
    kombi[14] = list(komb(word, kbdss))
    kombi[14] += list(komb(word, kbdss, "_"))
    kombi[15] = list(komb(word, mbdss))
    kombi[15] += list(komb(word, mbdss, "_"))
    kombi[16] = list(komb(word, dbdss))
    kombi[16] += list(komb(word, dbdss, "_"))
    kombi[17] = list(komb(word, years))
    kombi[17] += list(komb(word, years, "_"))
    kombi[202] = list(komb(word2, bdss))
    kombi[202] += list(komb(word2, bdss, "_"))
    kombi[212] = list(komb(word2, wbdss))
    kombi[212] += list(komb(word2, wbdss, "_"))
    kombi[222] = list(komb(word2, kbdss))
    kombi[222] += list(komb(word2, kbdss, "_"))
    kombi[232] = list(komb(word2, mbdss))
    kombi[232] += list(komb(word2, mbdss, "_"))
    kombi[242] = list(komb(word2, dbdss))
    kombi[242] += list(komb(word2, dbdss, "_"))
    kombi[252] = list(komb(word2, years))
    kombi[252] += list(komb(word2, years, "_"))

# Time de futebol
    kombi[18] = list(komb(fut, bdss))
    kombi[18] += list(komb(fut, bdss, "_"))
    kombi[19] = list(komb(fut, wbdss))
    kombi[19] += list(komb(fut, wbdss, "_"))
    kombi[20] = list(komb(fut, kbdss))
    kombi[20] += list(komb(fut, kbdss, "_"))
    kombi[21] = list(komb(fut, mbdss))
    kombi[21] += list(komb(fut, dbdss, "_"))
    kombi[22] = list(komb(fut, dbdss))
    kombi[22] += list(komb(fut, mbdss, "_"))    
    kombi[23] = list(komb(fut, years))
    kombi[23] += list(komb(fut, years, "_"))

# inserção CPF

    kombi[24] = list(komb(kombinaa, cpf))
    kombi[24] += list(komb(kombinaa, cpf, "_"))
    kombi[25] = list(komb(kombinaah, cpf))
    kombi[25] += list(komb(kombinaah, cpf, "_"))
    kombi[26] = list(komb(kombinaatel, cpf))
    kombi[26] += list(komb(kombinaatel, cpf, "_"))
    kombi[27] = list(komb(kombinaadi, cpf))
    kombi[27] += list(komb(kombinaadi, cpf, "_"))
    kombi[28] = list(komb(kombinaam, cpf))
    kombi[28] += list(komb(kombinaam, cpf, "_"))
    kombi[29] = list(komb(kombinaad, cpf))
    kombi[29] += list(komb(kombinaad, cpf, "_"))   
    kombi[30] = list(komb(kombinaak, cpf))
    kombi[30] += list(komb(kombinaak, cpf, "_"))
    kombi[31] = list(komb(word, cpf))
    kombi[31] += list(komb(word, cpf, "_"))
    kombi[32] = list(komb(word2, cpf))
    kombi[32] += list(komb(word2, cpf, "_"))
    kombi[33] = list(komb(fut, cpf))
    kombi[33] += list(komb(fut, cpf, "_"))

    #time de futebol
    kombi[34] = list(komb(kombinaa, fut))
    kombi[34] += list(komb(kombinaa, fut, "_"))
    kombi[35] = list(komb(kombinaah, fut))
    kombi[35] += list(komb(kombinaah, fut, "_"))
    kombi[36] = list(komb(kombinaatel, fut))
    kombi[36] += list(komb(kombinaatel, fut, "_"))
    kombi[37] = list(komb(kombinaadi, fut))
    kombi[37] += list(komb(kombinaadi, fut, "_"))
    kombi[38] = list(komb(kombinaam, fut))
    kombi[38] += list(komb(kombinaam, fut, "_"))
    kombi[39] = list(komb(kombinaad, fut))
    kombi[39] += list(komb(kombinaad, fut, "_"))

    kombi[40] = list(komb(kombinaak, fut))
    kombi[40] += list(komb(kombinaak, fut, "_"))
    kombi[41] = list(komb(word, fut))
    kombi[41] += list(komb(word, fut, "_"))
    kombi[42] = list(komb(word2, fut))
    kombi[42] += list(komb(word2, fut, "_"))
    kombi[43] = list(komb(cpf, fut))
    kombi[43] += list(komb(cpf, fut, "_"))


    kombi[44] = [""]
    kombi[45] = [""]
    kombi[46] = [""]
    kombi[47] = [""]
    kombi[48] = [""]
    kombi[49] = [""]
    kombi[50] = [""]
    kombi[51] = [""]
    kombi[52] = [""]
    kombi[53] = [""]
    kombi[54] = [""]
    kombi[55] = [""]
    kombi[56] = [""]
    if profile["randnum"] == "s":
        kombi[44] = list(concats(word, numfrom, numto))
        kombi[45] = list(concats(word2, numfrom, numto))
        kombi[46] = list(concats(kombinaa, numfrom, numto))
        kombi[47] = list(concats(kombinaac, numfrom, numto))
        kombi[48] = list(concats(kombinaaw, numfrom, numto))
        kombi[49] = list(concats(kombinaak, numfrom, numto))
        kombi[50] = list(concats(kombinaam, numfrom, numto))
        kombi[51] = list(concats(kombinaad, numfrom, numto))
        kombi[52] = list(concats(kombinaatel, numfrom, numto))
        kombi[53] = list(concats(kombinaadi, numfrom, numto))
        kombi[54] = list(concats(cpf, numfrom, numto))
        kombi[55] = list(concats(reverse, numfrom, numto))
        kombi[56] = list(concats(fut, numfrom, numto))
    kombi[57] = list(komb(reverse, years))
    kombi[57] += list(komb(reverse, years, "_"))
    kombi[58] = list(komb(rev_w, wbdss))
    kombi[58] += list(komb(rev_w, wbdss, "_"))
    kombi[59] = list(komb(rev_k, kbdss))
    kombi[59] += list(komb(rev_k, kbdss, "_"))
    kombi[60] = list(komb(rev_m, mbdss))
    kombi[60] += list(komb(rev_m, mbdss, "_"))
    kombi[61] = list(komb(rev_d, dbdss))
    kombi[61] += list(komb(rev_d, dbdss, "_"))
    kombi[62] = list(komb(rev_n, bdss))
    kombi[62] += list(komb(rev_n, bdss, "_"))
    kombi[63] = list(komb(rev_h, kbdss))
    kombi[63] += list(komb(rev_h, kbdss, "_"))
    kombi[64] = list(komb(rev_di, kbdss))
    kombi[64] += list(komb(rev_di, kbdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    komb007 = [""]
    komb008 = [""]
    komb009 = [""]
    komb010 = [""]
    komb011 = [""]
    komb012 = [""]
    komb013 = [""]
    komb014 = [""]
    komb015 = [""]
    if len(profile["spechars"]) > 0:
        komb001 = list(komb(kombinaa, profile["spechars"]))
        komb002 = list(komb(kombinaac, profile["spechars"]))
        komb003 = list(komb(kombinaaw, profile["spechars"]))
        komb004 = list(komb(kombinaak, profile["spechars"]))
        komb005 = list(komb(kombinaam, profile["spechars"]))
        komb006 = list(komb(kombinaad, profile["spechars"]))
        komb007 = list(komb(word, profile["spechars"]))
        komb008 = list(komb(reverse, profile["spechars"]))
        komb009 = list(komb(kombinaah, profile["spechars"]))
        komb010 = list(komb(tels, profile["spechars"]))
        komb011 = list(komb(kombinaatel, profile["spechars"]))
        komb012 = list(komb(kombinaadi, profile["spechars"]))
        komb013 = list(komb(word2, profile["spechars"]))
        komb014 = list(komb(cpf, profile["spechars"]))
        komb015 = list(komb(fut, profile["spechars"]))

    

    print("[+] Classificando lista e removendo palavras duplicadas...")

    komb_unique = {}
    for i in range(1, 22):
        komb_unique[i] = list(dict.fromkeys(kombi[i]).keys())

    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    komb_unique05 = list(dict.fromkeys(kombinaam).keys())
    komb_unique06 = list(dict.fromkeys(kombinaad).keys())
    komb_unique07 = list(dict.fromkeys(kombinaatel).keys())
    komb_unique08 = list(dict.fromkeys(kombinaah).keys())
    komb_unique09 = list(dict.fromkeys(kombinaadi).keys())    
    komb_unique010 = list(dict.fromkeys(word).keys())
    komb_unique011 = list(dict.fromkeys(word2).keys())
    komb_unique012 = list(dict.fromkeys(cpf).keys())
    komb_unique013 = list(dict.fromkeys(fut).keys())    
    komb_unique014 = list(dict.fromkeys(reverse).keys())
    komb_unique015 = list(dict.fromkeys(tels).keys())
    komb_unique016 = list(dict.fromkeys(komb001).keys())
    komb_unique017 = list(dict.fromkeys(komb002).keys())
    komb_unique018 = list(dict.fromkeys(komb003).keys())
    komb_unique019 = list(dict.fromkeys(komb004).keys())
    komb_unique020 = list(dict.fromkeys(komb005).keys())
    komb_unique021 = list(dict.fromkeys(komb006).keys())
    komb_unique022 = list(dict.fromkeys(komb007).keys())
    komb_unique023 = list(dict.fromkeys(komb008).keys())
    komb_unique024 = list(dict.fromkeys(komb009).keys())
    komb_unique025 = list(dict.fromkeys(komb010).keys())
    komb_unique026 = list(dict.fromkeys(komb011).keys())
    komb_unique027 = list(dict.fromkeys(komb012).keys())
    komb_unique028 = list(dict.fromkeys(komb013).keys())
    komb_unique029 = list(dict.fromkeys(komb014).keys())
    komb_unique030 = list(dict.fromkeys(komb015).keys())


    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + mbdss
        + cpf
        + tels
        + reverse
        + fut
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        + komb_unique05
        + komb_unique06
        + komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
        + komb_unique013
        + komb_unique014
        + komb_unique015
    )

    for i in range(1,21):
        uniqlist += komb_unique[i]

    uniqlist += (
        komb_unique016
        + komb_unique017
        + komb_unique018
        + komb_unique019
        + komb_unique020
        + komb_unique021
        + komb_unique022
        + komb_unique023
        + komb_unique024
        + komb_unique025
        + komb_unique026
        + komb_unique027
        + komb_unique028
        + komb_unique029
        + komb_unique030
    )
    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if profile["leetmode"] == "s":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cuppbr.cfg too...

            x = make_leet(x)  # convert to leet
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []
    unique_list_finished = [
        x
        for x in unique_list
        if len(x) < CONFIG["global"]["wcto"] and len(x) > CONFIG["global"]["wcfrom"]
    ]

    print_to_file(profile["name"] + ".txt", unique_list_finished)


def download_http(url, targetfile):
    print("[+] Baixando " + targetfile + " de " + url + " ... ")
    webFile = urllib.request.urlopen(url)
    localFile = open(targetfile, "wb")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()


def alectodb_download():
    """Baixe csv de alectodb e salve em um arquivo local como uma lista de
    nomes de usuário e senhas"""

    url = CONFIG["global"]["alectourl"]

    print("\r\n[+] Verificando se alectodb não está presente...")

    targetfile = "alectodb.csv.gz"

    if not os.path.isfile(targetfile):

        download_http(url, targetfile)

    f = gzip.open(targetfile, "rt")

    data = csv.reader(f)

    usernames = []
    passwords = []
    for row in data:
        usernames.append(row[5])
        passwords.append(row[6])
    gus = list(set(usernames))
    gpa = list(set(passwords))
    gus.sort()
    gpa.sort()

    print(
        "\r\n[+] Exportando para alectodb-usernames.txt e alectodb-passwords.txt\r\n[+] Feito!"
    )
    f = open("alectodb-usernames.txt", "w")
    f.write(os.linesep.join(gus))
    f.close()

    f = open("alectodb-passwords.txt", "w")
    f.write(os.linesep.join(gpa))
    f.close()


def download_wordlist():
    """Opção -l: Baixe listas de palavras do repositório http como
    definido no arquivo de configuração."""

    print("	\r\n	Escolha a seção que deseja baixar:	\r\n")

    print("     1   Moby            14      francês         27      locais")
    print("     2   africano        15      alemão          28      polonês")
    print("     3   americano       16      hindi           29      aleatório")
    print("     4   australiano     17      húngaro         30      religião")
    print("     5   chinês          18      italiano        31      russo")
    print("     6   computador      19      japonês         32      ciência")
    print("     7   croata          20      latino          33      espanhol")
    print("     8   tcheco          21      literatura      34      nativo africano")
    print("     9   dinamarqueses   22      movieTV         35      sueco")
    print("    10   bases de dados  23      música          36      turco")
    print("    11   dicionários     24      nomes           37      judeu")
    print("    12   alemão          25      net             38      sair do programa")
    print("    13   finlandês       26      norueguês       \r\n")
    print(
        "	\r\n	Os arquivos serão baixados de "
        + CONFIG["global"]["dicturl"]
        + " repositório"
    )
    print(
        "	\r\n	Dica: depois de baixar a lista de palavras, você pode melhorá-la com a opção -w\r\n"
    )

    filedown = input("> Digite o número: ")
    filedown.isdigit()
    while filedown.isdigit() == 0:
        print("\r\n[-] Escolha errada. ")
        filedown = input("> Digite o número: ")
    filedown = str(filedown)
    while int(filedown) > 38 or int(filedown) < 0:
        print("\r\n[-] Escolha errada. ")
        filedown = input("> Digite o número: ")
    filedown = str(filedown)

    download_wordlist_http(filedown)
    return filedown


def download_wordlist_http(filedown):
    """ faz o download HTTP de uma lista de palavras """

    mkdir_if_not_exists("dictionaries")

    # List of files to download:
    arguments = {
        1: (
            "Moby",
            (
                "mhyph.tar.gz",
                "mlang.tar.gz",
                "moby.tar.gz",
                "mpos.tar.gz",
                "mpron.tar.gz",
                "mthes.tar.gz",
                "mwords.tar.gz",
            ),
        ),
        2: ("afrikaans", ("afr_dbf.zip",)),
        3: ("american", ("dic-0294.tar.gz",)),
        4: ("aussie", ("oz.gz",)),
        5: ("chinese", ("chinese.gz",)),
        6: (
            "computer",
            (
                "Domains.gz",
                "Dosref.gz",
                "Ftpsites.gz",
                "Jargon.gz",
                "common-passwords.txt.gz",
                "etc-hosts.gz",
                "foldoc.gz",
                "language-list.gz",
                "unix.gz",
            ),
        ),
        7: ("croatian", ("croatian.gz",)),
        8: ("czech", ("czech-wordlist-ascii-cstug-novak.gz",)),
        9: ("danish", ("danish.words.gz", "dansk.zip")),
        10: (
            "databases",
            ("acronyms.gz", "att800.gz", "computer-companies.gz", "world_heritage.gz"),
        ),
        11: (
            "dictionaries",
            (
                "Antworth.gz",
                "CRL.words.gz",
                "Roget.words.gz",
                "Unabr.dict.gz",
                "Unix.dict.gz",
                "englex-dict.gz",
                "knuth_britsh.gz",
                "knuth_words.gz",
                "pocket-dic.gz",
                "shakesp-glossary.gz",
                "special.eng.gz",
                "words-english.gz",
            ),
        ),
        12: ("dutch", ("words.dutch.gz",)),
        13: (
            "finnish",
            ("finnish.gz", "firstnames.finnish.gz", "words.finnish.FAQ.gz"),
        ),
        14: ("french", ("dico.gz",)),
        15: ("german", ("deutsch.dic.gz", "germanl.gz", "words.german.gz")),
        16: ("hindi", ("hindu-names.gz",)),
        17: ("hungarian", ("hungarian.gz",)),
        18: ("italian", ("words.italian.gz",)),
        19: ("japanese", ("words.japanese.gz",)),
        20: ("latin", ("wordlist.aug.gz",)),
        21: (
            "literature",
            (
                "LCarrol.gz",
                "Paradise.Lost.gz",
                "aeneid.gz",
                "arthur.gz",
                "cartoon.gz",
                "cartoons-olivier.gz",
                "charlemagne.gz",
                "fable.gz",
                "iliad.gz",
                "myths-legends.gz",
                "odyssey.gz",
                "sf.gz",
                "shakespeare.gz",
                "tolkien.words.gz",
            ),
        ),
        22: ("movieTV", ("Movies.gz", "Python.gz", "Trek.gz")),
        23: (
            "music",
            (
                "music-classical.gz",
                "music-country.gz",
                "music-jazz.gz",
                "music-other.gz",
                "music-rock.gz",
                "music-shows.gz",
                "rock-groups.gz",
            ),
        ),
        24: (
            "names",
            (
                "ASSurnames.gz",
                "Congress.gz",
                "Family-Names.gz",
                "Given-Names.gz",
                "actor-givenname.gz",
                "actor-surname.gz",
                "cis-givenname.gz",
                "cis-surname.gz",
                "crl-names.gz",
                "famous.gz",
                "fast-names.gz",
                "female-names-kantr.gz",
                "female-names.gz",
                "givennames-ol.gz",
                "male-names-kantr.gz",
                "male-names.gz",
                "movie-characters.gz",
                "names.french.gz",
                "names.hp.gz",
                "other-names.gz",
                "shakesp-names.gz",
                "surnames-ol.gz",
                "surnames.finnish.gz",
                "usenet-names.gz",
            ),
        ),
        25: (
            "net",
            (
                "hosts-txt.gz",
                "inet-machines.gz",
                "usenet-loginids.gz",
                "usenet-machines.gz",
                "uunet-sites.gz",
            ),
        ),
        26: ("norwegian", ("words.norwegian.gz",)),
        27: (
            "places",
            (
                "Colleges.gz",
                "US-counties.gz",
                "World.factbook.gz",
                "Zipcodes.gz",
                "places.gz",
            ),
        ),
        28: ("polish", ("words.polish.gz",)),
        29: (
            "random",
            (
                "Ethnologue.gz",
                "abbr.gz",
                "chars.gz",
                "dogs.gz",
                "drugs.gz",
                "junk.gz",
                "numbers.gz",
                "phrases.gz",
                "sports.gz",
                "statistics.gz",
            ),
        ),
        30: ("religion", ("Koran.gz", "kjbible.gz", "norse.gz")),
        31: ("russian", ("russian.lst.gz", "russian_words.koi8.gz")),
        32: (
            "science",
            (
                "Acr-diagnosis.gz",
                "Algae.gz",
                "Bacteria.gz",
                "Fungi.gz",
                "Microalgae.gz",
                "Viruses.gz",
                "asteroids.gz",
                "biology.gz",
                "tech.gz",
            ),
        ),
        33: ("spanish", ("words.spanish.gz",)),
        34: ("swahili", ("swahili.gz",)),
        35: ("swedish", ("words.swedish.gz",)),
        36: ("turkish", ("turkish.dict.gz",)),
        37: ("yiddish", ("yiddish.gz",)),
    }

    # download the files

    intfiledown = int(filedown)

    if intfiledown in arguments:

        dire = "dictionaries/" + arguments[intfiledown][0] + "/"
        mkdir_if_not_exists(dire)
        files_to_download = arguments[intfiledown][1]

        for fi in files_to_download:
            url = CONFIG["global"]["dicturl"] + arguments[intfiledown][0] + "/" + fi
            tgt = dire + fi
            download_http(url, tgt)

        print("[+] arquivos salvos em " + dire)

    else:
        print("[-] saindo.")


# create the directory if it doesn't exist
def mkdir_if_not_exists(dire):
    if not os.path.isdir(dire):
        os.mkdir(dire)


# the main function
def main():
    """Interface de linha de comando para o app"""

    read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cuppbr.cfg"))

    parser = get_parser()
    args = parser.parse_args()

    if not args.quiet:
        print_cow()

    if args.version:
        version()
    elif args.interactive:
        interactive()
    elif args.download_wordlist:
        download_wordlist()
    elif args.alecto:
        alectodb_download()
    elif args.improve:
        improve_dictionary(args.improve)
    else:
        parser.print_help()


# Separate into a function for testing purposes
def get_parser():
    """Cria e retorna um analisador (argparse.ArgumentParser instance) para main()
    usar"""
    parser = argparse.ArgumentParser(description="Common User Passwords Profiler - Versão Brasil")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Perguntas interativas para criação de perfil de senha de usuário",
    )
    group.add_argument(
        "-w",
        dest="improve",
        metavar="FILENAME",
        help="Use esta opção para melhorar o dicionário existente,"
        " ou saída WyD.pl para fazer algum pwnsauce",
    )
    group.add_argument(
        "-l",
        dest="download_wordlist",
        action="store_true",
        help="Baixar grandes listas de palavras do repositório",
    )
    group.add_argument(
        "-a",
        dest="alecto",
        action="store_true",
        help="Analisar nomes de usuário e senhas padrão diretamente"
        "de Alecto DB."
        " bancos de dados de Phenoelit e CIRT que foram fundidos"
        " e melhorado",
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Mostra a versão do programa."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Modo quiet (não mostra o banner)"
    )

    return parser


if __name__ == "__main__":
    main()
