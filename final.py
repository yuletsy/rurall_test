# BY: YULETSY PAOLA PABON --- 2023 -- MARZO
# se importan los paquetes necesarios para la regresión lineal
import pyspark
import datetime
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import substring,col
import matplotlib.pyplot as plt
from pyspark.ml.evaluation import RegressionEvaluator

# se crea un instancia de sesion de pyspark
spark = SparkSession.builder.appName("Drugs").getOrCreate()

# se crea una variable now para saber la fecha actual
now = datetime.datetime.now()

# se cargan los dataframe que vamos a utilizar para hacer el procesamiento de datos y la prediccion
df0 = spark.read.csv("drugs_train.csv", header=True, inferSchema=True)
df1 = spark.read.csv("drugs_test.csv", header=True, inferSchema=True )
df2 = spark.read.csv("active_ingredients.csv", header=True, inferSchema=True)
df3 = spark.read.csv("drug_label_feature_eng.csv", header =True, inferSchema=True)

# se realizan los joins para tener todos los datos en conjunto y asi seguir con el entrenamiento.
# 1. Inner join de df0 con df2 utilizando durg_id como key
# 2. A partir de alli se crea un nuevo dataframe
df4 = df0.join(df2, "drug_id", how= "inner")

# 3. Se reaiza Inner join de los dataframe df4 y df1 con df3 utilizando 'description' como key
# 4. Crea dos dataframes 'train_data' y 'test_Data'
train_data = df4.join(df3, "description", how= "inner")
test_data = df1.join(df3, "description", how= "inner")


# Datos que convierto en train_data y test_data
# 1. De la columna 'marketing_authorization_date' y 'marketing_declaration_date' se hace la extracion del año y se convierte a tipo entero para tener una variable numerica
# 2. Se hace una resta de las fechas para saber cuanto tiempo hay de diferencia.
# 3. Se hace una operacion entre el año actual y el año de autorizacion
# 4. Se crea una variable que tome el precio como un label par aluego utilizarlo en la prediccion
train_data = train_data.withColumn('year_authorization',substring(col("marketing_authorization_date").cast("string"),1,4).cast("integer"))
train_data = train_data.withColumn('year_declaration',substring(col("marketing_declaration_date").cast("string"),1,4).cast("integer"))
train_data = train_data.withColumn('time_authorization', col("year_declaration") - col("year_authorization"))
train_data = train_data.withColumn('time', now.year - col("year_authorization"))
train_data = train_data.withColumn('label', col("price"))


test_data = test_data.withColumn('year_authorization',substring(col("marketing_authorization_date").cast("string"),1,4).cast("integer"))
test_data = test_data.withColumn('year_declaration',substring(col("marketing_declaration_date").cast("string"),1,4).cast("integer"))
test_data = test_data.withColumn('time_authorization', col("year_declaration") - col("year_authorization"))
test_data = test_data.withColumn('time', now.year - col("year_authorization"))

# feature engineering, donde añado los variables a analizar para que la prediccion sea poco mas precisa
fe_field = ["marketing_authorization_date", "label_plaquette" , "label_ampoule" , "label_flacon" , "label_tube" , "label_stylo" , "label_seringue" , "label_pilulier" , "label_sachet" , "label_comprime" , "label_gelule" , "label_film" , "label_poche" , "label_capsule" , "count_plaquette" , "count_ampoule" , "count_flacon" , "count_tube" , "count_stylo" , "count_seringue" , "count_pilulier" , "count_sachet" , "count_comprime" , "count_gelule" , "count_film" , "count_poche" , "count_capsule" , "count_ml"] 

# 1. Se crea un vectorAssembler que combina varias columnas utilizando la variable fe_field y se especifica la salida 'feature'
# 2. Se aplica el metodo trandform del vectorassembler al 'train_data' y se crea un nuevo dataframe con la columna 'features'
# 3. Se seleccionas las columnas en un nuevo dataframe y traemos el 'label' del 'train_data'
assembler = VectorAssembler().setInputCols(fe_field).setOutputCol('features')
train01 = assembler.transform(train_data)
train02 = train01.select("drug_id", "features", "label")
train02.show(truncate=False)

# 4. Se aplica el modelo de regresion lineal para ajustar los datos de entrenamiento
lr = LinearRegression(regParam=0.1)
model = lr.fit(train02)
test01 = assembler.transform(test_data)
test02 = test01.select("drug_id", "features")
test03 = model.transform(test02)
test03.show(truncate=False)

# Se guardan los resultados de la prediccion en la variable 'resul'
resul = test03.filter(col("drug_id") == "0_test")
resul.show()
resul.printSchema()
# Convertir los resultados a un formato de dataframe de pandas para poder exportarlo comoa archivo csv
test03_format = test03.toPandas()
# Seleccion de las columnas a visualizar en el archivo
resul_csv = resul.select('drug_id', 'prediction').toPandas()
# se crea el archivo csv y se muestra la variable 'resul'
resul_csv.to_csv("price_prediction.csv", index=False)

# evaluator = RegressionEvaluator(metricName="mse")
# mse = evaluator.evaluate(test03)
# print("MSE: ", mse)
# Se hace la visualizacion de los resultados en un grafico 

# features_array = np.array(test03_format["features"].tolist()) 
# plt.scatter(test03_format["drug_id"], features_array, color="gray")
# plt.plot(resul_csv["drug_id"], resul_csv['prediction'], color='red', linewidth=2)
# plt.xlabel("Features")
# plt.ylabel("Price")
# plt.legend(["real valeues", "predictions"])
# plt.title("Prediction vs real values")
# plt.show()







