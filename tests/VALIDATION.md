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


## Revisão de prontidão para release — 2026-11-04

Contexto: revisão local da versão 1.0.0, branch `main`, HEAD `0449ccca6044d5b933188f547cbb85e6a5a5d93b`. A worktree estava limpa no início. O sandbox desta sessão também falhou ao iniciar com `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; as verificações abaixo foram executadas fora dele, com autorização. Não houve alteração de configuração de segurança.

- **PASS — Gate automatizado:** `PYTHONDONTWRITEBYTECODE=1 ./scripts/validate.sh` verificou a sintaxe dos scripts shell e executou 9 testes com sucesso. Incluem integridade e referências, política textual, simulação, instalação e repetição de ambos os modelos, conflitos, links simbólicos, versão e casos de rollback com falhas injetadas. Esses testes não cobrem todas as condições de concorrência ou falhas do sistema.
- **PASS — Integridade estrutural:** os testes confirmam sete módulos e sete padrões para cada modelo e suas referências nos guias. Isso não comprova todas as interpretações ou comportamentos em execução.
- **PASS — Instalação e idempotência nos cenários testados:** simulação sem gravação, instalação e repetição com arquivos idênticos passaram para os dois modelos; conflitos e falhas injetadas foram recusados ou tratados nos casos testados. Rollback permanece de melhor esforço e não atômico.
- **PASS — Documentação e compatibilidade com o instalador:** o README descreve criação de repositório vazio, clone, simulação opcional, instalação, conferência, abertura no Codex e pedido inicial de discovery; também orienta o uso em projeto existente. As opções documentadas correspondem ao parser inspecionado. Referências locais do README e referências dos guias foram revisadas; os testes verificam os nomes dos módulos e padrões.
- **PASS — Política textual de aprovação:** os dois guias contêm a mesma política para seis categorias de alto impacto, com autorização explícita e específica; o teste automatizado verifica sua presença e igualdade. **NOT VERIFIED:** comportamento em runtime diante de solicitação de operação crítica.
- **PASS — Evidência de uso real relatada:** o usuário informou instalação em projeto real e leitura de `AGENTS.md`, consulta a módulos `.agents/` e aplicação das instruções pelo Codex durante desenvolvimento. É relato do usuário, sem logs fornecidos ou reprodução independente nesta revisão; o modelo usado e o escopo exato não foram informados.
- **NOT VERIFIED — Independência completa:** instalações temporárias anteriores e referências locais são evidência estrutural, mas não comprovam execução dos dois modelos pelo Codex sem acesso ao repositório de origem. Sessões específicas de planejamento, análise de bug e avaliação DevSecOps anteriormente não verificadas continuam sem evidência independente; o relato acima comprova apenas o uso informado.
- **PASS — Higiene local:** `git diff --check` passou antes desta atualização; `git status --short --untracked-files=all` e `git ls-files --others --exclude-standard` não mostraram alterações ou arquivos não rastreados iniciais. Busca por padrões comuns de credenciais e chaves privadas não encontrou correspondências; não é auditoria exaustiva, nem cobre histórico Git ou arquivos ignorados. README, changelog, instalador e teste referenciam 1.0.0 de forma consistente.
- **NOT VERIFIED — CI e proteção de branch:** nenhuma execução remota ou configuração do GitHub foi verificada nesta revisão. Nenhum commit, push, tag ou release foi criado.
