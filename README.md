# tp-02-lab-exp

Trabalho Prático #02 para a disciplina de Laboratório de Experimentação de Software do curso de Engenharia de Software na PUC-Minas.

Aluno: Gabriel Henrique Souza Haddad Campos

Repositório: https://github.com/Haddadson/tp-01-lab-exp

A proposta do trabalho consiste na construção de uma aplicação que efetue consultas com paginação à API do GitHub utilizando GraphQL e Python.
Deve-se minerar dados dos 1000 repositórios mais populares a fim de responder as questões abaixo:

1. Sistemas populares são maduros/antigos?
2. Sistemas populares recebem muita contribuição externa?
3. Sistemas populares lançam releases com frequência?
4. Sistemas populares são atualizados com frequência?
5. Sistemas populares são escritos nas linguagens mais populares?
6. Sistemas populares possuem um alto percentual de issues fechadas?
7. Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

Para respondê-las, será necessário realizar uma análise quantitativa dos dados obtidos para identificar os valores correspondentes às métricas estipuladas.

## Execução

Para execução do script, é necessário instalar as dependências utilizando os comandos abaixo:

> pip install requests

> pip install dump

> pip install loads

> pip install python-dateutil

Também é necessário inserir um token pessoal de desenvolvedor para acesso à API do GitHub no trecho indicado no código.

Após isso, basta executar o script e o arquivo CSV "ResultadoSprint2.csv" será criado na mesma pasta.
Durante a execução, serão exibidos logs informando o progresso, erros e retentativas das chamadas.
