Aventura Aérea 🚀

Bem-vindo ao Aventura Aérea! Um jogo de desvio de obstáculos inspirado no clássico Flappy Bird, mas com uma temática espacial. Desenvolvido em Python com a biblioteca Pygame, este projeto é perfeito para entusiastas de jogos casuais e estudantes de programação.

📜 Sobre o Jogo

O objetivo é simples: guie sua nave através de um campo de asteroides perigoso pelo maior tempo possível. A cada par de asteroides que você ultrapassa, sua pontuação aumenta. Mas cuidado, qualquer colisão resultará no fim da partida!

✨ Funcionalidades

Menu Interativo: Uma tela de início permite que você insira um nickname para competir.

Placar de Sessão: O jogo mantém um placar com as três melhores pontuações da sessão atual, que é zerado ao fechar o jogo.

Controles Simples: Basta usar a tecla ESPAÇO ou SETA PARA CIMA para impulsionar a nave.

Compilado e Pronto para Jogar: Um arquivo executável (.exe) está disponível para jogar instantaneamente no Windows, sem necessidade de instalação.

🕹️ Como Jogar

Existem duas maneiras de aproveitar o Aventura Aérea:

Opção 1: Usando o Executável (Recomendado para Jogadores)

Esta é a forma mais fácil e rápida.

Vá para a pasta dist ou onde você encontrou o arquivo FlappyBird.exe.

Dê um duplo clique no arquivo FlappyBird.exe.

O jogo irá iniciar. Divirta-se!

Opção 2: Executando a partir do Código-Fonte (Para Desenvolvedores)

Se você tem Python instalado e quer ver o código funcionando ou modificá-lo, siga estes passos:

Pré-requisitos:

Python 3.8+ instalado.

A biblioteca pygame instalada. Se não tiver, abra um terminal (CMD ou PowerShell) e digite:

pip install pygame


Clone ou baixe este repositório:

git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio


Execute o jogo:
No terminal, dentro da pasta do projeto, execute o comando:

python FlappyBird.py


🛠️ Como Compilar seu Próprio Executável

Se você fez alterações no código .py e quer gerar um novo arquivo .exe, precisará da ferramenta PyInstaller.

Instale o PyInstaller:
No terminal, digite:

pip install pyinstaller


Execute o Comando de Compilação:
Navegue até a pasta raiz do projeto com o terminal e execute o seguinte comando:

pyinstaller --onefile --windowed --add-data "imgs;imgs" "FlappyBird.py"


--onefile: Agrupa tudo em um único arquivo .exe.

--windowed: Remove a janela de console preta que aparece atrás do jogo.

--add-data "imgs;imgs": Comando crucial que inclui a sua pasta de imagens dentro do executável.

Encontre seu arquivo:
Após o processo, seu novo executável estará na pasta dist que foi criada.

📂 Estrutura do Projeto

.
├── FlappyBird.py       # O código-fonte principal do jogo.
├── FlappyBird.exe      # O arquivo executável para Windows.
├── imgs/               # Pasta contendo todos os recursos gráficos.
│   ├── base.png
│   ├── bg.png
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   └── pipe.png
└── README.md           # Este arquivo.


Desenvolvido com ❤️ por [Seu Nome/Nick]. Sinta-se à vontade para contribuir, sugerir melhorias ou simplesmente se divertir!
