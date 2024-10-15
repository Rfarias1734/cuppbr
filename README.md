# CUPPBr - Common User Passwords Profiler Brasil


## About (Sobre)

  A forma mais comum de autenticação é a combinação de um nome de usuário
  e uma senha ou frase secreta. Se ambos corresponderem aos valores armazenados em uma
  tabela armazenada localmente, o usuário é autenticado para uma conexão. A força da senha é
  uma medida da dificuldade envolvida em adivinhar ou quebrar a senha
  por meio de técnicas criptográficas ou testes automatizados baseados em bibliotecas de
  valores alternativos.

  Uma senha fraca pode ser muito curta ou usar apenas caracteres alfanuméricos,
  tornando a descriptografia simples. Uma senha fraca também pode ser facilmente
  adivinhado por alguém que perfila o usuário, como aniversário, apelido, endereço,nome 
  de um animal de estimação ou parente, ou uma palavra comum como Deus, amor, 
  dinheiro ou senha.

  É por isso que o CUPP nasceu, e pode ser usado em situações como
  testes de penetração ou investigações de crimes forenses.
  
  O CUPPBr é criado por entusiastas da área que buscam uma maior performance da ferramenta
  para o público brasileiro.


Requirements
------------

Você precisa do Python 3 para executar o CUPPBr.

Quick start
-----------

    $ python3 cuppbr.py -h

## Options

  Uso: cuppbr.py [OPTIONS]

        -h      este menu

        -i      Interagir com perguntas para criar o perfil de senha do usuário

        -w      Use esta opção para criar o perfil a partir de um dicionário existente,
                ou saída WyD.pl.

        -l      Realizar Download de wordlists do repositorio.

        -a      Analise nomes de usuário e senhas padrão diretamente do Alecto DB.
                O Projeto Alecto usa bancos de dados purificados de Phenoelit e CIRT que foram mesclados e aprimorados.

        -v      Versão do programa



## Configuration

   CUPPBr tem o arquivo de configuração cuppbr.cfg com instruções.


## License

  Este programa é um software livre; você pode redistribuí-lo e/ou modificá-lo
  sob os termos da GNU General Public License conforme publicada por
  a Fundação do Software Livre; quer a versão 3 da Licença, ou
  qualquer versão posterior.

  Este programa é distribuído na esperança de que seja útil,
  mas SEM QUALQUER GARANTIA; sem mesmo a garantia implícita de
  COMERCIALIZAÇÃO ou ADEQUAÇÃO A UM DETERMINADO FIM. Veja o
  Licença Pública Geral GNU para mais detalhes.

  Consulte './LICENSE' para obter mais informações.

## Github import

Este projeto foi adaptado e customizado a partir do 
https://github.com/Mebus/cupp por Mebus de:  
http://www.remote-exploit.org/content/cupp-3.0.tar.gz  
http://www.remote-exploit.org/articles/misc_research__amp_code/index.html  
para incentivar o desenvolvimento da ferramenta.

## Original author

  Muris Kurgas aka j0rgan  
  j0rgan@remote-exploit.org  
  http://www.remote-exploit.org  
  http://www.azuzi.me  
  
  
## Contributors (CUPPBr.py)

  * Ramon Neves  
      https://github.com/Rfarias1734 
    
  * Nilton Vicente  
      https://github.com/nextroid

  * Alex Augusto

  * Bruno Silva

  * Ramon Marsal

  * Allan Felicio
      https://github.com/AllanFelicio 

  * Auber Maroneze


## Contributors (CUPP.py)

  * Bosko Petrovic aka bolexxx  
  bole_loser@hotmail.com  
  http://www.offensive-security.com  
  http://www.bolexxx.net  

  * Mebus  
    https://github.com/Mebus/  

  * Abhro  
    https://github.com/Abhro/  

  * Andrea Giacomo  
    https://github.com/codepr

  * quantumcore  
    https://github.com/quantumcore
    
------------------------------------------------------------------------

[![Build Status](https://travis-ci.org/Mebus/cupp.svg?branch=master)](https://travis-ci.org/Mebus/cupp)
[![Coverage Status](https://coveralls.io/repos/github/Mebus/cupp/badge.svg)](https://coveralls.io/github/Mebus/cupp)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a578dde078ef481e97a0e7eac0c8d312)](https://app.codacy.com/app/Mebus/cupp?utm_source=github.com&utm_medium=referral&utm_content=Mebus/cupp&utm_campaign=Badge_Grade_Dashboard)
[![Rawsec's CyberSecurity Inventory](https://inventory.raw.pm/img/badges/Rawsec-inventoried-FF5050_plastic.svg)](https://inventory.raw.pm/)
