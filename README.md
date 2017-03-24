# Compranet - Ciencia de Datos para evitar la corrupción.

## ToDo's

- SQLite 2 RDS 
- Terminar Spider Declaranet
- Metadatos de Compranet
- Metadatos de Funcionarios
- Pipeline de actualización de Base de datos
- ToDO(Luigi)

## About:
Compranet es un sistema electrónico (Desarrollado por la Secretaría de la Función Pública) que asiste el proceso de contratación de servicios, bienes, arrendamientos y obra pública de las dependencias y entidades de la administración pública.
**


### Technical Plan


### Data Pipeline

* Download Data
	- /Ingest/Initial_Ingestion Descarga Compranet y el directorio de funcionarios
	- /Ingest/declaranet - scrapy/selenium crawler para obtener cvs y declaración **[Desarrollo]**
* Raw Table Creation **[Desarrollo]**
	- Datos se suben a un RDS
* Create semantic tables **[Desarrollo]**
* Create semantic tables **[Desarrollo]**
* Create Graph DB **[Desarrollo]**

### Configuration Files

### Dependencies

### Wishful

### Contributors

| [![taguerram][ph-thalia]][gh-thalia] | [![rsanchezavalos][ph-rsanchez]][gh-rsanchez] | [![monzalo14][ph-monica]][gh-monica] | [![maragones][ph-manuel-a]][gh-manuel-a] |
|                 :--:                 |                     :--:                      |                     :--:             |                     :--:             |
|        [taguerram][gh-thalia]         |         [rsanchezavalos][gh-rsanchez]           |          [monzalo14][gh-monica]      |          [maragones][gh-manuel-a]      |



[ph-thalia]: https://avatars0.githubusercontent.com/u/20998351?v=3&s=460
[gh-thalia]: https://github.com/taguerram

[ph-monica]: https://avatars0.githubusercontent.com/u/16139907?v=3&s=460
[gh-monica]: https://github.com/monzalo14


[ph-manuel-a]: https://avatars2.githubusercontent.com/u/11464076?v=3&s=460
[gh-manuel-a]: https://github.com/maragones

[ph-rsanchez]: https://avatars.githubusercontent.com/u/10931011?v=3&s=460
[gh-rsanchez]: https://github.com/rsanchezavalos


