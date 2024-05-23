import tensorflow as tf
import numpy as np

# Dados de exemplo: características do ambiente do jogo e ação (0 para não pular, 1 para pular)
dados = np.array([
    [300, 0, 0],  # Exemplo 1: altura do jogador, distância do zumbi, ação (não pular)
    [250, 100, 1],  # Exemplo 2: altura do jogador, distância do zumbi, ação (pular)
    # Adicione mais exemplos conforme necessário
])

# Separando os dados de entrada (características) e saída (ação)
X = dados[:, :2]  # Altura do jogador e distância do zumbi
y = dados[:, 2]   # Ação (pular ou não)

# Definindo a arquitetura da rede neural
model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(2, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compilando o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treinando o modelo
model.fit(X, y, epochs=100)

# Testando o modelo com novos dados
novo_dado = np.array([[280, 50]])  # Nova situação: altura do jogador e distância do zumbi
previsao = model.predict(novo_dado)
print("Probabilidade de pular:", previsao[0][0])