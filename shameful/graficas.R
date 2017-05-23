# Creamos la gráfica

graph <- startGraph("http://ec2-54-69-4-123.us-west-2.compute.amazonaws.com:7474/db/data/")
dependencia <- getLabeledNodes(graph, "Dependencia")
relacion <- getRels(graph, 'MATCH ()-[]->()')

# Primera prueba
edges = cypher(graph, 'MATCH (d:Dependencia)-[c:que_contiene]->(u:Unidad) 
RETURN d.nombre AS dependencia, u.clave AS unidad, count(*) as weight')

nodes <- data.frame(id=unique(c(edges$dependencia, edges$unidad)))
nodes$label = nodes$id

# Funcionarios-empresas

funcionarios_empresas = cypher(graph, 'MATCH (p:Proveedor)<-[dp:del_proveedor]-(c:Compra)<-[adq:adquirio]-(f:Fecha)-[per:pertenecio]->(fun:Funcionario)
RETURN fun.id AS funcionario, count(*) as weight
ORDER BY weight DESC') 


funcionarios_empresas_concentracion = cypher(graph, 'MATCH (p:Proveedor)<-[dp:del_proveedor]-(c:Compra)<-[adq:adquirio]-(f:Fecha)-[per:pertenecio]->(fun:Funcionario)
RETURN fun.id as funcionario, p.nombre as empresa, count(*) as weight
ORDER BY weight DESC') 


funcionarios_empresas_concentracion %>% 
  group_by(funcionario) %>%
  mutate(distintas = (weight/sum(weight))^2) %>%
  summarise(concentracion = sum(distintas)) %>%
  arrange(-concentracion) %>%
  ggplot() +
  geom_histogram(aes(concentracion),
                 binwidth = .008,
                 color = 'steelblue4',
                 fill = 'steelblue4') +
  labs(title = 'Concentración en relaciones de funcionarios',
       x = '', y = '') +
  coord_flip() +
  scale_x_continuous(labels = scales::percent) +
  theme_bw()



funcionarios_empresas %>%
  filter(!grepl('Info', funcionario),
         !grepl('Reserva', funcionario),
         !grepl('Vacant', funcionario)) %>%
  ggplot() +
  geom_histogram(aes(weight), 
                 binwidth = 1,
                 color = 'tomato4',
                 fill = 'tomato4') +
  labs(title = 'Centralidad pesada de funcionarios',
       x = '', y = '') +
  theme_bw()

#### Conexiones entre todo mundo y todo mundo

aux<-function(x){
  x[is.na(x)] <- 0
  x
}

fun <- data.frame(persona = unique(funcionarios_empresas_concentracion$funcionario))
emp <- data.frame(persona = unique(funcionarios_empresas_concentracion$empresa))

nodos <- rbind(fun, emp)
  
aristas1 <- funcionarios_empresas_concentracion %>%
            filter(funcionario == '3037') %>%
            spread(key = empresa, value = weight) %>%
            mutate_all(aux) %>%
            gather(key = empresa, value = weight, -funcionario) %>%
            mutate(relacion = weight>0) %>%
            group_by(funcionario) %>%
            arrange(-weight) %>%
            top_n(5) %>%
            ungroup()

aristas2 <- aristas1

names(aristas1) <- c('to', 'from', 'weight', 'relacion')
names(aristas2) <- c('from', 'to', 'weight', 'relacion')


aristas <- rbind(aristas1, aristas2)

grafica <- graph_from_data_frame(aristas, directed = F, vertices = nodos)

ggnet2(grafica)

# Tablita de la presentación
funcionarios_empresas_concentracion %>%
  filter(funcionario == 2981) %>%
  arrange(-weight) %>%
  head(5) -> sample

  