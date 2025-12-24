
![molinete_capa](https://github.com/user-attachments/assets/30ace0c4-8bc2-437b-9afc-755726889a3b)

# Introdução

O processo de quebra de hashes pode ser um grande atraso enquanto se realiza um pentest, especialmente quando o hash tem sua complexidade aumentada com aquela boa e velha pitada de Salt, um dado aleatório que é usado para gerar uma saída totalmente diferente daquela que a função de hash geraria por padrão, somente com a senha.

# 🎣 Molinete V2.0 (Atlantico)

A ferramenta agora está mais robusta. Diferentemente da primeira versão, o Molinete agora utiliza Multiprocessing (múltiplos núcleos da CPU) para "puxar a rede" com muito mais força, testando diversas senhas da sua wordlist até encontrar a correspondência exata, seja em hashes estruturados ou naqueles hexadecimais puros que encontramos em bancos de dados.

Modo de uso: `molinete.py <wordlist> <hash>`

# Funcionamento

A ferramenta lê o hash fornecido e, inteligentemente, identifica o tipo de "peixe" que está na rede.
1. Modo Automático: Se o hash segue o padrão Unix (com os separadores $), o programa o divide automaticamente em ID, Salt e Hash. Ele reconhece desde o clássico MD5 até o pesado Bcrypt ($2a$, $2b$), que antes passava direto pela rede.
2. Modo Salt Externo: Para aqueles casos onde o Salt não vem grudado no hash (comum em dumps de SQL), adicionei o parâmetro --salt. Assim, o programa concatena o salt especificado com cada senha da lista para gerar o hash SHA-256 correspondente e comparar os resultados.

![Explicações-Molinete1](https://github.com/user-attachments/assets/38c9ace6-05f4-4a90-8af1-570c4a80680b)

Após a identificação, o Molinete divide a wordlist em lotes e os distribui entre os núcleos do seu processador. Se o hash gerado de qualquer senha for igual ao fornecido, sabemos que o peixe foi fisgado.

# Princípios

O Molinete se baseia na biblioteca passlib e no módulo hashlib, permitindo lidar com uma vasta gama de algoritmos como MD5, SHA-256, SHA-512 e o temido Bcrypt.

Para tornar o processo menos tedioso, mantive a interface visual, mas agora com um toque de Verde para facilitar a leitura no escuro do terminal. A animação de "Fisgando" mantém você informado sobre qual senha está passando pelo anzol em tempo real, sem bloquear a execução principal, graças à arquitetura de processos paralelos.

Para os marinheiros de primeira viagem, os parâmetros -h ou --help mostram o manual completo de como operar a ferramenta.

# Disclaimer

Certamente, há uma série de ferramentas muito melhores que essa disponíveis (como o Hashcat ou John the Ripper). Ainda assim, a fim de praticar os meus próprios conhecimentos, a fim de ter uma ferramenta confiável e visualmente coerente em meu arsenal e, principalmente, a fim de fazer mais ASCII Arts, achei válido atualizar e compartilhar este script.

No mais, fico completamente aberto às sugestões e críticas.

Goodbye, little sprat! 'Til next time!  `><((((('>`
