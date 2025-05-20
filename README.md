# PHP 5.4.45 for AlmaLinux 8

This repository provides a custom RPM build of **PHP 5.4.45** adapted to run on **AlmaLinux 8**, by modifying the legacy Remi spec files.

## 🧠 Why?

PHP 5.4 reached EOL in 2015 and is not supported on modern RHEL-based systems.  
However, some legacy systems still depend on it.

This project aims to **rebuild PHP 5.4 for AlmaLinux 8**, mainly for legacy compatibility and system migration testing.

## 🔧 What's included?

- Custom `php-5.4.45` SPEC file based on Remi's original RPM
- Adjusted dependencies for glibc, OpenSSL, libcurl, and systemd support on EL8
- Builds cleanly using `mock` or standard `rpmbuild`
- Successfully runs on AlmaLinux 8.9 (x86_64)

## ⚠️ Warning

This is **not for production use**.  
PHP 5.4 contains known security vulnerabilities. This RPM is only for testing and compatibility purposes.

## 📦 How to Build

```bash
dnf install rpm-build rpmdevtools
git clone https://github.com/redadmin-k/php54-almalinux8.git
cd php54-almalinux8
rpmbuild -bb SPECS/php54.spec

