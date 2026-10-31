The MIT licence at this repository's root applies to the Unraid installation template, repository metadata, icon and documentation only. It does not license the proprietary learnmylines application.

speech-worker.py is a separate utility under GPL-3.0-or-later; see COPYING-speech-worker. That utility loads Kokoro-ONNX, phonemizer and eSpeak NG and communicates with the application using text requests and WAV audio over a pipe. It contains no accounts, script parsing, assignments, scoring or application HTTP-server implementation.

The application is distributed under its own Freeware Licence in the official image. Third-party components keep their own licences. The official image includes notices and corresponding source archives for bundled open-source components under /usr/share/learnmylines.
