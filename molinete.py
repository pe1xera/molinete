#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import multiprocessing
import signal
import hashlib
import logging
from argparse import ArgumentParser

# Configuração de Cores (Apenas Verde e Reset)
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GREEN = "\033[92m"

# Silencia avisos internos da passlib sobre backends e versões
logging.getLogger("passlib").setLevel(logging.ERROR)

# Tentativa de importar a passlib
try:
    from passlib.hash import sha512_crypt, sha256_crypt, md5_crypt, des_crypt, bcrypt
except ImportError:
    print(f"[!] Erro: Biblioteca 'passlib' não encontrada.")
    print(f"[!] Instale com: pip install passlib bcrypt")
    sys.exit(1)

def exibirBanner():
    # Banner em ASCII puro (Padrão do terminal)
    banner = r"""
         _p
 _______________/ |\___\\ ___________o____________o___________o_
()___.'---'.____\__/____)============'============'==========='==D
                                                                 |
          █▀▄▀█ ████▄  █    ▄█    ▄   ▄███▄      ▄▄▄▄▀ ▄███▄     |
          █ █ █ █    █ █    ██     █  █▀    ▀ ▀▀▀ █    █▀  ▀     |
          █ ▄ █ █    █ █    ██ ██   █ ██▄▄        █    ██▄▄      |
          █    █ ▀████ ███▄ ▐█ █ █  █ █▄    ▄▀   █      █▄  ▀    |
              █            ▀ ▐ █  █ █ ▀███▀     ▀      ▀███▀     |
              ▀                █   ██                            | 
                                                                 |
                      "A Hash-cracking Tool"                     |
                         V2.0 (Atlantico)                        |
                                                                _|__
                                                               / ' o\ 
                                                              / `   '\ 
                                                             /| /__\`|\ 
Modo de uso:                                                 '-\ `  /-/
molinete.py <wordlist> <hash> [params]       by pe1xera        ///\\\ 
                                                              '-'--'-' 
"""
    print(banner)

def exibirAjuda():
    ajuda = f"""
 {C_BOLD}{C_GREEN}Argumentos:{C_RESET}
   <wordlist>       Caminho para o arquivo de dicionário (ex: rockyou.txt)
   <hash>           O hash alvo (entre aspas simples para evitar erros no shell)

 {C_BOLD}{C_GREEN}Parâmetros:{C_RESET}
   -h, --help       Exibir esta mensagem de ajuda
   --salt <salt>    Salt externo para hashes hexadecimais puros (SHA256)

 {C_BOLD}{C_GREEN}Descrição:{C_RESET}
   O Molinete tenta quebrar hashes de duas formas:
   1. Automática: Detecta padrões Unix ($1$, $2a$, $5$, $6$) incluindo Salt e ID.
   2. Manual: Usa o parâmetro --salt para hashes extraídos de bancos de dados.

 {C_BOLD}{C_GREEN}Exemplos:{C_RESET}
   python3 molinete.py lista.txt '$2a$04$I/pbnr37PWok8haJXV17.OHJ...'
   python3 molinete.py lista.txt '70b69f451a771c474...' --salt '_FHJbQP'
"""
    exibirBanner()
    print(ajuda)

def inicializarProcessoFilho():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def identificarTipoHash(hashAlvo):
    try:
        if bcrypt.identify(hashAlvo): return f"{C_BOLD}{C_GREEN}Bcrypt (Blowfish){C_RESET}"
        if sha512_crypt.identify(hashAlvo): return f"{C_BOLD}{C_GREEN}SHA-512 (Unix){C_RESET}"
        if sha256_crypt.identify(hashAlvo): return f"{C_BOLD}{C_GREEN}SHA-256 (Unix){C_RESET}"
        if md5_crypt.identify(hashAlvo): return f"{C_BOLD}{C_GREEN}MD5 (Crypt/Apache){C_RESET}"
        if des_crypt.identify(hashAlvo): return f"{C_BOLD}{C_GREEN}DES (Traditional Unix){C_RESET}"
    except: pass
    return "Desconhecido/Incompatível"

