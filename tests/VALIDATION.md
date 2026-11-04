# Evidências de validação

Data: 2026-11-03. Comando: `PYTHONDONTWRITEBYTECODE=1 ./scripts/validate.sh`.

- `bash -n` verificou a sintaxe dos dois scripts shell.
- `python3 -m unittest discover -s tests -v`: 8 testes passaram. Cobertura: integridade e referências; instalação, simulação e repetição dos dois modelos; conflitos prévios, versão e links simbólicos; preservação de Entire; conflito concorrente após pré-validação; falha de escrita com rollback e preservação de arquivo existente; e preservação de arquivo substituído antes do rollback.
- Os testes de concorrência e falha usam injeção determinística nas chamadas de sistema. O workflow executa as mesmas verificações; execução no GitHub e proteção de branch não foram verificadas localmente.

Limitação: rollback é de melhor esforço; interrupção abrupta, falha de sistema ou alterações concorrentes podem deixar arquivos parciais. A verificação de identidade e remoção não são uma operação atômica frente a concorrentes hostis; use um destino sem outros processos de escrita. Python 3 é necessário para instalação e testes; nenhuma dependência externa foi instalada.
