#### Instituto Infnet
#### Disicplina: Veículos Autônomos
#### Prof.: M.e. Adalberto Oliveira
#### Teste de Performance 1 - Qst6

Implemente um nó de controle para o simulador TurtleSim do framework ROS, que seja capaz de realizar regulação de postura a partir da coordenada em que se encontra para uma coordenada qualquer, passada pelo operador. A solução deverá receber a coordenada de destino por meio de uma publicação no tópico /goal.

---

#### Step by step ->  Criação/Teste de execução: 

##### Terminal 1 (ROSCORE ROS1):
```shell
$ initros1
$ roscore
```
##### Terminal 2 (Iniciando o turtlesim):
```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
$ rosrun turtlesim turtlesim_node
```
![alt text](https://github.com/ElizCarvalho/TP1_Veiculos_Autonomos/blob/main/evidencia_terminal_2.png "Turtlesim")
##### Terminal 3 (Configurando turtlesim e publicando no tópico /goal):
```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
$ rosservice call /turtle1/set_pen "{r: 255, g: 255, b: 0, width: 3, 'off': 0}"
$ rostopic pub -r 10 /goal geometry_msgs/Pose2D "{x: 9.0, y: 2.0, theta: 1.57}"
```
#### Terminal 4 (Conferindo a publicação no tópico /goal):
```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
$ rostopic list 
$ rostopic echo /goal
```
![alt text](https://github.com/ElizCarvalho/TP1_Veiculos_Autonomos/blob/main/evidencia_terminal_4.png "Topico /goal")
#### Terminal 5 (Criando o pacote turtle_regulation e script de regulação):
```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
$ cd ~/aula/catkin_ws/src/
$ catkin_create_pkg turtle_regulation rospy geometry_msgs
$ cd ~/aula/catkin_ws/src/turtle_regulation/src/
$ gedit regulation_elizabeth_carvalho_DR4_TP1.py
$ chmod +x regulation_elizabeth_carvalho_DR4_TP1.py
$ cd ~/aula/catkin_ws/
$ catkin_make
$ rosrun turtle_regulation regulation_elizabeth_carvalho_DR4_TP1.py
```
![alt text](https://github.com/ElizCarvalho/TP1_Veiculos_Autonomos/blob/main/evidencia_terminal_5.png "Regulação de Postura")









