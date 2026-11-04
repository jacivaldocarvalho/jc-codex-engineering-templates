# Evidências de validação

Data: 2026-11-03. Comando: `PYTHONDONTWRITEBYTECODE=1 ./scripts/validate.sh`.

- `bash -n` verificou a sintaxe dos dois scripts shell.
- `python3 -m unittest discover -s tests -v`: 8 testes passaram. Cobertura: integridade e referências; instalação, simulação e repetição dos dois modelos; conflitos prévios, versão e links simbólicos; preservação de Entire; conflito concorrente após pré-validação; falha de escrita com rollback e preservação de arquivo existente; e preservação de arquivo substituído antes do rollback.
- Os testes de concorrência e falha usam injeção determinística nas chamadas de sistema. O workflow executa as mesmas verificações; execução no GitHub e proteção de branch não foram verificadas localmente.

Limitação: rollback é de melhor esforço; interrupção abrupta, falha de sistema ou alterações concorrentes podem deixar arquivos parciais. A verificação de identidade e remoção não são uma operação atômica frente a concorrentes hostis; use um destino sem outros processos de escrita. Python 3 é necessário para instalação e testes; nenhuma dependência externa foi instalada.

## Correção da política de aprovação — 2026-11-03

- `PYTHONDONTWRITEBYTECODE=1 ./scripts/validate.sh`: sintaxe shell válida e 9 testes passaram, incluindo a presença dos seis tipos de operação, autorização específica e consistência da política nos dois guias.
- Instalações reais em diretórios temporários de `/tmp`: ambos os modelos instalaram com sete módulos, sete padrões, referências locais, versão `1.0.0` e política de aprovação. Os diretórios foram removidos após a verificação. A ausência do caminho do repositório nos Markdown foi verificada; isso não demonstra execução independente do Codex.
- Inspeção estática: os guias orientam descoberta, inspeção, preservação de contratos, seleção de módulos e aprovação; DevOps, DevSecOps e Security separam responsabilidades. Isso não demonstra comportamento do agente.
- Sessões reais de planejamento de API, análise de bug, avaliação DevSecOps, operação crítica e seleção de módulos: **NOT VERIFIED**. O executável `codex-cli 0.166.0` está disponível, mas o sandbox do ambiente falhou ao inicializar; não foi possível assegurar uma sessão sem acesso a credenciais e recursos externos. Nenhuma operação crítica foi executada.
- `git diff --check` passou. A versão não foi alterada; não houve commit, push ou tag.
