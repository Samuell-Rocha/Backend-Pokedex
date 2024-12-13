# Minha API

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Básico** 

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das três aulas da disciplina.

---


### 1. Clonando o Repositório


Primeiramente, clone o repositório para o seu ambiente local:
```
git clone https://github.com/seu-usuario/pokedex-frontend.git
```
### 2. Instalando Bibliotecas

Para instalar todas as bibliotecas necessárias, abra um terminal e digite o seguinte comando:
```
pip install -r requirements.txt
```
Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

### 3. Instalando Ambiente Virtual

ainda no terminal, instale o ambiente virtual com o seguinte comando:
```
pip install virtualenv
```
após a instalação ative-o com o seguinte comando:

  ## 3.1 Criando Ambiente Virtual

  após a instalação do ambiente virtual, navegue até o diretório onde você deseja criar o ambiente virtual e execute o seguinte comando:
  ```
  virtualenv nome_do_ambiente
  ```
  Isso criará um diretório chamado nome_do_ambiente com todos os arquivos necessários para o ambiente virtual.

  ## 3.2 Ativando Ambiente Virtual
  ative o ambiente com o seguinte comando:

  No Windows:
  ```
  .\nome_do_ambiente\Scripts\activate
  ```
  No Linux ou macOS:
  ```
  source nome_do_ambiente/bin/activate
  ```

## Como executar 


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
