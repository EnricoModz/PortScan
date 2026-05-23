# Port Scanner Python Multithread 🕵️‍♂️🚀

Um scanner de portas TCP ultrarrápido, robusto e eficiente desenvolvido totalmente em Python. Este projeto vai além de um simples verificador de conexões: ele utiliza concorrência (multithreading) para varreduras em alta velocidade, identifica serviços em execução e realiza captura de banners (Banner Grabbing) para revelar detalhes dos servidores.

## 🚀 Funcionalidades

* **Varredura Multithread (Alta Velocidade):** Utiliza `concurrent.futures` com um pool de 50 *workers*, escaneando dezenas de portas simultaneamente e reduzindo o tempo de varredura de minutos para frações de segundo.
* **Identificação Inteligente de Serviços:** Descobre o serviço rodando na porta consultando o Sistema Operacional local e possui um sistema de *fallback* (Plano B) baseado em um dicionário próprio para garantir que portas conhecidas nunca passem despercebidas.
* **Banner Grabbing (Captura de Banner):** "Escuta" ativamente a porta após a conexão para capturar a mensagem de boas-vindas e a versão exata do software do servidor (incluindo táticas de requisição `HEAD` para instigar servidores HTTP/Proxy tímidos).
* **Geração de Relatório e Histórico:** Registra automaticamente todas as portas abertas e banners encontrados em um arquivo `relatorio_varredura.txt`. Utiliza o modo *append* para preservar varreduras antigas e construir um histórico contínuo de testes.
* **Resumo Detalhado:** Ao final da execução, exibe o total de portas abertas, fechadas e o tempo preciso gasto na operação.

## 🎥 Demonstração

https://github.com/user-attachments/assets/e2c374a0-23cb-40b5-af16-e1812fdba1d4



## 🛠️ Pré-requisitos

Tudo o que você precisa é ter o **Python 3.x** instalado em sua máquina. O projeto foi construído puramente com bibliotecas nativas do Python (`socket`, `time`, `concurrent.futures`), caracterizando **dependência zero** de pacotes externos.

## 💻 Como usar

Pelo terminal, navegue até a pasta onde o script está salvo e execute o arquivo Python. O script é totalmente interativo e solicitará os parâmetros de varredura.

**Executando o script:**
```bash
python port_scanner.py
Exemplo de Interação e Saída no Terminal:

Plaintext
Digite o IP alvo: scanme.nmap.org
Digite até qual porta deseja escanear: 100

Porta 22 ABERTA - Serviço: ssh | Banner: SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2
Porta 80 ABERTA - Serviço: http | Banner: HTTP/1.1 200 OK

----------------------------------------
=== RESUMO FINAL ===
Total de portas abertas: 2
Total de portas fechadas: 98
Tempo total de execução: 0.25 segundos
Após a execução, um arquivo chamado relatorio_varredura.txt será criado ou atualizado no mesmo diretório contendo o registro completo da operação.

👨‍💻 Criadores
Este projeto foi desenvolvido por:

[EnricoModz] - [https://github.com/EnricoModz]
[CHOQUE4399] - [https://github.com/CHOQUE4399?tab=followers]
