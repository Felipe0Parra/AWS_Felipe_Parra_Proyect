# AWS_Felipe_Parra_Proyect
Repositorio sobre el proyecto de observabilidad en la nube de Amazon Web Services.
El proyecto se inicia configurando la instancia de EC2 que se desea utilizar, instancia la cual corresponde a nuestro servidor y es donde se alojara el nginx que utilizaremos como pagina web en la cual los clientes se loggeran. Sin embargo, antes de empezar a activar servicios es importante configurar y establecer la seguridad, para esto primero se crea una persona, para no exponer al root user y luego se asignan roles, que permitan activar servicios y permitir la comunicación entre ellos.

Asi como se deben crear roles para conservar la seguridad y permitir un flujo de trabajo, se deben habilitar diferentes reglas de seguridad en los grupos de seguridad de la instancia para permitir el trafico de datos en las diferentes direcciones.



<img width="941" height="136" alt="Captura desde 2025-12-01 11-46-11" src="https://github.com/user-attachments/assets/2fbaa49d-399a-4663-a9da-a3caae6797e0" />



Es importante tener en cuenta que es necesario habilitar la instancia como una vpc para poder tener subredes publicas y privadas, publicas pues es donde se alojaran los servicios al publico y privadas donde se alojaran los servicios que solo necesitan información del exterior pero que no se pueden acceder desde internet.

Una vez creada la instancia de EC2 debemos instalar el Nginx, y el agente de CloudWatch que es el que nos va a permitir realizar un monitoreo y nos va a servir de puente en el envió de logs.


<img width="921" height="729" alt="Captura desde 2025-11-18 18-37-36" src="https://github.com/user-attachments/assets/9fab6ad7-a42d-4fe5-bdd9-5b645b63e716" />



Esto nos permitirá poder ver las metricas que elijamos conocer de la instancia EC2, y como este es nuestro servidor y en el está alojado nginx, cuando ingresen al sitio este tendrá que responder de alguna forma y esto representará un esfuerzo en terminos de RAM usada. Con el agente instalado entonces es posible ver estas metricas en CloudWatch.



<img width="960" height="1050" alt="Captura desde 2025-11-30 19-56-08" src="https://github.com/user-attachments/assets/bfda9fd6-6966-469a-850a-50c57547848c" />

<img width="1852" height="968" alt="Captura desde 2025-12-02 20-48-34" src="https://github.com/user-attachments/assets/7bb55ba7-e08b-493c-9547-4f03300aacb7" />



Veremos tambien desde la informacion de los registros que portan una traza que permite seguirlos con X-ray:


<img width="1852" height="968" alt="Captura desde 2025-12-02 20-50-34" src="https://github.com/user-attachments/assets/82dbc2d8-3431-4467-bd53-e421fa56f42d" />



Esto permite tener una guía visual en la seccion de X-ray de CloudWatch para visualizar que tipo de procesos estan experimentando esos datos:


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-24-01" src="https://github.com/user-attachments/assets/8cdf099d-2c70-4191-a639-6319b9eab8b2" />



Ahora bien, con este mismo funcionamiento y con los datos disponibles, es posible activar alarmas según la detección de anomalías, las cuales notifiquen sobre posibles riesgos, en este caso el porcentaje de uso de la RAM, lo cual puede indicar posibles riesgos para el servicio, y apartir de esto entonces se envíen correos y se habiliten balanceadores de carga o procesos de autoescala.



<img width="1852" height="968" alt="imagen" src="https://github.com/user-attachments/assets/0883d14b-f33d-42af-a7b2-0072aed6b831" />



Luego se deben crear las funciones lambda, las cuales en este caso son 2, una será fundamental para que firehose tome los datos, los transforme y permita que opensearch trabaje con ellos; y la otra será para simular la entrada de clientes a la aplicación, simulando errores con 10% de probabilidad.


En CloudWatch, tambien tendremos grupos de registros disponibles para observar una vez se haya creado la función lambda correspondiente y se haya asociado el permiso para recibir sus logs.


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-15-06" src="https://github.com/user-attachments/assets/3c4e6339-0f30-4d29-8a95-0297c8120df0" />



El paso siguiente es construir las secuencias de Firehose, que son simplemente conductos que permiten el transporte de datos desde un servicio a otro, hay que tener especial cuidado con los permisos, los destinos, el indice de los datos transportados, y el procesamiento de estos, de forma que el servicio que los recibe los comprenda y los pueda usar, para esto es la función lambda de procesamiento, permite descomprimirlos y ajustar su formato para que OpenSearch pueda recibir apropiadamente los datos desde CloudWatch.



<img width="1852" height="968" alt="Captura desde 2025-12-02 20-44-23" src="https://github.com/user-attachments/assets/82757d90-5d32-403c-a70c-ad186adb2477" />



Una vez se logre esto se debe "matricular" el indice de los datos en OpenSearch, y se empezaran a recibir:


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-14-39" src="https://github.com/user-attachments/assets/f59a0797-4cbc-4007-9267-9254650d76a7" />


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-14-48" src="https://github.com/user-attachments/assets/7e756a0f-ed6b-46c6-9b7f-777581d9a5fb" />


El proceso siguiente una vez habiendo logrado lo mas dificil que es permitir la libre comunicación fluida y correcta entre los servicios es simplemente visualizar con una mejor calidad y posibilidad de personalización los datos en Grafana, la cual fue previamente instalada en el servidor, instancia de EC2 mediante comandos. Todo esto hecho desde una cuenta real.


<img width="1855" height="968" alt="Captura desde 2025-12-01 19-14-29" src="https://github.com/user-attachments/assets/e693b7be-a64d-4de8-963c-20914b7a79a8" />


