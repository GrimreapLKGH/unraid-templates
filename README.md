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

The first use downloads speech models; afterwards voice preparation and transcription are local. Email delivery uses your configured mail provider. This beta supports x86-64 CPUs. The standard image uses CPU inference. Experimental NVIDIA generation is available in `ghcr.io/grimreaplkgh/learnmylines:beta-nvidia`: expose a compatible NVIDIA GPU to the container, then select NVIDIA GPU in the generation settings. The NVIDIA build uses CUDA 12.6 to retain older architecture support; P2000 rendering and memory use still require hardware testing. Newer GPU architectures may need a different build. CPU remains available if GPU generation fails. Sound effects use small local CPU synthesis and need no GPU.

## Voice generation

Approved voice profiles are saved and reused across imported scripts. Quiet, Balanced and Fast use 1, 2 and 5 CPU processing threads; Quiet includes a brief rest per recording. Generation may be slow on CPU, especially on first use. These settings do not regulate temperature. Saved recordings play without running the voice model. All/Both offers male or female same-speaker echoes.

Script management provides Recast, Unpublish, Clear all recordings and confirmed Delete Script. Clearing forces a fresh recording generation before republishing, while files needed by another script are retained for that script. Back up appdata before using destructive actions.

## Updates

The maintainer develops privately, tests each beta and publishes numbered images. Select the beta image while testing. Once a stable channel is published, stable users can update through Unraid's normal Docker update controls. Appdata remains outside the container. Stop the app and back up its appdata before upgrades; database changes may need the matching backup when rolling back.

## Support

Report issues at https://github.com/GrimreapLKGH/unraid-templates/issues. Include the image version, Unraid version and relevant logs with passwords, cookies, email addresses and script content removed.

## Open-source components

See LICENSING.md and COPYING-speech-worker. The image contains third-party notices and source archives under `/usr/share/learnmylines`. These licences are separate from the application licence.
