<M-k># Middleware

Para ejecutar el middleware , primero se debera realizar **build** de la docker image, utilizando el siguiente comando:
```
docker build -t <docker_image> .
```

Despues de haber realizado el **build** , esto generara dicha docker image, y se podra ejecutar haciendo uso del siguiente comando:
```
docker run --rm\ 
--name middleware\
--env-file test.env\
-v $(pwd)/restuls:/results\ 
<docker_image> 
```
El nombre de la imagen puede variar dependiendo si se realizar el **build**,  en caso de no realizar el **build**, se puede obtener utilizando los repositorios de Docker Hub, haciendo uso del siguiente comando:

```
docker run --rm \
--name middleware\
--env-file test.env
-v $(pwd)/results:/results\
nachocode/cinvestav-ds-middleware
```


