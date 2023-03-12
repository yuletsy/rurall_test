# rurall_test

### 1. Como deben correr el codigo
1. git clone https://github.com/yuletsy/rurall_test.git

2. Abrir en vscode

3. instalar python o verificar version de python
   sudo apt-get install python3.7

   python3 --version

4. Instalar pyspark
   sudo pip3 install pyspark

5. Verificar version de pyspark
   pyspark --version
   
6. instalar librerias correspondientes

7. Correr el archivo 
   python3 final.py

Automaticamente se crea un archivo llamado price_prediction.csv donde esta el resultado

###  2. Describe en uno o dos párrafos el por qué elegiste este algoritmo para solucionar el problema.

Escogi el algoritmo de regresión lineal para predecir los precios porque me permite analisas la relacion entre dos cvariable cuantitativas continuas, en este caso el precio y las features que pueden influir. 
Es una técnica que me permitio predecir los precios, para modelar la relación en el precio de los farmacos y otras variables, tambien estimar el valor de la variable dependiente(precio) para un valor dado de la variable independiente(prediction), lo que permitiria en un futuro tomar decisiones informadas sobre sus estrategias de precios.

### 3 . Una descripción del rendimiento en general de el(los) algoritmo(s)

Con respecto al rendimiento, en las primeras predicciones los valores eran muy muy altos, entonces loq que se hizo fue tomas mas variables y datos para llegar a una prediccion mas acertada, el comportamiento.

