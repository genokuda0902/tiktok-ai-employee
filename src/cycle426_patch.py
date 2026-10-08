from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
s=s.replace('cycle418','cycle426').replace('"cycle":418','"cycle":426')
s=s.replace('"previous_reviewed_cycle":415','"previous_reviewed_cycle":425')
s=s.replace('会議メモ、毎回手作業？','その返信、送信前に確認！')
s=s.replace('会議メモ、\\nまだ手作業？','AI返信、\\nそのまま送る？')
s=s.replace('AI × 仕事効率化 / 会議メモ','AI × 仕事効率化 / 根拠確認')
Path('src/cycle426_native_japanese.py').write_text(s)
print('prepared native Japanese candidate')
