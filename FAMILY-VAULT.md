# Family Vault for Unraid — Beta

A private home for your family's memories, with shared and personal libraries,
family invitations, albums and import review. Photos stay on your server.

## Install

Image: `ghcr.io/grimreaplkgh/family-vault:beta` (x86-64).
Use the Family Vault Community Applications template when the listing is available.
Default host port is 8999; the container port remains 8080.

Choose storage locations during installation:

| Setting | Container path | Contents |
| --- | --- | --- |
| Application data | `/data` | Accounts, database, thumbnails, reference photos, protected account-removal archives |
| Photo storage | `/data/originals` | Uploaded original photos, videos and files |

Photo storage can be a dedicated folder on an array share, pool, Unassigned Device
or network share already mounted in Unraid. Select its host path, for example
`/mnt/user/Photos/FamilyVault`, `/mnt/disks/your-drive/FamilyVault` or a mounted
folder under `/mnt/remotes`. Direct SMB URLs are not accepted. Ensure the mount
is available before starting the app; start it after the remote mount on reboot.
Remote/unusual filesystems have not all been tested. Use local appdata storage
for SQLite; choose writable dedicated folders for UID 99 / GID 100.

Set Application URL to the exact browser address, such as
`https://familyvault.example.com`. Behind an HTTPS proxy, forward internally using
HTTP to your Unraid IP and host port 8999. TLS terminates at the proxy.

For a fresh install, read the protected first-admin code in the Unraid terminal:

```sh
docker exec family-vault cat /data/admin-setup-code
```

Enter that code on the setup page and create the administrator. No accounts,
passwords or photos are bundled. Existing configured installations do not require
another setup code. Optional SMTP settings deliver invitations; otherwise copy links.

## Free and Pro testing

Free has a 500 MB installation-wide storage limit. Paid lifetime activation and
Google cloud backup are not implemented. The optional Allow Pro testing setting
enables the administrator's Settings switch for evaluating trees, custom tags
and local face matching. It is not a purchased licence. Face suggestions require
confirmation. Duplicate/blur checks are warnings and may need human review.

## Updating your existing manual installation

Stop the container and back up both appdata and original photo storage together.
Edit the existing container, change Repository from `family-vault:0.1.0-test` to
`ghcr.io/grimreaplkgh/family-vault:beta`, retain ALL existing storage mappings,
port and APP_URL, and apply. Do not install a second container against the same
appdata. Your current photos and accounts remain in their existing folders.
The beta tag receives tested releases; Unraid's normal Docker update controls
download them. New template variables may need adding manually to existing installs.

To relocate originals later, stop the container, copy the complete originals folder
to the new location, verify the copy, then change Photo storage to that folder.
Keep the database/appdata mapping. Changing a mapping alone does not move photos.

Keep backups before each upgrade. A rollback may require the matching database
backup as well as the previous numbered image. Initial release smoke checks cover
fresh setup and container replacement; they do not guarantee every future schema
migration. Release checks must grow when migrations are introduced.

## Admin password recovery

Use the Unraid terminal. This prompts for your active admin email and a hidden new
password; it revokes that admin's sessions and leaves photos/settings unchanged:

```sh
docker exec -it family-vault python -c '
import sqlite3, getpass
from werkzeug.security import generate_password_hash
c=sqlite3.connect("file:/data/familyloom.sqlite3?mode=rw", uri=True)
email=input("Admin email: ").strip()
u=c.execute("SELECT id FROM users WHERE email=? COLLATE NOCASE AND role=? AND active=1",(email,"admin")).fetchone()
if not u: raise SystemExit("No active admin with that email. Nothing changed.")
p=getpass.getpass("New password (12-256 characters): ")
q=getpass.getpass("Confirm password: ")
if p!=q or not 12<=len(p)<=256: raise SystemExit("Passwords differ or invalid length. Nothing changed.")
with c:
 c.execute("UPDATE users SET password_hash=? WHERE id=?",(generate_password_hash(p),u[0]))
 c.execute("DELETE FROM sessions WHERE user_id=?",(u[0],))
print("Password reset. Sign in again.")
'
```

## Support

Report Family Vault issues at https://github.com/GrimreapLKGH/unraid-templates/issues.
Include version, Unraid version and relevant redacted errors. Never attach account
databases, face references, private photos, passwords or session cookies.
Application source is maintained privately. Official beta use is permitted without
charge; third-party components retain their own licences.
