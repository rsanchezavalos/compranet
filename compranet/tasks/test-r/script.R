

df <- data.frame(minusculas=letters, numeros=rnorm(n=length(letters)), mayusculas=LETTERS)

write.table(df, file="./data/hola_mundo_desde_R.psv", quote=TRUE, sep="|",
            row.names=FALSE, col.names=TRUE)
