import pathlib
import importlib.util
import os
from unittest import mock
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / 'scripts/install.sh'
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
MODULES = {'frontend', 'backend', 'devops', 'devsecops', 'sre', 'ai', 'security'}
STANDARDS = {'engineering', 'architecture', 'clean-code', 'testing', 'security', 'observability', 'ai-finops'}


def install(kind, dest, dry=False):
    args = [str(INSTALL)] + (['--dry-run'] if dry else []) + [kind, str(dest)]
    return subprocess.run(args, text=True, capture_output=True)


class TemplatesTest(unittest.TestCase):
    def test_integrity_and_references(self):
        self.assertEqual({p.stem for p in (ROOT / 'standards').glob('*.md')}, STANDARDS)
        for kind in ('new-project', 'existing-project'):
            base = ROOT / 'templates' / kind
            self.assertEqual({p.stem for p in (base / '.agents').glob('*.md')}, MODULES)
            guide = (base / 'AGENTS.md').read_text()
            for name in MODULES | STANDARDS:
                self.assertIn(f'`{name}.md`', guide)
            self.assertIn('.entire/agent-guide.md', guide)

    def test_install_and_idempotence(self):
        for kind in ('new-project', 'existing-project'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                dest = pathlib.Path(tmp)
                self.assertEqual(install(kind, dest, True).returncode, 0)
                self.assertEqual(list(dest.iterdir()), [])
                first = install(kind, dest)
                self.assertEqual(first.returncode, 0, first.stderr)
                snapshot = {p.relative_to(dest): p.read_bytes() for p in dest.rglob('*') if p.is_file()}
                second = install(kind, dest)
                self.assertEqual(second.returncode, 0, second.stderr)
                self.assertEqual(snapshot, {p.relative_to(dest): p.read_bytes() for p in dest.rglob('*') if p.is_file()})
                self.assertEqual((dest / '.agents/template-version').read_text(), f'template={kind}\nversion=1.0.0\n')
                self.assertEqual({p.stem for p in (dest / '.agents/standards').glob('*.md')}, STANDARDS)

    def test_conflict_preflight_and_entire(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            (dest / '.agents').mkdir()
            (dest / '.agents/security.md').write_text('preservar')
            (dest / '.entire').mkdir()
            (dest / '.entire/agent-guide.md').write_text('entire')
            result = install('new-project', dest)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((dest / 'AGENTS.md').exists())
            self.assertEqual((dest / '.agents/security.md').read_text(), 'preservar')
            self.assertEqual((dest / '.entire/agent-guide.md').read_text(), 'entire')

    def test_invalid_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            self.assertNotEqual(install('invalid', dest).returncode, 0)
            (dest / '.agents').symlink_to(dest, target_is_directory=True)
            self.assertNotEqual(install('new-project', dest).returncode, 0)
            self.assertFalse((dest / 'AGENTS.md').exists())

    def test_late_conflict_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            (dest / '.agents').mkdir()
            (dest / '.entire').mkdir()
            (dest / '.entire/agent-guide.md').write_text('preservar')
            original = os.open
            def race(path, flags, *args, **kwargs):
                if path == 'ai.md' and flags & os.O_EXCL:
                    (dest / '.agents/ai.md').write_text('concorrente')
                return original(path, flags, *args, **kwargs)
            with mock.patch.object(installer.os, 'open', side_effect=race):
                with self.assertRaises(FileExistsError):
                    installer.install('new-project', dest)
            self.assertFalse((dest / 'AGENTS.md').exists())
            self.assertEqual((dest / '.agents/ai.md').read_text(), 'concorrente')
            self.assertEqual((dest / '.entire/agent-guide.md').read_text(), 'preservar')
            self.assertFalse((dest / '.agents/standards').exists())

    def test_write_failure_rolls_back_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            original_guide = (ROOT / 'templates/new-project/AGENTS.md').read_bytes()
            (dest / 'AGENTS.md').write_bytes(original_guide)
            original = os.write
            calls = 0
            def fail(fd, data):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError('injected write failure')
                return original(fd, data)
            with mock.patch.object(installer.os, 'write', side_effect=fail):
                with self.assertRaises(OSError):
                    installer.install('new-project', dest)
            self.assertEqual((dest / 'AGENTS.md').read_bytes(), original_guide)
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ['AGENTS.md'])

    def test_replaced_file_not_removed_on_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            original = os.write
            calls = 0
            def replace_then_fail(fd, data):
                nonlocal calls
                calls += 1
                if calls == 2:
                    (dest / 'AGENTS.md').rename(dest / 'moved')
                    (dest / 'AGENTS.md').write_text('novo dono')
                    raise OSError('injected')
                return original(fd, data)
            with mock.patch.object(installer.os, 'write', side_effect=replace_then_fail):
                with self.assertRaises(OSError):
                    installer.install('new-project', dest)
            self.assertEqual((dest / 'AGENTS.md').read_text(), 'novo dono')

    def test_version_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp)
            self.assertEqual(install('new-project', dest).returncode, 0)
            manifest = dest / '.agents/template-version'
            manifest.write_text('version=old\n')
            before = (dest / 'AGENTS.md').read_bytes()
            self.assertNotEqual(install('new-project', dest).returncode, 0)
            self.assertEqual((dest / 'AGENTS.md').read_bytes(), before)
            self.assertEqual(manifest.read_text(), 'version=old\n')


if __name__ == '__main__':
    unittest.main()
