# AWS_Felipe_Parra_Proyect
Repositorio sobre el proyecto de observabilidad en la nube de Amazon Web Services.
El proyecto se inicia configurando la instancia de EC2 que se desea utilizar, instancia la cual corresponde a nuestro servidor y es donde se alojara el nginx que utilizaremos como pagina web en la cual los clientes se loggeran. Sin embargo, antes de empezar a activar servicios es importante configurar y establecer la seguridad, para esto primero se crea una persona, para no exponer al root user y luego se asignan roles, que permitan activar servicios y permitir la comunicación entre ellos.

Es importante tener en cuenta que es necesario habilitar la instancia como una vpc para poder tener subredes publicas y privadas, publicas pues es donde se alojaran los servicios al publico y privadas donde se alojaran los servicios que solo necesitan información del exterior pero que no se pueden acceder desde internet.

Luego se deben crear las funciones lambda, las cuales en este caso son 2, una será fundamental para que firehose tome los datos, los transforme y permita que opensearch trabaje con ellos; y la otra será para simular la entrada de clientes a la aplicación, simulando errores con 10% de probabilidad.

<img width="921" height="729" alt="Captura desde 2025-11-18 18-37-36" src="https://github.com/user-attachments/assets/9fab6ad7-a42d-4fe5-bdd9-5b645b63e716" />
