# Códigos de Status HTTP

## 1xx - Informativo
- **100 Continue**: O servidor recebeu o cabeçalho de solicitação e o cliente deve continuar com o envio do corpo da solicitação.
- **101 Switching Protocols**: O servidor está mudando para o protocolo solicitado pelo cliente.
- **102 Processing**: O servidor recebeu e está processando a solicitação, mas ainda não tem uma resposta.

## 2xx - Sucesso
- **200 OK**: A solicitação foi bem-sucedida e o servidor retornou a resposta solicitada.
- **201 Created**: A solicitação foi bem-sucedida e um novo recurso foi criado.
- **202 Accepted**: A solicitação foi aceita para processamento, mas o processamento não foi concluído.
- **203 Non-Authoritative Information**: A solicitação foi bem-sucedida, mas a informação retornada pode ser de uma fonte diferente.
- **204 No Content**: A solicitação foi bem-sucedida, mas não há conteúdo para retornar.
- **205 Reset Content**: A solicitação foi bem-sucedida, e o cliente deve redefinir o conteúdo.
- **206 Partial Content**: O servidor está enviando apenas uma parte do recurso solicitado.
- **207 Multi-Status**: A resposta contém informações sobre múltiplos recursos, como em um PROPFIND.

## 3xx - Redirecionamento
- **300 Multiple Choices**: Há múltiplas opções para o recurso solicitado.
- **301 Moved Permanently**: O recurso solicitado foi movido permanentemente para uma nova URL.
- **302 Found**: O recurso solicitado foi encontrado em uma URL diferente, temporariamente.
- **303 See Other**: O recurso deve ser acessado em uma URL diferente usando o método GET.
- **304 Not Modified**: O recurso não foi modificado desde a última solicitação.
- **305 Use Proxy**: O recurso solicitado deve ser acessado através de um proxy especificado.
- **307 Temporary Redirect**: O recurso solicitado foi temporariamente movido para uma URL diferente.
- **308 Permanent Redirect**: O recurso foi permanentemente movido para uma nova URL e deve ser acessado usando a nova URL.

## 4xx - Erro do Cliente
- **400 Bad Request**: A solicitação não pode ser processada devido a um erro do cliente.
- **401 Unauthorized**: A solicitação requer autenticação.
- **402 Payment Required**: O pagamento é necessário para acessar o recurso (pouco usado atualmente).
- **403 Forbidden**: O servidor entendeu a solicitação, mas se recusa a autorizá-la.
- **404 Not Found**: O recurso solicitado não foi encontrado.
- **405 Method Not Allowed**: O método HTTP usado na solicitação não é permitido para o recurso.
- **406 Not Acceptable**: O recurso não é aceitável de acordo com os cabeçalhos de aceitação da solicitação.
- **407 Proxy Authentication Required**: A autenticação é necessária para acessar o recurso através de um proxy.
- **408 Request Timeout**: O cliente demorou demais para enviar a solicitação.
- **409 Conflict**: A solicitação não pôde ser completada devido a um conflito com o estado atual do recurso.
- **410 Gone**: O recurso solicitado foi removido permanentemente e não está mais disponível.
- **411 Length Required**: O cabeçalho `Content-Length` é necessário.
- **412 Precondition Failed**: Uma condição especificada nos cabeçalhos da solicitação falhou.
- **413 Payload Too Large**: O corpo da solicitação é maior do que o servidor pode processar.
- **414 URI Too Long**: A URI fornecida foi muito longa para ser processada pelo servidor.
- **415 Unsupported Media Type**: O tipo de mídia do corpo da solicitação não é suportado.
- **416 Range Not Satisfiable**: O servidor não pode fornecer a parte solicitada do recurso.
- **417 Expectation Failed**: O servidor não pode atender ao cabeçalho `Expect` da solicitação.
- **418 I'm a teapot**: (RFC 2324) O servidor é uma cafeteira e não pode processar a solicitação. (Usado humoristicamente.)
- **421 Misdirected Request**: A solicitação foi direcionada a um servidor que não pode gerar uma resposta.
- **422 Unprocessable Entity**: A solicitação é bem formada, mas não pode ser processada devido a erros semânticos.
- **423 Locked**: O recurso está bloqueado e não pode ser modificado.
- **424 Failed Dependency**: A solicitação falhou devido a uma falha em uma solicitação anterior.
- **425 Too Early**: A solicitação foi feita muito cedo e não pode ser processada.
- **426 Upgrade Required**: O cliente deve mudar para um protocolo diferente.
- **427 Unassigned**: Código de status reservado.
- **428 Precondition Required**: O servidor requer que a solicitação seja condicional.
- **429 Too Many Requests**: O cliente enviou muitas solicitações em um período de tempo curto.
- **431 Request Header Fields Too Large**: Os campos dos cabeçalhos da solicitação são muito grandes.
- **451 Unavailable For Legal Reasons**: O recurso não está disponível por razões legais.

## 5xx - Erro do Servidor
- **500 Internal Server Error**: O servidor encontrou um erro inesperado que não conseguiu processar.
- **501 Not Implemented**: O servidor não suporta a funcionalidade necessária para atender à solicitação.
- **502 Bad Gateway**: O servidor recebeu uma resposta inválida de um servidor upstream.
- **503 Service Unavailable**: O servidor está temporariamente fora de serviço ou sobrecarregado.
- **504 Gateway Timeout**: O servidor não recebeu uma resposta a tempo de um servidor upstream.
- **505 HTTP Version Not Supported**: A versão HTTP usada na solicitação não é suportada pelo servidor.
- **506 Variant Also Negotiates**: O servidor tem um erro de configuração e a negociação de conteúdo falhou.
- **507 Insufficient Storage**: O servidor não consegue armazenar a representação necessária para completar a solicitação.
- **508 Loop Detected**: O servidor detectou um loop infinito ao processar a solicitação.
- **510 Not Extended**: A solicitação não foi completada porque requer extensões adicionais.
