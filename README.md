# 🎵 Analizador de Playlist Spotify

Projeto Acadêmico feito para a disciplina de Matemática Aplicada a Computação
Este projeto é uma ferramenta em Python que permite analisar playlists do Spotify, extraindo informações detalhadas sobre as músicas, artistas, popularidade, gêneros musicais e frequências, apresentando rankings e gráficos interativos.

## 🚀 Funcionalidades

- **Leitura de qualquer playlist pública ou colaborativa do Spotify**
- **Ranking das músicas mais populares e mais repetidas**
- **Análise e ranking de gêneros musicais presentes na playlist**
- **Visualização gráfica dos dados (gráficos de barras e pizza)**
- **Estrutura eficiente usando árvores binárias para ordenação personalizada**

## 🛠️ Tecnologias Utilizadas

- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) (API Spotify para Python)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv) (para variáveis de ambiente)
- Árvores Binárias customizadas para ordenação e ranking

É necessário configurar suas credenciais do Spotify:
   - Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
     ```
     SPOTIFY_CLIENT_ID=seu_client_id
     SPOTIFY_CLIENT_SECRET=seu_client_secret
     ```
   - Você pode obter suas credenciais criando um app em [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).


## 📊 Exemplos de Saída

- **Árvore Representada Graficamente**
  
![Imagem do WhatsApp de 2025-06-05 à(s) 20 28 37_050ef340](https://github.com/user-attachments/assets/e45cb500-cfd1-4497-9536-9f4bdafec76a)
![Imagem do WhatsApp de 2025-06-05 à(s) 20 28 37_d2efc561](https://github.com/user-attachments/assets/ae3c12c6-0322-4a89-a52b-b3c0b5fb5fb6)
![Imagem do WhatsApp de 2025-06-05 à(s) 20 28 38_fa6e2aa9](https://github.com/user-attachments/assets/0f15856c-1235-4c21-b134-6f22689d355c)
![Imagem do WhatsApp de 2025-06-05 à(s) 20 28 38_3f516889](https://github.com/user-attachments/assets/38b6ef34-01fa-4b95-93b5-ed91dbede358)

## 💡 Observações

- O script utiliza a API do Spotify, que possui limites de requisições. Para playlists muito grandes, a análise pode demorar alguns segundos.
- Os gráficos são exibidos diretamente utilizando Matplotlib, então é necessário que o ambiente suporte janelas gráficas.
