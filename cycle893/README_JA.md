# cycle893 音声優先ダッキング

前回cycle890の自作効果音10箇所を日本語ナレーションと重なる区間で約12dB抑制する。48kHzモノラル音声を入力とし、20ms RMS・10ms attack・90ms release。10ジャンル共通、外部API不要。音声の日本語意味一致、素材権利、実機再生、人間の聴感評価、参考動画v33との直接比較は未検証。HUMAN_REVIEW / PUBLICATION_NOT_APPROVED。投稿・マージ・有料契約なし。

ローカル再現: cycle889の音声WAVとcycle890の自作SFX WAVを用意し、python cycle893/src/voice_priority.py voice.wav cues.wav mixed.wav を実行。完成動画はcycle890の映像をstream-copyし、mixed.wavをAACにエンコードする。GitHub CIは合成データのみ検証。