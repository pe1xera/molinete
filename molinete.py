#!/usr/bin/python
# -*- coding: utf-8 -*-
import crypt
import sys
import time

def exibirBanner():
    print r"""  
		 _p
 _______________/ |\___\\ ___________o____________o___________o_
()___.'---'.____\__/____)============'============'==========='=D
                                                                |
                                                                |
        █▀▄▀█ ████▄ █    ▄█    ▄   ▄███▄     ▄▄▄▄▀ ▄███▄        |
        █ █ █ █   █ █    ██     █  █▀   ▀ ▀▀▀ █    █▀   ▀       |
        █ ▄ █ █   █ █    ██ ██   █ ██▄▄       █    ██▄▄         |
        █   █ ▀████ ███▄ ▐█ █ █  █ █▄   ▄▀   █     █▄   ▄▀      |
           █            ▀ ▐ █  █ █ ▀███▀    ▀      ▀███▀        |
          ▀                 █   ██                              | 
                                                                |
                     "A Hash-cracking Tool"                     |
                                                                |
                                                                |
                                                               _|__
                                                              / ' o\ 
                                                             / `   '\ 
                                                            /| /__\`|\ 
Modo de uso:                                                '-\ `  /-/
molinete.py <sua wordlist>                       by pe1xera   ///\\\ 
                                                             '-'--'-' 
"""
    return

def exibirAjuda():
    ajuda = r"""
		 _p
 _______________/ |\___\\ ___________o____________o___________o_
()___.'---'.____\__/____)============'============'==========='=D
                                                                |
                                                                |
        █▀▄▀█ ████▄ █    ▄█    ▄   ▄███▄     ▄▄▄▄▀ ▄███▄        |
        █ █ █ █   █ █    ██     █  █▀   ▀ ▀▀▀ █    █▀   ▀       |
        █ ▄ █ █   █ █    ██ ██   █ ██▄▄       █    ██▄▄         |
        █   █ ▀████ ███▄ ▐█ █ █  █ █▄   ▄▀   █     █▄   ▄▀      |
           █            ▀ ▐ █  █ █ ▀███▀    ▀      ▀███▀        |
          ▀                 █   ██                              | 
                                                                |
                     "A Hash-cracking Tool"                     |
                                                                |
                                                                |
                                                               _|__
                                                              / ' o\ 
                                                             / `   '\ 
                                                            /| /__\`|\ 
    Uso:                                                    '-\ `  /-/
      molinete.py <wordlist>                     by pe1xera   ///\\\ 
                                                             '-'--'-' 
    Argumentos:
      <wordlist>    Caminho para o arquivo de wordlist
    
    Parâmetros:
      -h, --help    Exibir esta mensagem de ajuda
    
    Descrição:
      Este programa tenta quebrar um hash fornecido usando uma lista de palavras (wordlist). 
      Solicitará ao usuário um hash completo, incluindo o ID do hash, o salt, e o hash em si.
    
    Exemplo:
      python molinete.py wordlist.txt"""
    print ajuda

def exibirLoading(frames, index, senha):
    sys.stdout.write('\r' + ' ' * 80)
    sys.stdout.write('\r' + 'Testando: [ {} ] - '.format(senha) + frames[index % len(frames)])
    sys.stdout.flush()    

def main():
    if len(sys.argv) != 2:
        exibirBanner()
        return

    if sys.argv[1] in ('-h', '--help'):
        exibirAjuda()
        return

    caminhoWordlist = sys.argv[1]
    exibirBanner()

    try:
        with open(caminhoWordlist, "r") as arquivo:
            # solicitando o hash completo
            hashCompleto = raw_input("_______________________\n> Digite o hash completo:\n")

            # separar o hash completo em idHash, salt e hashEsperado
            partes = hashCompleto.split('$')
            if len(partes) < 4:
                print("> Hash digitado inválido.")
                return

            idHash = '$' + partes[1] + '$'
            salt = partes[2]
            hashEsperado = partes[3]

            # Frames da animação de peixe nadando em ASCII
            frames = [
                "><(((('>",
                " ><(((('>",
                "  ><(((('>",
                " ><(((('>",
            ]

            # Comparando os hashes
            encontrado = False
            frameIndex = 0
	    
	    print "_______________________\n> Fishing those salted sprats..."
            for linha in arquivo:
                senha = linha.strip()
                resultado = crypt.crypt(senha, idHash + salt)
                
                # Exibir a animação de loading
		exibirLoading(frames, frameIndex, senha)
                frameIndex += 1
                time.sleep(0.1)
		
                if resultado == hashCompleto:
                    print("\n_______________________\n> Pescou! Senha encontrada: {}".format(senha))
                    encontrado = True
                    break

            if not encontrado:
                print("\n_______________________\n> Parece que o mar nao esta para peixe. A senha não foi encontrada.")

    except IOError:
        print("> Arquivo {} não encontrado.".format(caminhoWordlist))
    except KeyboardInterrupt:
        print("\n> As vezes, uma pequena pausa traz todas as respostas...")
    except Exception as e:
        print("> Ocorreu um erro: {}".format(e))

if __name__ == "__main__":
    main()

