# PHP 5.4.45 RPM for AlmaLinux 8

This repository provides a custom RPM build of **PHP 5.4.45** adapted to run on **AlmaLinux 8**, by modifying the legacy Remi spec files.

## 🧠 Why?

PHP 5.4 reached EOL in 2015 and is not supported on modern RHEL-based systems.
However, some legacy systems still depend on it.

This project aims to **rebuild PHP 5.4 for AlmaLinux 8**, mainly for legacy compatibility and system migration testing.

## 🔧 What's included?

* Custom `php-5.4.45` SPEC file based on Remi's original RPM
* Adjusted dependencies for glibc, OpenSSL, libcurl, and systemd support on EL8
* Builds cleanly using standard `rpmbuild`
* Successfully runs on AlmaLinux 8.9 (x86\_64)

## ⚠️ Warning

This is **not intended for production use**.
PHP 5.4 has reached end-of-life and includes multiple known security vulnerabilities (CVEs).
Use only for internal testing or migration assessments.

## 📦 How to Build

```bash
# Install build tools if not already installed
dnf install rpm-build rpmdevtools -y

# Clone and build
git clone https://github.com/redadmin-k/php54-almalinux8.git
cd php54-almalinux8
rpmbuild -bb SPECS/php.spec
```

## 🤝️ Maintainer

[@redadmin-k](https://github.com/redadmin-k),
Contributor to the AlmaLinux Project.
