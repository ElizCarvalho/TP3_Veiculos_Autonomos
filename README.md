#### Instituto Infnet
#### Disicplina: Veículos Autônomos
#### Prof.: M.e. Adalberto Oliveira
#### Teste de Performance 3 - Qst5

crie um nó para o framework ROS utilizando linguagem Python que seja capaz de realizar processamento de imagem e a publicação das coordenadas de um ponto extraído a partir da imagem de um objeto no ambiente, podendo ser sua centroide ou o ponto de contato entre o este objeto e sua superfície de apoio. O nó deverá publicar no tópico /goal uma mensagem do tipo Pose2D, contendo apenas as coordenadas x e y do atributo escolhido, não sendo necessária a publicação de nenhuma imagem (original, máscara ou imagem modificada). A aquisição da imagem poderá ser feita utilizando uma das seguintes opções: leitura de um arquivo estático local; captura de imagens a partir de uma câmera; recebimento de uma publicação vinda de um tópico de imagem. Deverão ser aplicadas técnicas de melhoria de imagem, tais como filtros ou operações morfológicas, de forma a melhorar o processo de extração de atributos.

---

#### Step by step ->  Criação/Teste de execução: 

#### % Etapa 1: Criando o pacote cv_coord_centroid e script de extração de coordenada da centróide
```shell
$ initros1
$ source ~/catkin_ws/devel/setup.bash
$ cd ~/catkin_ws/src/
$ catkin_create_pkg cv_coord_centroid rospy geometry_msgs
$ cd cv_coord_centroid/
$ mkdir images
$ cd ~/catkin_ws/
$ catkin_make
```
#### % Etapa 2: Como não o ambiente de trabalho não dispões de câmera, será lida uma imagem estática para realização do processamento.

##### Imagem 1: 
<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/images/caixa-de-som-1.jpg" width=300/>

##### Imagem 2:
<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/images/caixa-de-som-2.jpg" width=300/>

```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
$ cd ~/catkin_ws/src/cv_coord_centroid/src/
$ gedit ec_publisher_static_image.py
$ chmod +x ec_publisher_static_image.py
$ cd ~/catkin_ws/
$ catkin_make
$ rosrun cv_coord_centroid ec_publisher_static_image.py
```
[ec_publisher_static_image.py](https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/src/ec_publisher_static_image.py)

#### % Etapa 3: Utilizar o calibrador (código cedido pelo professor) para exrair os valores a serem utilizados para criação da máscara (binarização da imagem)
```shell
$ initros1
$ source ~/aula/catkin_ws/devel/setup.bash
```
[calibrador_hsv_yaml_ROS.py](https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/src/calibrador_hsv_yaml_ROS.py)

*- Enter file name: jbl*<br/>
*- Enter topic name: camera_frames*<br/>
*Output: ['num_masks: 1\n', ' low: [0, 18, 0], ' high: [255, 255, 255]\n]*<br/>

<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/prints/evidencia_mascara_img1.png" width=600/>

#### % Etapa 4: Implementação do script que irá:
#####	4.1- Ler a imagem do tópico
#####	4.2- Criar a máscara com os valores de low e high adquiridos na etapa anterior
#####	4.3- Aplicar filtros para melhorar a visualização. 
- Foi aplicado o filtro GAUSIANO para remoção de ruídos e DILATE (aumentar a área da imagem), e foi realizada a operação morfológica CLOSE (para remover os 'buracos' pretos de dentro da imagem - consiste numa dilatação (aumentar a área), seguida de erosão (reduir a área)) 
#####	4.4- Extrair a centróide e pegar sua coordenada
#####	4.5- Publicar msg do tipo Pose2D com a coordenada no tópico /goal
```shell
$ cd ~/catkin_ws/src/cv_coord_centroid/src
$ gedit coord_centroid_ecarvalho_DR4_TP3.py
$ chmod +x coord_centroid_ecarvalho_DR4_TP3.py
$ cd ~/catkin_ws/
$ catkin_make
$ rosrun cv_coord_centroid ec_coord_centroid.py
```
[ec_coord_centroid.py](https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/src/ec_coord_centroid.py)

#### Evidências:

<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/prints/evidencia_mascara_img2.png" width=600/>
<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/prints/baundbox-com-centroid_img1.png" width=600/>
<img src="https://github.com/ElizCarvalho/TP3_Veiculos_Autonomos/blob/main/cv_coord_centroid/prints/baundbox-com-centroid_img2.png" width=600/>
