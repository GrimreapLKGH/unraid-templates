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


## What’s new in 0.1.0-beta.9

- A first-sign-in guide and a clear top menu for rehearsal, session details and cue cards.
- **Practice My Lines** keeps lines visible and advances after a one-second pause without recording. **Check My Lines** records and scores with optional automatic continuation. **Cue Lines Only** plays just your cues and scores automatically. **Custom Session** keeps the existing controls in a collapsible panel.
- **Session Details** shows rehearsal time and word accuracy by day. **Directors Area → Members** adds member activity, script and scene progress, and rehearsal data reset.
- **Cue Cards** groups nearby turns within the same scene and lays out two cards per A4 sheet. Print them, download a PDF, or email the PDF to your sign-in address using the installation’s configured mail service.

## Storage, backups and rehearsal options

Version 0.1.0-beta.8 adds **Cue lines only**, **Skip line** and **Repeat previous line**, plus song lyric practice and uploaded rehearsal tracks. Cue lines only works with Practice and Test Myself. Songs can be spoken, played from an uploaded audio track, or skipped. Only spoken lyric words are scored; pitch and singing quality are not assessed.

### Storage on Unraid

The install template shows three editable host folders with help text. Create separate shares for working storage and backups and choose where each share lives in Unraid.

| Unraid field | Default host folder | Container path |
| --- | --- | --- |
| Appdata | `/mnt/user/appdata/learnmylines` | `/data` |
| SSD working storage | `/mnt/user/learnmylines-working` | `/work` |
| Backup storage | `/mnt/user/learnmylines-backups` | `/backups` |

Set the working share's Primary storage to your SSD pool and leave Secondary storage unset if you want the files to stay on SSD. Put the backup share on the array and keep it private. Use separate folders with no overlap.

### Migrate an existing installation

1. Stop learnmylines and make a copy of its existing appdata. Update to beta.8 or later and keep the existing host folder mapped to `/data` so learnmylines can find your accounts, scripts, scores, uploads and settings.
2. In **Docker → learnmylines → Edit**, add any missing path mappings for `/work` and `/backups`. Add the variables `WORK_DIR=/work` and `BACKUP_DIR=/backups` if missing. Apply the changes. Existing containers use their saved settings, so check the fields even if you just updated the image.
3. Sign in as an administrator. Pause recording generation, open **Storage & backups**, and choose **Back up now**. Wait for the backup to complete, then select **Move working files to SSD storage**.
4. The app copies and verifies the working files before switching to the new location. The original working folders in appdata are retained as a safety copy. Check playback, generate a recording and make a new backup.

- The GPU software itself still occupies Docker image storage. Moving working files does not make those installed libraries smaller. Check total Docker utilisation and allow update headroom before installing; do not prune unrelated containers or delete docker.img.

### Backup and restore

**Storage & backups** offers manual, daily or weekly backups, retention limits, verified archive creation and last-success status. Pause generation first. All appdata and working files are backed up, including recordings, effects, custom files, uploaded tracks and downloaded models. Filesystem links within model caches are recorded without duplicating their content in the backup archive. Archives contain private accounts, password hashes and mail credentials: keep the backup share private.

On a fresh installation, backups in the configured folder are detected. Enter the new installation's setup code to list and restore one before creating an administrator. Restored accounts are used for login; old login sessions are invalidated. The app refuses restoration over an installation containing accounts, scripts or scores. Checksums and database integrity are verified before restoring. Keep enough free appdata space to stage the restore; archive size may be smaller than the required uncompressed space.

The public template uses a PNG icon for Unraid compatibility. Browser pages include the matching favicon. Existing saved containers may need their icon URL updated to `https://raw.githubusercontent.com/GrimreapLKGH/unraid-templates/main/icon.png` and the browser refreshed.

New installations limit Docker logs to three 10 MB files. Existing GPU installations can append `--log-driver=json-file --log-opt max-size=10m --log-opt max-file=3` to Extra Parameters while retaining `--gpus=all`. This limits log growth; it does not reduce installed GPU libraries.

### Correct a blended dialogue line

Open **Review script → Edit → Split a blended dialogue line**. Place the cursor in Original text just before the second speech, choose **Split at cursor**, then check the first character and spoken words. Choose the second character (including any configured main character name), check the second speech and choose **Save split into two lines**. The script is unpublished. Generate missing recordings and publish again; unchanged audio is reused. Changed lines need new attempts; existing history is retained. The importer also recognises a known character followed by a tab when its colon is missing.

Model transport caches, Torch/Numba caches and temporary files use mapped runtime-cache storage rather than the container writable layer. Existing installations without WORK_DIR keep these under appdata until SSD storage is configured and migrated.
