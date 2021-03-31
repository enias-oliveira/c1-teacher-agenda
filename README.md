# Teacher Flask API
 
Um aplicativo para um professor particular para organizar os agendamentos de seus alunos, já que atualmente o tempo que o mesmo gasta para revisar e fazer anotações está o prejudicando bastante.

Seu cliente enviou o seguinte texto para explicar o que espera do produto final. 

Preciso de um aplicativo que me ajude a me organizar. Meu nome é Izabel Rainha de Portugal, sou professora de matemática, física e química. Pela alta quantidade de agendamentos, a boa e velha agenda não tem dado mais conta de me ajudar com a organização das datas, além disso, é tanta papelada para cada aluno que as vezes acabo me perdendo. Hoje tenho mais de 45 alunos que preciso encaixar em horários sempre muito apertados, muitas vezes gasto muito tempo com esse tipo de atividade, porque preciso fazê-la algumas vezes por dia. 

Seria interessante poder saber quais horários estão disponíveis para certo dia, quais alunos estão agendados para certo dia, assim como ter acesso a descrição que faço para cada aula, assim consigo saber exatamente o que foi visto na última aula, e organizar as anotações para as próximas.

- Para modularizar o código, criei um diretório de serviços para separar as funcionalidades relacionadas ao csv
- Para gravar um agendamento é necessário um id novo, criei uma função que pega o ultimo agendamento registrado, pega o seu id e retorna esse id incrementado. 
- Antes de marcar um agendamento é preciso verificar se o horário está disponível. Há duas condições em relação as datas, o horário precisa estar live e precisar ser entre as 8 e 23 horas. Essas condições serão encapsuladas em uma função que verifica a disponibilidade do horário. 


Entradas e saídas
Input1
Requisição POST para /appointment - Agendar Aula

POST /appointment HTTP/1.1
Content-Type: application/json
Host: localhost:5000
Content-Length: 296

{
	"date": "2021-07-24 14:22:00",
	"name": "Son Goku",
	"school-subjects": "Matemática",
	"difficulty": "Não consegue entender como escalonar matrizes",
	"class-number": 3,
	"_growth": "Agora o aluno já entendeu que sistemas de equações podem ser representado por matrizes"
}
Output1
Resposta do servidor

{
	"id": 1,
	"date": "2021-07-24 14:00:00",
	"name": "Son Goku",
	"school-subjects": "Matemática",
	"difficulty": "Não consegue entender como escalonar matrizes",
	"class-number": 3,
	"_growth": "Agora o aluno já entendeu que sistemas de equações podem ser representado por matrizes"
}
Input2
Requisição GET para /appointment - Listar Aulas

GET /appointment HTTP/1.1
Host: localhost:5000
Output2
Resposta do servidor

[
  {
    "id": 1,
    "date": "2021-08-22 09:00:00",
    "name": "Son Goku",
    "school-subjects": "Matemática",
    "difficulty": "Não consegue entender como escalonar matrizes",
    "class-number": 3,
    "_growth": "Agora o aluno já entendeu que sistemas de equações podem ser representado por matrizes"
  },
  {
    "id": 2,
    "date": "2021-12-27 11:00:00",
    "name": "Naruto Uzumaki",
    "school-subjects": "Física",
    "difficulty": "Dificuldade em entender as propriedades das ondas eletromagnéticas",
    "class-number": 0,
  },
  {
    "id": 3,
    "date": "2021-10-01 23:00:00",
    "name": "Saitama",
    "school-subjects": "Química",
    "difficulty": "Não entende a condutibilidade da água",
    "class-number": 3,
    "_growth": "Agora o aluno já entendeu como acontece uma reação de neutralização"
  }
]
Input3
Requisição GET para /appointment/available_times_on_the_day?date=02012021 - Janelas de horário disponíveis em certa data

GET /appointment/available_times_on_the_day?date=02012021 HTTP/1.1
Host: localhost:5000
Output3
Resposta do servidor

{
  "available-times": ["08:00-11:00", "15:00-16:00", "21:00-23:00"]
}
Input4
Requisição PATCH para /appointment/1 - Alterar data/horário do agendamento

PATCH /appointment/1 HTTP/1.1
Content-Type: application/json
Host: localhost:5000
Content-Length: 54

{
	"date": "2021-07-21 08:00:00"
}
Output4
Resposta do servidor

{
	"id": 1,
	"date": "2021-07-21 08:00:00",
	"name": "Son Goku",
	"school-subjects": "Matemática",
	"difficulty": "Não consegue entender como escalonar matrizes",
	"class-number": 3,
	"_growth": "Agora o aluno já entendeu que sistemas de equações podem ser representado por matrizes"
}
 

Input5
Requisição DELETE para /appointment/3 - Deletar agendamento

DELETE /appointment/3 HTTP/1.1
Host: localhost:5000
Output5
Resposta do servidor

HTTP/1.0 204 NO-CONTENT
Access-Control-Allow-Origin: *
Server: Werkzeug/1.0.1 Python/3.8.5
Date: Wed, 05 Sep 2020 11:53:53 GMT
