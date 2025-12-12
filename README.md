# AWS_Proyecto_Observabilidad
Repositorio sobre el proyecto de observabilidad en la nube de Amazon Web Services.
El proyecto se inicia configurando la instancia de EC2 que se desea utilizar, instancia la cual corresponde a nuestro servidor y es donde se alojara el nginx que utilizaremos como pagina web en la cual los clientes se loggeran. Sin embargo, antes de empezar a activar servicios es importante configurar y establecer la seguridad, para esto primero se crea una persona, para no exponer al root user y luego se asignan roles, que permitan activar servicios y permitir la comunicación entre ellos.

Asi como se deben crear roles para conservar la seguridad y permitir un flujo de trabajo, se deben habilitar diferentes reglas de seguridad en los grupos de seguridad de la instancia para permitir el trafico de datos en las diferentes direcciones.



<img width="818" height="92" alt="Captura desde 2025-12-02 21-03-20" src="https://github.com/user-attachments/assets/1bd421ad-4585-4bad-ba3e-70d563ef4431" />




Es importante tener en cuenta que es necesario habilitar la instancia como una vpc para poder tener subredes publicas y privadas, publicas pues es donde se alojaran los servicios al publico y privadas donde se alojaran los servicios que solo necesitan información del exterior pero que no se pueden acceder desde internet.

Una vez creada la instancia de EC2 debemos instalar el Nginx, y el agente de CloudWatch que es el que nos va a permitir realizar un monitoreo y nos va a servir de puente en el envió de logs.


<img width="836" height="398" alt="Captura desde 2025-12-02 21-03-42" src="https://github.com/user-attachments/assets/df3141a4-2501-48e7-955c-3ce017a84f1f" />




Esto nos permitirá poder ver las metricas que elijamos conocer de la instancia EC2, y como este es nuestro servidor y en el está alojado nginx, cuando ingresen al sitio este tendrá que responder de alguna forma y esto representará un esfuerzo en terminos de RAM usada. Con el agente instalado entonces es posible ver estas metricas en CloudWatch.




<img width="828" height="636" alt="Captura desde 2025-12-02 21-03-30" src="https://github.com/user-attachments/assets/cfb9e29a-33c1-4544-a596-1a832b0db9c6" />




Veremos tambien desde la informacion de los registros que portan una traza que permite seguirlos con X-ray:


<img width="836" height="398" alt="Captura desde 2025-12-02 21-03-51" src="https://github.com/user-attachments/assets/6490b0f5-6d11-49f0-96f1-8801181964ae" />




Esto permite tener una guía visual en la seccion de X-ray de CloudWatch para visualizar que tipo de procesos estan experimentando esos datos:


<img width="836" height="398" alt="Captura desde 2025-12-02 21-03-58" src="https://github.com/user-attachments/assets/c396644e-a89e-4ecf-925b-8e6d24a7dc93" />



Ahora bien, con este mismo funcionamiento y con los datos disponibles, es posible activar alarmas según la detección de anomalías, las cuales notifiquen sobre posibles riesgos, en este caso el porcentaje de uso de la RAM, lo cual puede indicar posibles riesgos para el servicio, y apartir de esto entonces se envíen correos y se habiliten balanceadores de carga o procesos de autoescala.



<img width="836" height="398" alt="Captura desde 2025-12-02 21-04-05" src="https://github.com/user-attachments/assets/cddcefca-4aac-4cd0-a884-ed914157c566" />




Luego se deben crear las funciones lambda, las cuales en este caso son 2, una será fundamental para que firehose tome los datos, los transforme y permita que opensearch trabaje con ellos; y la otra será para simular la entrada de clientes a la aplicación, simulando errores con 10% de probabilidad.


En CloudWatch, tambien tendremos grupos de registros disponibles para observar una vez se haya creado la función lambda correspondiente y se haya asociado el permiso para recibir sus logs.


<img width="836" height="398" alt="Captura desde 2025-12-02 21-04-24" src="https://github.com/user-attachments/assets/fef585a7-f91c-49b5-9cb7-f89c738f156b" />




El paso siguiente es construir las secuencias de Firehose, que son simplemente conductos que permiten el transporte de datos desde un servicio a otro, hay que tener especial cuidado con los permisos, los destinos, el indice de los datos transportados, y el procesamiento de estos, de forma que el servicio que los recibe los comprenda y los pueda usar, para esto es la función lambda de procesamiento, permite descomprimirlos y ajustar su formato para que OpenSearch pueda recibir apropiadamente los datos desde CloudWatch.



<img width="836" height="398" alt="Captura desde 2025-12-02 21-04-24" src="https://github.com/user-attachments/assets/02dc5362-81a3-478e-aa92-85dc703a8ed4" />





Una vez se logre esto se debe "matricular" el indice de los datos en OpenSearch, y se empezaran a recibir:


<img width="836" height="398" alt="Captura desde 2025-12-02 21-04-29" src="https://github.com/user-attachments/assets/31e65686-5cda-4644-8c18-02a4c12d4870" />



<img width="836" height="398" alt="Captura desde 2025-12-02 21-04-35" src="https://github.com/user-attachments/assets/4c2f0eef-f4b8-4eef-b374-cb5c0fd1f00e" />




El proceso siguiente una vez habiendo logrado lo mas dificil que es permitir la libre comunicación fluida y correcta entre los servicios es simplemente visualizar con una mejor calidad y posibilidad de personalización los datos en Grafana, la cual fue previamente instalada en el servidor, instancia de EC2 mediante comandos. Todo esto hecho desde una cuenta real.


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-14-29" src="https://github.com/user-attachments/assets/e693b7be-a64d-4de8-963c-20914b7a79a8" />


El servicio de Grafana tambien puede usar el pluggin de ElasticSearch, realizan esecialmente el mismo proceso, de recibir los permisos de Firhose, los indices para cada uno de los streams de Firehose y la interfaz de DashBoards para configurar la visualización.

<img width="959" height="968" alt="Captura desde 2025-12-11 21-55-19" src="https://github.com/user-attachments/assets/a94c3c5b-6761-406a-bf9d-ca6b106fad15" />


Por lo cual es posible hacer la misma visualización y observabilidad de los datos que están entrando el servidor como logs de Nginx desde EC2 y la ejecución de funciones Lambda que son nuestras aplicaciones que producen los datos. Se pueden visualizar graficas de numeros de errores detectados por ejecución de una función lambda, los registros y su información, la distribución temporal de estos accesos en terminos del uso de disco o uso de ram en la instancia de EC2, o la información de cada pedido a la funcion lambda.


<img width="959" height="968" alt="Captura desde 2025-12-11 21-49-00" src="https://github.com/user-attachments/assets/e555e46f-d54a-49d8-a990-714069e3953e" />



Se tienen habilitadas tambien funciones como CloudWatch logs insights que nos permite una visualización del comportamiento de los datos muy similar a OpenSearch DashBoards o Kibana. 

Agregamos una función con Machine Learning en Amazon SageMaker, desde un notebook de Jupyter que nos permite analizar comportamientos anómalos en un conjunto de datos como el que puede estarse reportando por cualquiera de los servicios o como un archivo .csv que subimos directamente al Bucket de S3 en este caso. Los resultados del analisis se reportan directamente a este bucket en forma de imagen .png de la grafica del analisis que genera el código usando sckit-learn.
