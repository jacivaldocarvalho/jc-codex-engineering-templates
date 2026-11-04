#!/usr/bin/env python3
"""Install templates without overwriting destination files."""
import argparse
import os
from pathlib import Path
import stat
import sys

BASE = Path(__file__).resolve().parent.parent
VERSION = '1.0.0'
FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def install(kind, destination, dry=False):
    dest = Path(destination)
    if dest.is_symlink() or not dest.is_dir():
        raise ValueError('destino deve ser um diretório existente, não um link simbólico')
    source = BASE / 'templates' / kind
    files = [('AGENTS.md', (source / 'AGENTS.md').read_bytes())]
    for directory, prefix in ((source / '.agents', '.agents/'), (BASE / 'standards', '.agents/standards/')):
        for path in sorted(directory.glob('*.md')):
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'origem inválida: {path}')
            files.append((prefix + path.name, path.read_bytes()))
    files.append(('.agents/template-version', f'template={kind}\nversion={VERSION}\n'.encode()))
    fds = {'': os.open(dest, FLAGS)}
    created_dirs, created = [], []
    try:
        # Keep directory descriptors open so later operations cannot follow swapped symlinks.
        for name, parent, leaf in (('.agents', '', '.agents'), ('.agents/standards', '.agents', 'standards')):
            if fds[parent] is None:
                fds[name] = None
                continue
            try:
                fds[name] = os.open(leaf, FLAGS, dir_fd=fds[parent])
            except FileNotFoundError:
                fds[name] = None
        existing = {}
        for path, data in files:
            parent, _, leaf = path.rpartition('/')
            fd = fds[parent]
            if fd is None:
                existing[path] = False
                continue
            try:
                filefd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            except FileNotFoundError:
                existing[path] = False
                continue
            with os.fdopen(filefd, 'rb') as stream:
                st = os.fstat(stream.fileno())
                if not stat.S_ISREG(st.st_mode) or stream.read() != data:
                    raise ValueError(f'conflito: {path}')
                existing[path] = (st.st_dev, st.st_ino)
        if dry:
            return
        for name, parent, leaf in (('.agents', '', '.agents'), ('.agents/standards', '.agents', 'standards')):
            if fds[name] is None:
                os.mkdir(leaf, dir_fd=fds[parent])
                st = os.stat(leaf, dir_fd=fds[parent], follow_symlinks=False)
                created_dirs.append((fds[parent], leaf, st.st_dev, st.st_ino))
                fds[name] = os.open(leaf, FLAGS, dir_fd=fds[parent])
        for path, data in files:
            parent, _, leaf = path.rpartition('/')
            fd = fds[parent]
            if existing[path]:
                # Revalidate files accepted during preflight before completing.
                check = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                with os.fdopen(check, 'rb') as stream:
                    st = os.fstat(stream.fileno())
                    if (st.st_dev, st.st_ino) != existing[path] or not stat.S_ISREG(st.st_mode) or stream.read() != data:
                        raise ValueError(f'conflito concorrente: {path}')
                continue
            filefd = os.open(leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o666, dir_fd=fd)
            try:
                st = os.fstat(filefd)
                created.append((fd, leaf, st.st_dev, st.st_ino))
                view = memoryview(data)
                while view:
                    count = os.write(filefd, view)
                    if count <= 0:
                        raise OSError('falha de escrita')
                    view = view[count:]
            finally:
                os.close(filefd)
    except BaseException:
        for fd, leaf, dev, ino in reversed(created):
            try:
                st = os.stat(leaf, dir_fd=fd, follow_symlinks=False)
                if (st.st_dev, st.st_ino) == (dev, ino):
                    os.unlink(leaf, dir_fd=fd)
            except FileNotFoundError:
                pass
        for fd, leaf, dev, ino in reversed(created_dirs):
            try:
                st = os.stat(leaf, dir_fd=fd, follow_symlinks=False)
                if (st.st_dev, st.st_ino) == (dev, ino):
                    os.rmdir(leaf, dir_fd=fd)
            except OSError:
                pass
        raise
    finally:
        for fd in reversed(list(fds.values())):
            if fd is not None:
                os.close(fd)


def main():
    parser = argparse.ArgumentParser(description='Instala templates sem sobrescrever arquivos.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('kind', choices=['new-project', 'existing-project'])
    parser.add_argument('destination')
    args = parser.parse_args()
    try:
        install(args.kind, args.destination, args.dry_run)
    except (OSError, ValueError) as exc:
        print(f'Erro: {exc}', file=sys.stderr)
        return 1
    print(f'{"Simulação" if args.dry_run else "Instalado"}: {args.kind} {VERSION} em {args.destination}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
