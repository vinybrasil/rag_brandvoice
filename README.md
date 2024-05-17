# Configuração do Brand voice 

API que é uma RAG num PDF de Brand Voice que impersona uma marca de sapatos e
responde as perguntas com base nas Brand Voice Guidelines entregues à ele.

## Como usar

```bash
ollama serve
```

Buildar a imagem: 
```bash
docker build -t rag_voice:latest .
```

Rodar ela:
```bash
docker run -p 8000:8000 rag_voice:latest
```

### Exemplos

Usando o método POST deve-se chamar a rota /api/v1/download com o seguinte Body:
```json
{
    "url": "https://a.slack-edge.com/a29fb/marketing/img/media-kit/Slack-Brand-Guidelines.pdf"
}
```
Caso consiga, é possível chamar a rota /api/v1/question com a pergunta no Body da requisição:
```json
{
    "question": "What are the mission of your company?"
}
``` 

## TODO 

### LLM
- Utilizar uma LLM multimodal como a Mistral 
- Testar outros prompts para tentar melhorar a resposta
- Persisitir os vetores lidos no disco, separando cada voice em uma base de dados com seus textos e imagens


### API 
- Retornar assim que receber a URL (hoje espera a extração do PDF terminar para dar o retorno da requisição), ou seja, tornar assíncrono o processo de extração de dados
- Validar a URL da requisição antes de baixar
- Validar o texto da pergunta
- Salvar os resultados num banco de dados
- Usar o logging para gerar os logs
- Testes unitários
- Error Handling
- Swagger

### Deploy 
- Chamar a API de dentro do Docker
- Dar a opção de chamar outras LLMs (caso teste ou uma esteja fora do ar)

### Monitoramento 
- Para checar a qualidade das respostas, pode-se usar um modelo maior (ex. ChatGPT4) via comparação
- Utilizar métricas como a [Perplexity](https://huggingface.co/spaces/evaluate-metric/perplexity) para avaliar o modelo 
- Checar para prompt leakage e toxicidade nas respostas
