# Digi CPU Miner — configuração

Este repositório contém um modelo de configuração para conectar um minerador compatível ao pool DigiByte informado.

## Pool

- Endpoint: `stratum+tcp://digi.hmpool.io:3337`
- Algoritmo: SHA-256d (DigiByte)
- Worker: `cpu1`
- Arquivo de configuração: `miner.yml`

**Importante:** o arquivo YAML é um modelo genérico. O formato exato depende do programa de mineração que você escolher; confirme os nomes das opções na documentação desse minerador antes de executá-lo.

## Segurança e uso responsável

- Use apenas computadores que você possui ou tem autorização para utilizar.
- Comece com poucos threads e monitore temperatura, consumo e estabilidade.
- CPU mining pode render muito pouco ou gerar prejuízo de energia; não há garantia de ganhos.
- Nunca coloque frases-semente, chaves privadas ou credenciais pessoais neste repositório.
- GitHub Actions aqui apenas valida a presença de configurações; não executa mineração. Mineração em runners do GitHub não é configurada nem recomendada.

## Endereço de pagamento

O campo de usuário usa o endereço público DigiByte fornecido, com o identificador de worker `.cpu1`. Verifique o endereço antes de usar.
