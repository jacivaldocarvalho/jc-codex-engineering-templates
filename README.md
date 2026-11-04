# JC Codex Engineering Templates

[![Validate](https://github.com/jacivaldocarvalho/jc-codex-engineering-templates/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/jacivaldocarvalho/jc-codex-engineering-templates/actions/workflows/validate.yml)
[![GitHub release](https://img.shields.io/github/v/release/jacivaldocarvalho/jc-codex-engineering-templates)](https://github.com/jacivaldocarvalho/jc-codex-engineering-templates/releases/1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Biblioteca de instruções modulares para OpenAI Codex, versão 1.0.0. Os templates ajudam a orientar planejamento, engenharia, segurança e validação sem depender deste repositório depois da instalação.

- **new-project:** discovery, decisões de arquitetura, bootstrap e implementação incremental.
- **existing-project:** diagnóstico, correções e evolução com preservação de contratos e compatibilidade.

Cada modelo inclui módulos especializados de frontend, backend, DevOps, DevSecOps, SRE, AI e segurança. O `AGENTS.md` instrui o Codex a consultar os módulos e padrões pertinentes sob demanda; esses arquivos complementares não são carregados automaticamente.

## Pré-requisitos

- Git e acesso ao GitHub para clonar os repositórios.
- OpenAI Codex CLI ou integração compatível já configurada.
- Bash e Python 3 com biblioteca padrão para o instalador e a validação, em ambiente Unix compatível com as operações de diretório e links usadas pelo instalador.

## Início rápido: novo projeto

1. No GitHub, crie um repositório vazio chamado, por exemplo, `minha-api`, sem README, licença ou `.gitignore`. Substitua `SEU-USUARIO` nos comandos abaixo.
2. Clone seu projeto e o repositório de templates como diretórios separados:

   ```sh
   git clone https://github.com/SEU-USUARIO/minha-api.git
   git clone https://github.com/jacivaldocarvalho/jc-codex-engineering-templates.git
   cd minha-api
   ```

   Se você já possui uma cópia dos templates, use o caminho dessa cópia no comando seguinte. O exemplo pressupõe os dois diretórios lado a lado; o destino `.` já existe por ser o projeto clonado.

3. Simule e instale o modelo:

   ```sh
   ../jc-codex-engineering-templates/scripts/install.sh --dry-run new-project .
   ../jc-codex-engineering-templates/scripts/install.sh new-project .
   ```

4. Confira os arquivos instalados e a versão:

   ```sh
   ls -la AGENTS.md .agents .agents/standards
   cat .agents/template-version
   git status --short
   ```

5. Ainda na raiz do projeto, inicie `codex` ou abra o diretório em sua integração compatível. Um primeiro pedido possível é:

   > Quero criar uma API de tarefas. Antes de implementar, faça o discovery, identifique perguntas e hipóteses e proponha uma arquitetura simples, com critérios de aceitação, segurança, testes e observabilidade.

6. Revise as instruções instaladas e versione `AGENTS.md` e `.agents/` junto com o projeto. Quando estiver pronto para criar o primeiro commit, por exemplo:

   ```sh
   git add AGENTS.md .agents/
   git commit -m "chore: add Codex project instructions"
   ```

   Se regras do `.gitignore` impedirem o rastreamento de `.agents/`, ajuste-as conforme as convenções do projeto antes de adicionar os arquivos. Publicar o commit requer um push separado.

## Projeto existente

Clone o projeto ou acesse sua cópia local. O exemplo também pressupõe uma cópia dos templates ao lado do projeto:

```sh
git clone https://github.com/SEU-USUARIO/projeto-existente.git
cd projeto-existente
../jc-codex-engineering-templates/scripts/install.sh --dry-run existing-project .
../jc-codex-engineering-templates/scripts/install.sh existing-project .
ls -la AGENTS.md .agents .agents/standards
cat .agents/template-version
```

O instalador recusa conflitos e não substitui arquivos existentes. Se já houver `AGENTS.md` ou módulos diferentes, compare e integre as instruções manualmente; preserve a hierarquia de instruções do projeto. Se existir `.entire/agent-guide.md`, revise sua compatibilidade: Entire é opcional e o instalador não altera esse arquivo. Revise as mudanças com `git status` e versione as instruções apropriadas junto com o projeto.

Abra o Codex na raiz e peça, por exemplo:

> Analise a arquitetura e os contratos existentes antes de propor alterações. Identifique os testes relevantes e os principais riscos de manutenção, sem modificar arquivos.

## Referência do instalador

```sh
caminho/para/jc-codex-engineering-templates/scripts/install.sh [--dry-run] {new-project|existing-project} DIRETÓRIO
```

O destino deve ser um diretório existente e não pode ser um link simbólico. `--dry-run` verifica a instalação sem gravar arquivos. A instalação cria `AGENTS.md`, sete módulos em `.agents/`, os padrões em `.agents/standards/` e `.agents/template-version` com modelo e versão.

Arquivos idênticos são aceitos, tornando a repetição idempotente; arquivos diferentes, links simbólicos nos caminhos verificados ou tipos incompatíveis geram erro. A verificação ocorre antes da gravação. Em caso de falha, o instalador tenta reverter os arquivos e diretórios que criou, mas o rollback não é atômico diante de interrupções abruptas, falhas do sistema ou alterações concorrentes. Use um destino sem outros processos de escrita.

Não há atualização automática. Para adotar uma versão posterior, compare os arquivos instalados com os novos templates e integre as alterações manualmente; executar novamente o instalador não sobrescreve arquivos diferentes.

## Estrutura instalada

```text
projeto/
├── AGENTS.md
└── .agents/
    ├── frontend.md, backend.md, devops.md, devsecops.md
    ├── sre.md, ai.md, security.md
    ├── template-version
    └── standards/
        └── engineering.md, architecture.md, clean-code.md, testing.md,
            security.md, observability.md, ai-finops.md
```

`AGENTS.md` contém as orientações principais. `.agents/` reúne módulos especializados e o registro de versão. `standards/`, dentro de `.agents/`, contém padrões compartilhados copiados para que o projeto de destino seja autocontido.

## Boas práticas

Inicie o Codex na raiz do projeto e solicite planejamento antes da implementação quando houver decisões a esclarecer. Peça a consulta aos módulos pertinentes à tarefa, sem presumir carregamento automático. Siga as instruções superiores, o sandbox e os mecanismos de aprovação aplicáveis; para operações críticas, consulte a política de aprovação do `AGENTS.md` instalado e obtenha as autorizações necessárias. Mantenha as instruções sob controle de versão e revise alterações manuais antes de adotá-las.

## Solução de problemas

- **Conflito:** use `--dry-run`, compare o arquivo indicado e integre as instruções manualmente; o instalador não oferece sobrescrita.
- **Permissão de execução:** confira as permissões e execute o script com Bash, por exemplo `bash ../jc-codex-engineering-templates/scripts/install.sh new-project .`. Verifique também a permissão de escrita no destino.
- **Dependência ausente:** confirme que Git, Bash, Python 3 e sua integração Codex estão disponíveis no ambiente apropriado.
- **Falha de sandbox do Codex:** erros de inicialização, como falha de configuração de loopback no `bwrap`, podem decorrer de restrições do ambiente e não comprovam defeito do template. Registre a mensagem e consulte o administrador; não desative o sandbox nem as aprovações.

## Validação e contribuição

Na raiz deste repositório, execute `./scripts/validate.sh` para verificar sintaxe e testes. O workflow executa o mesmo gate em pushes e pull requests. Para torná-lo obrigatório antes de merges, configure a proteção da branch no GitHub e exija o check `quality-gates`; o workflow sozinho não configura essa política.

Os diretórios em `examples/` sugerem módulos por contexto; não são aplicações prontas. Consulte [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md) e as evidências em [tests/VALIDATION.md](tests/VALIDATION.md).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Author

**Jacivaldo Carvalho**

Telecommunications Engineer | DevOps Engineer | SRE | Networking

[GitHub](https://github.com/jacivaldocarvalho) | [LinkedIn](https://www.linkedin.com/in/jacivaldocarvalho) | [Website](https://www.jacivaldocarvalho.com/)
