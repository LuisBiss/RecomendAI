import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

LIMITES = {
    "Colesterol": [190],
    "Glicose": [126],
    "T3": [1.81],
    "T4": [12.3],
    "TSH": [5.60],   
    "Triglicerídeos": [150]
}

DICAS_NUTRICIONAIS = {
    "Colesterol": "Aumente o consumo de fibras, frutas e vegetais. Evite gorduras trans e saturadas.",
    "Glicose": "Reduza a ingestão de açúcares e carboidratos refinados. Prefira alimentos com baixo índice glicêmico.",
    "T3": "Inclua alimentos ricos em iodo e zinco, que ajudam no metabolismo da tireoide.",
    "T4": "Mantenha uma alimentação equilibrada, rica em vitaminas e minerais, especialmente o selênio.",
    "TSH": "Consuma alimentos ricos em iodo, como peixe e algas marinhas. Evite goitrogênios em excesso.",
    "Triglicerídeos": "Reduza o consumo de alimentos ricos em gordura saturada e carboidratos simples."
}

def gerar_dados_treinamento(num_amostras=2000):
    X_train = []
    y_train = []
    
    for _ in range(num_amostras):
        colesterol = np.random.uniform(110, 260)  
        glicose = np.random.uniform(80, 220)  
        t3 = np.random.uniform(0.2, 4.5) 
        t4 = np.random.uniform(3.0, 18.0)  
        tsh = np.random.uniform(0.3, 14.0) 
        triglicerideos = np.random.uniform(80, 700)  
        
        valores = [colesterol, glicose, t3, t4, tsh, triglicerideos]
        recomendacoes = []
        
        recomendacoes.append(1 if colesterol <= LIMITES["Colesterol"][0] else 0)
        recomendacoes.append(1 if glicose <= LIMITES["Glicose"][0] else 0)
        recomendacoes.append(1 if t3 <= LIMITES["T3"][0] else 0)
        recomendacoes.append(1 if t4 <= LIMITES["T4"][0] else 0)
        recomendacoes.append(1 if tsh <= LIMITES["TSH"][0] else 0)
        recomendacoes.append(1 if triglicerideos <= LIMITES["Triglicerídeos"][0] else 0)

        X_train.append(valores)
        y_train.append(recomendacoes)
    
    return np.array(X_train), np.array(y_train)

def criar_modelo():
    model = keras.Sequential([
        keras.layers.Input(shape=(6,)), 
        keras.layers.Dense(64, activation="relu"),   
        keras.layers.Dropout(0.4),  
        keras.layers.Dense(128, activation="relu"),  
        keras.layers.Dense(6, activation="sigmoid")   
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

def carregar_ou_treinar_modelo():
    modelo_path = 'modelo.keras'
    
    if os.path.exists(modelo_path):
        print("Carregando modelo existente...")
        modelo = keras.models.load_model(modelo_path)
    else:
        print("Modelo não encontrado, treinando modelo...")
        X_train, y_train = gerar_dados_treinamento()
        modelo = criar_modelo()
        modelo.fit(X_train, y_train, epochs=2000, batch_size=32, validation_split=0.2)
        modelo.save(modelo_path) 
        print(f"Modelo treinado e salvo em {modelo_path}")
    
    return modelo

modelo = carregar_ou_treinar_modelo()

def classificar_resultado_com_modelo(valores):
    previsao = modelo.predict(np.array([valores]))[0]
    
    recomendacoes = []
    for i, valor in enumerate(previsao):
        if valor >= 0.5:
            recomendacoes.append("Muito bem! Continue assim.")
        else:
            parametro = list(LIMITES.keys())[i]
            recomendacoes.append(f"Melhore: {DICAS_NUTRICIONAIS[parametro]}")
    
    return {
        "Colesterol": recomendacoes[0],
        "Glicose": recomendacoes[1],
        "T3": recomendacoes[2],
        "T4": recomendacoes[3],
        "TSH": recomendacoes[4],
        "Triglicerídeos": recomendacoes[5]
    }

novos_valores = [150, 130, 100, 4.5, 12.5, 2.0] 
resultado_classificado = classificar_resultado_com_modelo(novos_valores)
print(resultado_classificado)