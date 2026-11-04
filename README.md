# JC Codex Engineering Templates

Biblioteca de instruções modulares para OpenAI Codex, versão 1.0.0. Escolha `new-project` para descoberta e bootstrap ou `existing-project` para evolução e manutenção de sistemas existentes.

## Instalação

Requisitos: Bash e Python 3 (biblioteca padrão) para instalação e validação. O destino deve ser um diretório existente. Na raiz deste repositório:

```sh
./scripts/install.sh --dry-run new-project /caminho/do/projeto
./scripts/install.sh new-project /caminho/do/projeto
# Alternativa: existing-project
```

O instalador verifica todos os conflitos antes de escrever, aceita arquivos idênticos e recusa sobrescritas. Em falha durante a gravação, tenta reverter os arquivos e diretórios criados. Ele não atualiza instalações automaticamente: para atualizar, compare e integre as mudanças manualmente. A versão e o modelo ficam em `.agents/template-version`. A reversão não pode garantir atomicidade diante de interrupções abruptas, falhas do sistema ou alterações concorrentes; use um destino sem outros processos de escrita.

O `AGENTS.md` instalado orienta a leitura seletiva de `.agents/*.md` e `.agents/standards/*.md`; não pressupõe carregamento automático. Todos os padrões necessários são copiados ao destino. Se relevante e presente, `.entire/agent-guide.md` pode ser lido; Entire não é exigido nem modificado. A hierarquia de instruções, o sandbox e as aprovações do Codex prevalecem.

## Validação

```sh
./scripts/validate.sh
```

O workflow executa o mesmo gate em pushes e pull requests. Para torná-lo obrigatório antes de merges, configure a proteção da branch no GitHub e exija o check `quality-gates`; o workflow sozinho não configura essa política.

Os diretórios em `examples/` indicam módulos sugeridos por contexto; não são aplicações prontas. Leia [CONTRIBUTING.md](CONTRIBUTING.md) para critérios de aceite e [CHANGELOG.md](CHANGELOG.md) para versões. Evidências locais estão em [tests/VALIDATION.md](tests/VALIDATION.md).