def crackChunk(listaPalavras, hashAlvo, idNucleo, saltExterno=None):
    for i, palavra in enumerate(listaPalavras):
        palavra = palavra.strip()
        
        intervalo = 100 if "$2" in hashAlvo else 500
        if i % intervalo == 0:
            sys.stdout.write(f"\r{C_GREEN}Fisgando:{C_RESET} {palavra[:20]:<20}")
            sys.stdout.flush()

        try:
            if saltExterno:
                teste1 = hashlib.sha256((palavra + saltExterno).encode()).hexdigest()
                teste2 = hashlib.sha256((saltExterno + palavra).encode()).hexdigest()
                if teste1 == hashAlvo.lower() or teste2 == hashAlvo.lower():
                    return palavra
            else:
                if bcrypt.identify(hashAlvo):
                    if bcrypt.verify(palavra, hashAlvo): return palavra
                elif sha512_crypt.identify(hashAlvo):
                    if sha512_crypt.verify(palavra, hashAlvo): return palavra
                elif sha256_crypt.identify(hashAlvo):
                    if sha256_crypt.verify(palavra, hashAlvo): return palavra
                elif md5_crypt.identify(hashAlvo):
                    if md5_crypt.verify(palavra, hashAlvo): return palavra
                elif des_crypt.identify(hashAlvo):
                    if des_crypt.verify(palavra, hashAlvo): return palavra
        except:
            continue
    return None

def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument("wordlist", nargs='?')
    parser.add_argument("hash", nargs='?')
    parser.add_argument("--salt", help="Salt externo para hashes hex puros")
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args()

    if args.help or not args.wordlist or not args.hash:
        exibirAjuda()
        return

    exibirBanner()
    tipoIdentificado = identificarTipoHash(args.hash)

    try:
        print(f"> Preparando as redes para a pesca...")
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as arquivo:
            todasPalavras = arquivo.readlines()
    except Exception as e:
        print(f"> [!] Erro ao abrir a wordlist: {e}")
        return

    numeroNucleos = multiprocessing.cpu_count()
    totalPalavras = len(todasPalavras)
    tamanhoLote = totalPalavras // numeroNucleos
    
    print(f"{C_GREEN}________________________________________________________________{C_RESET}\n")
    print(f"> Alvo: {C_GREEN}{args.hash[:45]}...{C_RESET}")
    print(f"> Espécie identificada: {tipoIdentificado}")
    print(f"> Maré boa! Pescando com {C_GREEN}{numeroNucleos}{C_RESET} núcleos.")
    print(f"{C_GREEN}________________________________________________________________{C_RESET}\n")

    tempoInicio = time.time()
    encontrado = False
    pool = multiprocessing.Pool(processes=numeroNucleos, initializer=inicializarProcessoFilho)

    try:
        lotesTrabalho = [todasPalavras[i:i + tamanhoLote] for i in range(0, totalPalavras, tamanhoLote)]
        resultadosTrabalho = [pool.apply_async(crackChunk, (lote, args.hash, n, args.salt)) 
                             for n, lote in enumerate(lotesTrabalho)]
        
        while not encontrado:
            for r in resultadosTrabalho:
                if r.ready():
                    senhaDescoberta = r.get()
                    if senhaDescoberta:
                        encontrado = True
                        tempoTotal = time.time() - tempoInicio
                        sys.stdout.write("\r" + " " * 60 + "\r")
                        sys.stdout.flush()
                        print(f"{C_BOLD}{C_GREEN}> [!!!] PESCOU! Senha encontrada: {C_RESET}{C_BOLD}{senhaDescoberta}{C_RESET}")
                        print(f"> Tempo de pescaria: {C_GREEN}{tempoTotal:.2f} segundos{C_RESET}")
                        pool.terminate()
                        break
            if all(r.ready() for r in resultadosTrabalho) and not encontrado:
                break
            time.sleep(0.05)

    except KeyboardInterrupt:
        sys.stdout.write("\r" + " " * 60 + "\r")
        print("> [!] O pescador voltou para a costa...")
    finally:
        pool.terminate()
        pool.join()

    if not encontrado and 'senhaDescoberta' not in locals():
        print(f"\n> [-] O mar não está para peixe hoje.")

if __name__ == "__main__":
    main()
