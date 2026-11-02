# learnmylines for Unraid — Beta

Local play rehearsal with 52 audition-approved British voice profiles, Practice mode and Test Myself, microphone recording, line/scene scores, group accounts and assigned scripts.

The application is proprietary freeware. You may install and use the official unmodified image without charge. Application development is private. This repository contains only the Unraid installation template, documentation and the separately licensed speech utility; it is not the application source repository. See LICENSING.md.

## Install

The beta image is `ghcr.io/grimreaplkgh/learnmylines:beta`. The Community Applications listing must be submitted and accepted before it appears in Apps. A repository alone does not create a listing.

Default host port: 8097. Container port: 8000. Appdata: `/mnt/user/appdata/learnmylines` mapped to `/data`. Configure your HTTPS reverse proxy to point at your Unraid IP and host port 8097, keeping the incoming Host header. HTTPS is required for secure login cookies and microphone access.

Read the first administrator code on the server console:

```
docker exec learnmylines cat /data/admin-setup-code
```

Open your HTTPS address and create the first administrator with an email and password. There are no bundled accounts. Open Script management and import a script you have permission to use. The wizard guides you through casting, optional sound effects, local voice generation and publishing; then assign it to members. Configure your own sending mailbox and public HTTPS address under Manage members if you want invitations and password resets. No private scripts, accounts, credentials or rehearsal recordings are included. Synthetic voice audition clips are bundled.

The first use downloads speech models; afterwards voice preparation and transcription are local. Email delivery uses your configured mail provider. This beta supports x86-64 CPUs. The standard image uses CPU inference. Experimental NVIDIA generation is available in `ghcr.io/grimreaplkgh/learnmylines:beta-nvidia`: expose a compatible NVIDIA GPU to the container, then select NVIDIA GPU in the generation settings. The NVIDIA build uses CUDA 12.6 to retain older architecture support; A limited Unraid/P2000 user smoke test showed active GPU generation; full performance and audio quality have not been benchmarked. Newer GPU architectures may need a different build. CPU remains available if GPU generation fails. Sound effects use small local CPU synthesis and need no GPU.

## Voice generation

Approved voice profiles are saved and reused across imported scripts. Quiet, Balanced and Fast use 1, 2 and 5 CPU processing threads; Quiet includes a brief rest per recording. Generation may be slow on CPU, especially on first use. These settings do not regulate temperature. Saved recordings play without running the voice model. All/Both offers male or female same-speaker echoes.

Script management provides Recast, Unpublish, Clear all recordings and confirmed Delete Script. Clearing forces a fresh recording generation before republishing, while files needed by another script are retained for that script. Back up appdata before using destructive actions.

## Updates

The maintainer develops privately, tests each beta and publishes numbered images. Select the beta image while testing. Once a stable channel is published, stable users can update through Unraid's normal Docker update controls. Appdata remains outside the container. Stop the app and back up its appdata before upgrades; database changes may need the matching backup when rolling back.

## Support

Report issues at https://github.com/GrimreapLKGH/unraid-templates/issues. Include the image version, Unraid version and relevant logs with passwords, cookies, email addresses and script content removed.

## Open-source components

See LICENSING.md and COPYING-speech-worker. The image contains third-party notices and source archives under `/usr/share/learnmylines`. These licences are separate from the application licence.


## Storage, backups and rehearsal options

Version 0.1.0-beta.8 adds **Cue lines only**, **Skip line** and **Repeat previous line**, plus song lyric practice and uploaded rehearsal tracks. Cue lines only works with Practice and Test Myself. Songs can be spoken, played from an uploaded audio track, or skipped. Only spoken lyric words are scored; pitch and singing quality are not assessed.

### Storage on Unraid

- Keep `/data` mapped to the existing appdata folder: accounts, database, scripts, assignments, scores, uploads, song tracks and settings.
- Map a separate SSD-pool share such as `/mnt/user/learnmylines-working` to `/work` and set `WORK_DIR=/work`. Put this share on the SSD pool as Primary storage, with no secondary array destination if you want it to stay on SSD. Models, generated voice recordings, effects and GPU caches go here.
- Map a private array share such as `/mnt/user/learnmylines-backups` to `/backups` and set `BACKUP_DIR=/backups`. Backups can grow large; the current full backup includes downloaded models too.
- Existing installations continue using their old working folders until **Storage & backups → Move working files to SSD storage** is chosen. Make a backup first and pause generation. Migration copies and verifies files; it retains original folders in appdata. Once you have verified playback, generation and a new backup, you can manually remove the original models, speech-cache, sound-effects and cuda-cache folders from the old appdata location. Never remove the database, uploads or settings.
- New template settings do not automatically appear in an existing saved Unraid container: add the two path mappings and two environment variables when upgrading. Keep the existing `/data` mapping.
- The GPU software itself still occupies Docker image storage. Moving working files does not make those installed libraries smaller. Check total Docker utilisation and allow update headroom before installing; do not prune unrelated containers or delete docker.img.

### Backup and restore

**Storage & backups** offers manual, daily or weekly backups, retention limits, verified archive creation and last-success status. Pause generation first. All appdata and working files are backed up, including recordings, effects, custom files, uploaded tracks and downloaded models. Filesystem links within model caches are recorded without duplicating their content in the backup archive. Archives contain private accounts, password hashes and mail credentials: keep the backup share private.

On a fresh installation, backups in the configured folder are detected. Enter the new installation's setup code to list and restore one before creating an administrator. Restored accounts are used for login; old login sessions are invalidated. The app refuses restoration over an installation containing accounts, scripts or scores. Checksums and database integrity are verified before restoring. Keep enough free appdata space to stage the restore; archive size may be smaller than the required uncompressed space.

The public template uses a PNG icon for Unraid compatibility. Browser pages include the matching favicon. Existing saved containers may need their icon URL updated to `https://raw.githubusercontent.com/GrimreapLKGH/unraid-templates/main/icon.png` and the browser refreshed.

New installations limit Docker logs to three 10 MB files. Existing GPU installations can append `--log-driver=json-file --log-opt max-size=10m --log-opt max-file=3` to Extra Parameters while retaining `--gpus=all`. This limits log growth; it does not reduce installed GPU libraries.

### Correct a blended dialogue line

Open **Review script → Edit → Split a blended dialogue line**. Place the cursor in Original text just before the second speech, choose **Split at cursor**, then check the first character and spoken words. Choose the second character (including any configured main character name), check the second speech and choose **Save split into two lines**. The script is unpublished. Generate missing recordings and publish again; unchanged audio is reused. Changed lines need new attempts; existing history is retained. The importer also recognises a known character followed by a tab when its colon is missing.
