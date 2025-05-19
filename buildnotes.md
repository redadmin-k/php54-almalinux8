# Build Notes

This RPM rebuild of PHP 5.4.45 is based on Remi's `php54.spec`, adapted and modernized for AlmaLinux 8.

## ✅ Key Changes

- Base: Remi's `php54.spec` (originally for CentOS 7)
- Removed obsolete or CentOS 7-specific conditionals
- Ensured compatibility with:
  - `glibc 2.28` (default in AlmaLinux 8)
  - `OpenSSL 1.1+` (system default)
  - `libnsl` via compat-lib package
- Cleaned up spec macros and paths for AlmaLinux 8 environment

## ✅ Supported SAPI Modes

The RPM can be used in multiple environments:

- **mod_php**: Compatible when using `httpd` with `prefork MPM`
- **php-fpm**: Can be launched via `systemctl start php-fpm`
- **CLI**: Installed to `/usr/bin/php` for use in scripts or terminal

## ✅ Build Environment

- OS: AlmaLinux 8.9 Minimal
- Required packages:
  - `dnf groupinstall "Development Tools"`
  - `dnf install rpm-build`

## 🔧 Build Method

```bash
rpmbuild --rebuild SRPMS/php-5.4.45-1.src.rpm

