
![molinete_capa](https://github.com/user-attachments/assets/30ace0c4-8bc2-437b-9afc-755726889a3b)

# Introdução

O processo de quebra de hashes pode ser um grande atraso enquanto se realiza um pentest, especialmente quando o hash tem sua complexidade aumentada com aquela boa e velha pitada de Salt, um dado aleatório que é usado para gerar uma saída totalmente diferente daquela que a função de hash geraria por padrão, somente com a senha.

Diante disso, desenvolvi uma ferramenta em Python - bastante simples, na verdade - que tenta agilizar nossas vidas. O `molinete`, como apelidei a ferramenta, utiliza uma wordlist fornecida pelo usuário e, por meio da função crypt, testa diversas senhas até encontrar a correspondência exata com o hash fornecido.

Modo de uso: `molinete.py <wordlist>`

# Funcionamento

A ferramenta, em questão, lê o hash digitado pelo usuário e o divide em três partes, conforme o padrão aceito pela função crypt: ID, Salt e Hash, mostrando na imagem abaixo. Ela usa o caractere de cifrão ($) para separar os pedaços do hash e continuar com os outros procedimentos. Após a divisão, o programa cria o hash de cada uma das senhas na wordlist usada como argumento, com base no tipo de algoritmo do hash passado e no salt obtido.

![Explicações-Molinete1](https://github.com/user-attachments/assets/38c9ace6-05f4-4a90-8af1-570c4a80680b)

Assim, caso o hash final gerado de qualquer uma das senhas da lista de palavras seja igual ao hash digitado pelo usuário, sabe-se que aquela é a senha correta.

# Princípios

A ferramenta se baseia na função `crypt`, do Python, que permite gerar hashes a partir de uma senha e um salt específicos. A `crypt` utiliza o algoritmo de hashing especificado pelo ID do hash fornecido pelo usuário. Isso garante que a ferramenta possa lidar com diferentes tipos de hashes, como MD5, SHA-256, entre outros, dependendo do ID e do salt extraídos do hash completo.

Para facilitar a utilização, o código foi estruturado para receber o caminho da wordlist como argumento e o hash completo diretamente do usuário. A animação de loading, que mostra um peixe nadando, torna o processo mais amigável e menos tedioso, exibindo também qual senha está sendo testada no momento.

Para facilitar ainda mais o entendimento, pode-se usar os parâmetros `-h` e `--help` para mostrar um pequeno manual do script. Uma outra propriedade deste código, que acho interessante ressaltar, é o uso de threading. Enquanto uma thread testa as senhas, a outra mantém o usuário informado com a animação, sem bloquear a execução principal do programa, de modo que uma coisa não interfere na outra.

# Disclaimer

Certamente, há uma série de ferramentas muito melhores que essa disponíveis. Ainda assim, a fim de praticar os meus próprios conhecimentos, a fim de ter uma ferramenta confiável em meu arsenal e, principalmente, a fim de fazer mais ASCII Arts, achei válido criar e compartilhar este script por aqui.

No mais, fico completamente aberto às sugestões e críticas.

Goodbye, little sprat! 'Til next time!  `><((((('>`
