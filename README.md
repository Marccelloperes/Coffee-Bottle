# Coffee-Bottle

<h1> Trabalho de Conclusão de curso Iot_IFESP</h1>
<h2>Prof. Dr. Gustavo Voltani von Atzingen </h2>
<h3>Alunos:</h3>
<h3>Eraldo Gonçalves Junior</h3>
<h3>Marccello Peres</h3>

<h2>Projeto: Construção de uma Garrafa de Café Baseado em Iot</h2>

O projeto serve como um controlador de uma garrafa de café inteligente baseado nos conceitos de IOT.

O controlador exibe a temperatura do líquido na tela LCD, a temperatura é captada por sensor submerso no líquido.
A placa Galileo funciona ao mesmo tempo como slave e server. A temperatura é enviada para o servidor MQTT que retorna para a placa que, processa a informação, retorna os dados para o servidor MQTT que envia novamente para a placa publicando os dados ao usuário.

O sistema libera o líquido por duas formas:
<ul>
  <li>Sensor de IR de proximidade</li>
  <li>Solicitação via WEB</li>
</ul>
Quando solicitado mediante uma das formas acima o relê ativa a bomba air pump que bombeia o líquido.
