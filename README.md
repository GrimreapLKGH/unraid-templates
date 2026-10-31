# learnmylines for Unraid — Beta

Local play rehearsal with British character voices, microphone recording, line/scene scores, slow and fast rehearsal, group accounts and assigned scripts.

The application is proprietary freeware. You may install and use the official unmodified image without charge. Application development is private. This repository contains only the Unraid installation template, documentation and the separately licensed speech utility; it is not the application source repository. See LICENSING.md.

## Install

The beta image is `ghcr.io/grimreaplkgh/learnmylines:beta`. The Community Applications listing must be submitted and accepted before it appears in Apps. A repository alone does not create a listing.

Default host port: 8097. Container port: 8000. Appdata: `/mnt/user/appdata/learnmylines` mapped to `/data`. Configure your HTTPS reverse proxy to point at your Unraid IP and host port 8097, keeping the incoming Host header. HTTPS is required for secure login cookies and microphone access.

Read the first administrator code on the server console:

```
docker exec learnmylines cat /data/admin-setup-code
```

Open your HTTPS address and create the first administrator with an email and password. There are no bundled accounts. Import a script you have permission to use, prepare voices, publish it and assign members. Configure your own sending mailbox and public HTTPS address under Manage members if you want invitations and password resets. No scripts, accounts, credentials or recordings are included in this image.

The first use downloads speech models; afterwards voice preparation and transcription are local. Email delivery uses your configured mail provider. This beta supports x86-64 CPUs and uses CPU inference. GPU acceleration is not advertised.

## Updates

The maintainer develops privately, tests each beta and publishes numbered images. Select the beta image while testing. Once a stable channel is published, stable users can update through Unraid's normal Docker update controls. Appdata remains outside the container. Stop the app and back up its appdata before upgrades; database changes may need the matching backup when rolling back.

## Support

Report issues at https://github.com/GrimreapLKGH/unraid-templates/issues. Include the image version, Unraid version and relevant logs with passwords, cookies, email addresses and script content removed.

## Open-source components

See LICENSING.md and COPYING-speech-worker. The image contains third-party notices and source archives under `/usr/share/learnmylines`. These licences are separate from the application licence.
