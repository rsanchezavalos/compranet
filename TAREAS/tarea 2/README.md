*TAREA 2*
export COMPOSE_API_VERSION=1.22
docker-compose down
docker-compose build
docker-compose up -d


- Crea un /dashboard/ usando =shiny= que utilice como =backend= un servicio =Flask=. Para conectarte utiliza el paquete de =R= ~httr~.  El /dashboard/ muestra la base de datos =iris= guardada en una base de datos  =postgresql= i.e., el servicio web de =Flask= lee la base de datos, y devuelve un =json= con el dataset

# http://localhost:2234/

- Agrega otro contenedor que al ejecutarse obtiene un renglón al azar del /dataset/ y lo imprime en pantalla (puedes construirlo en =bash= (=httpie=) o en =python=

# http://localhost:8080/

- Desarrolla todo, obviamente, usando =docker-compose= con =docker-machine= en *Amazon AWS*

