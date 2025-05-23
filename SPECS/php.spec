# remirepo spec file for php54-php
# with SCL and backport stuff, adapted from
#
# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%if 0%{?scl:1}
%scl_package php
%else
%global pkg_name          %{name}
%global _root_sysconfdir  %{_sysconfdir}
%global _root_bindir      %{_bindir}
%global _root_sbindir     %{_sbindir}
%global _root_includedir  %{_includedir}
%global _root_libdir      %{_libdir}
%global _root_prefix      %{_prefix}
%global _root_initddir    %{_initddir}
%endif

# API/ABI check
%global apiver      20100412
%global zendver     20100525
%global pdover      20080721
# Extension version
%global oci8ver     1.4.9

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 5.4

# Ugly hack. Harcoded values to avoid relocation.
%global _httpd_mmn         %(cat %{_root_includedir}/httpd/.mmn 2>/dev/null || echo 0)
%global _httpd_confdir     %{_root_sysconfdir}/httpd/conf.d
%global _httpd_moddir      %{_libdir}/httpd/modules
%global _root_httpd_moddir %{_root_libdir}/httpd/modules
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
# httpd 2.4 values
%global _httpd_apxs        %{_root_bindir}/apxs
%global _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.modules.d
%global _httpd_contentdir  /usr/share/httpd
%else
# httpd 2.2 values
%global _httpd_apxs        %{_root_sbindir}/apxs
%global _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.d
%global _httpd_contentdir  /var/www
%endif

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)

%global mysql_sock %(mysql_config --socket  2>/dev/null || echo /var/lib/mysql/mysql.sock)

# See exclude line in mock configuration
%global oraclever 12.1
%global oraclemax 13

# Build for LiteSpeed Web Server (LSAPI)
%global with_lsws     1

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %global runselftest 1}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_root_libdir}/mysql/mysql_config

# Optional components; pass "--with mssql" etc to rpmbuild.
%global with_oci8     %{?_with_oci8:1}%{!?_with_oci8:0}

%global with_imap      1
%global with_interbase 1
%global with_mcrypt    1
%global with_freetds   1
%global with_tidy      1
%global with_sqlite3   1
%global with_enchant   1
%global with_recode    1
%global with_t1lib     1
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_libpcre      1
%else
%global with_libpcre      0
%endif

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# systemd to manage the service, Fedora >= 15
# systemd with notify mode, Fedora >= 16
# systemd with additional service config
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
# httpd 2.4.10 with httpd-filesystem and sethandler support
%if 0%{?fedora} >= 21
%global with_httpd2410 1
%else
%global with_httpd2410 0
%endif

%global with_zip     0

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

#global rcver RC1

Summary: PHP scripting language for creating dynamic web sites
Name: %{?scl_prefix}php
Version: 5.4.45
Release: 19%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}%{?rcver}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: php.conf2
Source11: php-fpm.init

# Build fixes
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.4.35-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.4.7-libdb.patch

# Fixes for extension modules
# https://bugs.php.net/63171 no odbc call during timeout
Patch21: php-5.4.7-odbctimer.patch

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch41: php-5.4.0-easter.patch
Patch42: php-5.4.34-systzdata-v11.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.4.8-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-5.4.9-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.4.9-phpinfo.patch
# Allow multiple paths in ini_scan_dir
Patch48: php-5.4.16-iniscan.patch
# Add CURL_SSLVERSION_* constant
Patch49: php-5.4.45-curltls.patch

# RC Patch
Patch91: php-5.3.7-oci8conf.patch

# Upstream fixes (100+)
# Backported from 5.5.18 for https://bugs.php.net/65641
Patch100: php-5.4.33-bug65641.patch
# Backported from 5.5.16 for https://bugs.php.net/67635
Patch101: php-5.4.38-systemd.patch
# Backported from 5.5.14 for https://bugs.php.net/50444
Patch102: php-5.4.39-bug50444.patch

# Security fixes (200+)
Patch200: bug69720.patch
Patch201: bug70433.patch
Patch202: bug70755.patch
Patch203: bug70728.patch
Patch204: bug70741.patch
Patch205: bug70661.patch
Patch206: bug71354.patch
Patch207: bug71335.patch
Patch208: bug71391.patch
Patch209: bug71323.patch
Patch210: bug71459.patch
Patch211: bug71039.patch
Patch212: bug71488.patch
Patch213: pcre838.patch
Patch214: bug71498.patch
Patch215: bug71587.patch
Patch216: bug71860.patch
Patch217: bug71906.patch
Patch218: bug71798.patch
Patch219: bug71704.patch
Patch220: bug71527.patch
Patch221: bug64938.patch
Patch222: bug71912.patch
Patch223: bug72061.patch
Patch224: bug72093.patch
Patch225: bug72094.patch
Patch226: bug72099.patch
Patch227: bug71331.patch
Patch228: bug72114.patch
Patch229: bugoverflow.patch
Patch230: bug72135.patch
Patch231: bug72241.patch
Patch232: bug66387.patch
Patch233: bug72340.patch
Patch234: bug72275.patch
# For #72400, #72403, #72268
Patch235: bug72400.patch
Patch236: bug72339.patch
Patch237: bug72298.patch
Patch238: bug72402.patch
Patch239: bug72433.patch
Patch240: bug72434.patch
Patch241: bug72455.patch
Patch242: bug72446.patch
Patch243: bug70480.patch
Patch244: bug69975.patch
Patch245: bug72479.patch
Patch246: bug72573.patch
Patch247: bug72513.patch
Patch248: bug72520.patch
Patch249: bug72533.patch
Patch250: bug72562.patch
Patch251: bug72603.patch
Patch252: bug72606.patch
Patch253: bug72613.patch
Patch254: bug72618.patch
Patch255: bug72519.patch
Patch256: bug72735.patch
Patch257: bug72627.patch
Patch258: bug72926.patch
Patch259: bug73035.patch
Patch260: bug72928.patch
Patch261: bug73737.patch
Patch262: bug73764.patch
Patch263: bug73768.patch
Patch264: bug73773.patch
Patch265: bug73549.patch
Patch266: bug73868.patch
Patch267: bug73869.patch
Patch268: bug74435.patch
Patch269: bug75571.patch
Patch270: bug75981.patch
Patch271: bug76582.patch
Patch272: bug77153.patch
Patch273: bug77020.patch
Patch274: bug77231.patch
Patch275: bug77242.patch
Patch276: bug77380.patch
Patch277: bug78599.patch
Patch278: bug81719.patch

# Fixes for tests (300+)
# Backported from 5.5
Patch300: php-5.4.42-datetests-1.patch
# no_NO issue
Patch301: php-5.4.42-datetests-2.patch
# Revert changes for pcre < 8.34
Patch302: php-5.4.42-oldpcre.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, %{db_devel}, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
%if %{with_httpd2410}
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
%endif
BuildRequires: libstdc++-devel, openssl-devel
%if %{with_sqlite3}
# For SQLite3 extension
BuildRequires: sqlite-devel >= 3.6.0
%else
# Enough for pdo_sqlite
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if %{with_libpcre}
BuildRequires: pcre-devel >= 8.20
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
Requires: httpd-mmn = %{_httpd_mmn}
Provides: %{?scl_prefix}mod_php = %{version}-%{release}
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{?scl_prefix}php-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
%if %{with_httpd2410}
Requires(pre): httpd-filesystem
%else
Requires(pre): httpd
%endif


# Don't provides extensions, or shared libraries (embedded)
%{?filter_from_requires: %filter_from_requires /libphp5.*so/d}
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

This package contains the module (often referred to as mod_php)
which adds support for the PHP language to system Apache HTTP Server.


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-cgi = %{version}-%{release}, %{?scl_prefix}php-cgi%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-pcntl, %{?scl_prefix}php-pcntl%{?_isa}
Provides: %{?scl_prefix}php-readline, %{?scl_prefix}php-readline%{?_isa}

%description cli
The %{?scl_prefix}php-cli package contains the command-line interface
executing PHP scripts, %{_bindir}/php, and the CGI interface.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
Requires(pre): %{_root_sbindir}/useradd
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
%if %{with_systemd}
BuildRequires: systemd-devel
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%else
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif
%if %{with_httpd2410}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.


%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: %{?scl_prefix}php-embedded-devel = %{version}-%{release}
Provides: %{?scl_prefix}php-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The %{?scl_prefix}php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.


%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
Provides: %{?scl_prefix}php-api = %{apiver}%{isasuffix}
Provides: %{?scl_prefix}php-zend-abi = %{zendver}%{isasuffix}
Provides: %{?scl_prefix}php(api) = %{apiver}%{isasuffix}
Provides: %{?scl_prefix}php(zend-abi) = %{zendver}%{isasuffix}
Provides: %{?scl_prefix}php(language) = %{version}
Provides: %{?scl_prefix}php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: %{?scl_prefix}php-bz2, %{?scl_prefix}php-bz2%{?_isa}
Provides: %{?scl_prefix}php-calendar, %{?scl_prefix}php-calendar%{?_isa}
Provides: %{?scl_prefix}php-core = %{version}, %{?scl_prefix}php-core%{?_isa} = %{version}
Provides: %{?scl_prefix}php-ctype, %{?scl_prefix}php-ctype%{?_isa}
Provides: %{?scl_prefix}php-curl, %{?scl_prefix}php-curl%{?_isa}
Provides: %{?scl_prefix}php-date, %{?scl_prefix}php-date%{?_isa}
Provides: %{?scl_prefix}php-ereg, %{?scl_prefix}php-ereg%{?_isa}
Provides: %{?scl_prefix}php-exif, %{?scl_prefix}php-exif%{?_isa}
Provides: %{?scl_prefix}php-fileinfo, %{?scl_prefix}php-fileinfo%{?_isa}
Provides: %{?scl_prefix}php-filter, %{?scl_prefix}php-filter%{?_isa}
Provides: %{?scl_prefix}php-ftp, %{?scl_prefix}php-ftp%{?_isa}
Provides: %{?scl_prefix}php-gettext, %{?scl_prefix}php-gettext%{?_isa}
Provides: %{?scl_prefix}php-gmp, %{?scl_prefix}php-gmp%{?_isa}
Provides: %{?scl_prefix}php-hash, %{?scl_prefix}php-hash%{?_isa}
Provides: %{?scl_prefix}php-mhash = %{version}, %{?scl_prefix}php-mhash%{?_isa} = %{version}
Provides: %{?scl_prefix}php-iconv, %{?scl_prefix}php-iconv%{?_isa}
Provides: %{?scl_prefix}php-json, %{?scl_prefix}php-json%{?_isa}
Provides: %{?scl_prefix}php-libxml, %{?scl_prefix}php-libxml%{?_isa}
Provides: %{?scl_prefix}php-openssl, %{?scl_prefix}php-openssl%{?_isa}
Provides: %{?scl_prefix}php-phar, %{?scl_prefix}php-phar%{?_isa}
Provides: %{?scl_prefix}php-pcre, %{?scl_prefix}php-pcre%{?_isa}
Provides: %{?scl_prefix}php-reflection, %{?scl_prefix}php-reflection%{?_isa}
Provides: %{?scl_prefix}php-session, %{?scl_prefix}php-session%{?_isa}
Provides: %{?scl_prefix}php-shmop, %{?scl_prefix}php-shmop%{?_isa}
Provides: %{?scl_prefix}php-simplexml, %{?scl_prefix}php-simplexml%{?_isa}
Provides: %{?scl_prefix}php-sockets, %{?scl_prefix}php-sockets%{?_isa}
Provides: %{?scl_prefix}php-spl, %{?scl_prefix}php-spl%{?_isa}
Provides: %{?scl_prefix}php-standard = %{version}, %{?scl_prefix}php-standard%{?_isa} = %{version}
Provides: %{?scl_prefix}php-tokenizer, %{?scl_prefix}php-tokenizer%{?_isa}
%if %{with_zip}
Provides: %{?scl_prefix}php-zip, %{?scl_prefix}php-zip%{?_isa}
%endif
Provides: %{?scl_prefix}php-zlib, %{?scl_prefix}php-zlib%{?_isa}
%{?scl:Requires: %{scl}-runtime}

%description common
The %{?scl_prefix}php-common package contains files used by both
the %{?scl_prefix}php package and the %{?scl_prefix}php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{?scl_prefix}php-cli%{?_isa} = %{version}-%{release}, autoconf, automake
%if %{with_libpcre}
Requires: pcre-devel%{?_isa} >= 8.20
%endif

%description devel
The %{?scl_prefix}php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%if %{with_imap}
%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The %{?scl_prefix}php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The %{?scl_prefix}php-ldap package adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: %{?scl_prefix}php-pdo-abi = %{pdover}%{isasuffix}
Provides: %{?scl_prefix}php(pdo-abi) = %{pdover}%{isasuffix}
%if %{with_sqlite3}
Provides: %{?scl_prefix}php-sqlite3, %{?scl_prefix}php-sqlite3%{?_isa}
%endif
Provides: %{?scl_prefix}php-pdo_sqlite, %{?scl_prefix}php-pdo_sqlite%{?_isa}

%description pdo
The %{?scl_prefix}php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
Provides: %{?scl_prefix}php-mysql = %{version}-%{release}
Provides: %{?scl_prefix}php-mysql%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-mysqli = %{version}-%{release}
Provides: %{?scl_prefix}php-mysqli%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-pdo_mysql, %{?scl_prefix}php-pdo_mysql%{?_isa}
Obsoletes: %{?scl_prefix}php-mysql < %{version}

%description mysqlnd
The %{?scl_prefix}php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
Provides: %{?scl_prefix}php-pdo_pgsql, %{?scl_prefix}php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The %{?scl_prefix}php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-posix, %{?scl_prefix}php-posix%{?_isa}
Provides: %{?scl_prefix}php-sysvsem, %{?scl_prefix}php-sysvsem%{?_isa}
Provides: %{?scl_prefix}php-sysvshm, %{?scl_prefix}php-sysvshm%{?_isa}
Provides: %{?scl_prefix}php-sysvmsg, %{?scl_prefix}php-sysvmsg%{?_isa}

%description process
The %{?scl_prefix}php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
Provides: %{?scl_prefix}php-pdo_odbc, %{?scl_prefix}php-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel

%description odbc
The %{?scl_prefix}php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel

%description soap
The %{?scl_prefix}php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_interbase}
%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires:  firebird-devel
Requires: %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
Provides: %{?scl_prefix}php-firebird, %{?scl_prefix}php-firebird%{?_isa}
Provides: %{?scl_prefix}php-pdo_firebird, %{?scl_prefix}php-pdo_firebird%{?_isa}

%description interbase
The %{?scl_prefix}php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%if %{with_oci8}
%package oci8
Summary:        A module for PHP applications that use OCI8 databases
Group:          Development/Languages
# All files licensed under PHP version 3.01
License:        PHP
BuildRequires:  oracle-instantclient-basic <  %{oraclemax}
BuildRequires:  oracle-instantclient-basic >= %{oraclever}
BuildRequires:  oracle-instantclient-devel <  %{oraclemax}
BuildRequires:  oracle-instantclient-devel >= %{oraclever}
Requires:       %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
Provides:       %{?scl_prefix}php_database
Provides:       %{?scl_prefix}php-pdo_oci, %{?scl_prefix}php-pdo_oci%{?_isa}
Obsoletes:      %{?scl_prefix}php-pecl-oci8 <  %{oci8ver}
Conflicts:      %{?scl_prefix}php-pecl-oci8 >= %{oci8ver}
Provides:       %{?scl_prefix}php-pecl(oci8) = %{oci8ver}, %{?scl_prefix}php-pecl(oci8)%{?_isa} = %{oci8ver}
# Should requires libclntsh.so.12.1, but it's not provided by Oracle RPM.
AutoReq:        0

%description oci8
The %{?scl_prefix}php-oci8 packages provides the OCI8 extension version %{oci8ver}
and the PDO driver to access Oracle Database.

The extension is linked with Oracle client libraries %{oraclever}
(Oracle Instant Client).  For details, see Oracle's note
"Oracle Client / Server Interoperability Support" (ID 207303.1).

You must install libclntsh.so.%{oraclever} to use this package, provided
in the database installation, or in the free Oracle Instant Client
available from Oracle.

Notice:
- %{?scl_prefix}php-oci8 provides oci8 and pdo_oci extensions from php sources.
- %{?scl_prefix}php-pecl-oci8 only provides oci8 extension.

Documentation is at http://php.net/oci8 and http://php.net/pdo_oci
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The %{?scl_prefix}php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php-dom, %{?scl_prefix}php-dom%{?_isa}
Provides: %{?scl_prefix}php-domxml, %{?scl_prefix}php-domxml%{?_isa}
Provides: %{?scl_prefix}php-wddx, %{?scl_prefix}php-wddx%{?_isa}
Provides: %{?scl_prefix}php-xmlreader, %{?scl_prefix}php-xmlreader%{?_isa}
Provides: %{?scl_prefix}php-xmlwriter, %{?scl_prefix}php-xmlwriter%{?_isa}
Provides: %{?scl_prefix}php-xsl, %{?scl_prefix}php-xsl%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The %{?scl_prefix}php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}

%description xmlrpc
The %{?scl_prefix}php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}

%description mbstring
The %{?scl_prefix}php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libgd is licensed under BSD
License: PHP and BSD
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
BuildRequires: libXpm-devel
%if %{with_t1lib}
BuildRequires: t1lib-devel
%endif

%description gd
The %{?scl_prefix}php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}

%description bcmath
The %{?scl_prefix}php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}

%description dba
The %{?scl_prefix}php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%if %{with_mcrypt}
%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The %{?scl_prefix}php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.
%endif

%if %{with_tidy}
%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The %{?scl_prefix}php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.
%endif

%if %{with_freetds}
%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: %{?scl_prefix}php-pdo_dblib, %{?scl_prefix}php-pdo_dblib%{?_isa}
Provides: %{?scl_prefix}php-sybase_ct, %{?scl_prefix}php-sybase_ct%{?_isa}

%description mssql
The %{?scl_prefix}php-mssql package contains a dynamic shared object that will
add MSSQL and Sybase database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.
%endif

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The %{?scl_prefix}php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%if %{with_recode}
%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The %{?scl_prefix}php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.
%endif

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
# Upstream requires 3.6, we require 50 to ensure use of libicu-last
BuildRequires: libicu-devel >= 50

%description intl
The %{?scl_prefix}php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%if %{with_enchant}
%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License: PHP
Group: System Environment/Libraries
Requires: %{?scl_prefix}php-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The %{?scl_prefix}php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif


%prep
: Building %{name}-%{version}-%{release} with systemd=%{with_systemd} imap=%{with_imap} interbase=%{with_interbase} mcrypt=%{with_mcrypt} freetds=%{with_freetds} sqlite3=%{with_sqlite3} tidy=%{with_tidy} zip=%{with_zip}

%setup -q -n php-%{version}%{?rcver}

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch21 -p1 -b .odbctimer

%patch40 -p1 -b .dlopen
%patch41 -p1 -b .easter
%patch42 -p1 -b .systzdata
%patch43 -p1 -b .headers
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .iniscan
%patch49 -p1 -b .curltls

%patch91 -p1 -b .remi-oci8

# upstream patches
%patch100 -p1 -b .bug65641
%patch101 -p1 -b .bug65635
%patch102 -p1 -b .bug50444

# security patches
%patch200 -p1 -b .bug69720
%patch201 -p1 -b .bug70433
%patch202 -p1 -b .bug70755
%patch203 -p1 -b .bug70728
%patch204 -p1 -b .bug70741
%patch205 -p1 -b .bug70661
%patch206 -p1 -b .bug71354
%patch207 -p1 -b .bug71335
%patch208 -p1 -b .bug71391
%patch209 -p1 -b .bug71323
%patch210 -p1 -b .bug71459
%patch211 -p1 -b .bug71039
%patch212 -p1 -b .bug71488
%patch213 -p1 -b .pcre838
%patch214 -p1 -b .bug71498
%patch215 -p1 -b .bug71587
%patch216 -p1 -b .bug71860
%patch217 -p1 -b .bug71906
%patch218 -p1 -b .bug71798
%patch219 -p1 -b .bug71704
%patch220 -p1 -b .bug71527
%patch221 -p1 -b .bug64938
%patch222 -p1 -b .bug71912
%patch223 -p1 -b .bug72061
%patch224 -p1 -b .bug72093
%patch225 -p1 -b .bug72094
%patch226 -p1 -b .bug72099
%patch227 -p1 -b .bug71331
%patch228 -p1 -b .bug72114
%patch229 -p1 -b .bugoverflow
%patch230 -p1 -b .bug72135
%patch231 -p1 -b .bug72241
%patch232 -p1 -b .bug66387
%patch233 -p1 -b .bug72340
%patch234 -p1 -b .bug72275
%patch235 -p1 -b .bug72400
%patch236 -p1 -b .bug72339
%patch237 -p1 -b .bug72298
%patch238 -p1 -b .bug72402
%patch239 -p1 -b .bug72433
%patch240 -p1 -b .bug72434
%patch241 -p1 -b .bug72455
%patch242 -p1 -b .bug72446
%patch243 -p1 -b .bug70480
%patch244 -p1 -b .bug69975
%patch245 -p1 -b .bug72479
%patch246 -p1 -b .bug72573
%patch247 -p1 -b .bug72513
%patch248 -p1 -b .bug72520
%patch249 -p1 -b .bug72533
%patch250 -p1 -b .bug72562
%patch251 -p1 -b .bug72603
%patch252 -p1 -b .bug72606
%patch253 -p1 -b .bug72613
%patch254 -p1 -b .bug72618
%patch255 -p1 -b .bug72519
%patch256 -p1 -b .bug72735
%patch257 -p1 -b .bug72627
%patch258 -p1 -b .bug72926
%patch259 -p1 -b .bug73035
%patch260 -p1 -b .bug72928
%patch261 -p1 -b .bug73737
%patch262 -p1 -b .bug73764
%patch263 -p1 -b .bug73768
%patch264 -p1 -b .bug73773
%patch265 -p1 -b .bug73549
%patch266 -p1 -b .bug73868
%patch267 -p1 -b .bug73869
%patch268 -p1 -b .bug74435
%patch269 -p1 -b .bug75571
%patch270 -p1 -b .bug75981
%patch271 -p1 -b .bug76582
%patch272 -p1 -b .bug77153
%patch273 -p1 -b .bug77020
%patch274 -p1 -b .bug77231
%patch275 -p1 -b .bug77242
%patch276 -p1 -b .bug77380
%patch277 -p1 -b .bug78599
%patch278 -p1 -b .bug81719
: ------------------------
#exit 1

# Fixes for tests
%patch300 -p1 -b .datetests1
%patch301 -p1 -b .datetests2
%if %{with_libpcre}
%if 0%{?fedora} < 21
# Only apply when system libpcre < 8.34
%patch302 -p1 -b .pcre834
%endif
%endif

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir \
    build-fpm \
    build-apache \
    build-embedded \
    build-cgi

# ----- Manage known as failed test -------
# php_egg_logo_guid() removed by patch41
rm -f tests/basic/php_egg_logo_guid.phpt
# affected by systzdata patch
rm -f ext/date/tests/timezone_location_get.phpt
# fails sometime
rm -f ext/sockets/tests/mcast_ipv?_recv.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_OCI8_VERSION /{s/.* "//;s/".*$//;p}' ext/oci8/php_oci8.h)
if test "$ver" != "%{oci8ver}"; then
   : Error: Upstream OCI8 version is now ${ver}, expecting %{oci8ver}.
   : Update the oci8ver macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# Create the macros.php files
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
 -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
 -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
 -e "s/@PHP_VERSION@/%{version}/" \
 -e "s:@LIBDIR@:%{_libdir}:" \
 -e "s:@ETCDIR@:%{_sysconfdir}:" \
 -e "s:@INCDIR@:%{_includedir}:" \
 -e "s:@BINDIR@:%{_bindir}:" \
 -e 's/@SCL@/%{?scl:%{scl}_}/' \
 %{SOURCE3} | tee macros.php
%if 0%{?fedora} >= 24
echo '%%%{?scl:%{scl}_}pecl_xmldir  %{_localstatedir}/lib/php/peclxml' | tee -a macros.php
%endif


%build
export PKG_CONFIG_PATH="/usr/local/openssl/lib/pkgconfig"
# aclocal workaround - to be improved
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-bz2 \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_root_prefix} \
    --with-png-dir=%{_root_prefix} \
    --with-xpm-dir=%{_root_prefix} \
    --enable-gd-native-ttf \
%if %{with_t1lib}
    --with-t1lib=%{_root_prefix} \
%endif
    --without-gdbm \
    --with-gettext \
    --with-iconv \
    --with-jpeg-dir=%{_root_prefix} \
    --with-openssl \
%if %{with_libpcre}
    --with-pcre-regex=%{_root_prefix} \
%endif
    --with-zlib \
    --with-layout=GNU \
    --enable-exif \
    --enable-ftp \
    --enable-sockets \
    --with-kerberos \
    --enable-shmop \
    --enable-calendar \
    --with-libxml-dir=%{_root_prefix} \
    --enable-xml \
    --with-system-tzdata \
    --with-mhash \
    $*
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
%if %{with_imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --with-gmp=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_root_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with_oci8}
      --with-oci8=shared,instantclient,%{_root_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever} \
      --with-pdo-oci=shared,instantclient,%{_root_prefix},%{oraclever} \
%endif
%if %{with_interbase}
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_root_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_root_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_root_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_root_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_root_prefix} \
      --with-pdo-sqlite=shared,%{_root_prefix} \
%if %{with_sqlite3}
      --with-sqlite3=shared,%{_root_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
%if %{with_mcrypt}
      --with-mcrypt=shared,%{_root_prefix} \
%endif
%if %{with_tidy}
      --with-tidy=shared,%{_root_prefix} \
%endif
%if %{with_freetds}
      --with-mssql=shared,%{_root_prefix} \
      --with-pdo-dblib=shared,%{_root_prefix} \
      --with-sybase-ct=shared,%{_root_prefix} \
%endif
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_root_prefix} \
      --enable-intl=shared \
      --with-icu-dir=%{_root_prefix} \
%if %{with_enchant}
      --with-enchant=shared,%{_root_prefix} \
%endif
%if %{with_recode}
      --with-recode=shared,%{_root_prefix} \
%endif
      --enable-fileinfo=shared
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemd}
      --with-fpm-systemd \
%endif
      --libdir=%{_libdir}/php \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd


# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd


%check
%if %runselftest
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysqlnd.so

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/%{name}.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}

# Apache config fragment
%if %{?scl:1}0
install -m 755 -d $RPM_BUILD_ROOT%{_root_httpd_moddir}
ln -s %{_httpd_moddir}/libphp5.so      $RPM_BUILD_ROOT%{_root_httpd_moddir}/lib%{name}5.so
%endif
sed -e 's/libphp5/lib%{name}5/' %{SOURCE9} >modconf

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4
install -D -m 644 modconf $RPM_BUILD_ROOT%{_httpd_confdir}/%{name}.conf
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/%{name}.conf
%else
# Dual config file with httpd >= 2.4
install -D -m 644 modconf    $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-%{name}.conf
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/%{name}.conf
%if %{with_httpd2410}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_confdir}/%{name}.conf
%endif
%endif

sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/%{name}.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache
%if 0%{?fedora} >= 24
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/peclxml
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl
%endif


# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -e 's:/etc:%{_sysconfdir}:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
# install systemd unit files and scripts for handling server startup
%if %{with_systemd}
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/%{?scl_prefix}php-fpm.service
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/etc/sysconfig:%{_sysconfdir}/sysconfig:' \
    -e 's:php-fpm.service:%{?scl_prefix}php-fpm.service:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i $RPM_BUILD_ROOT%{_unitdir}/%{?scl_prefix}php-fpm.service
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_root_sysconfdir}/systemd/system/%{?scl_prefix}php-fpm.service.d
%else
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_root_initddir}
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_root_initddir}/%{?scl_prefix}php-fpm
# Needed relocation for SCL
sed -e '/php-fpm.pid/s:/var:%{_localstatedir}:' \
    -e '/subsys/s/php-fpm/%{?scl_prefix}php-fpm/' \
    -e 's:/etc/sysconfig/php-fpm:%{_sysconfdir}/sysconfig/php-fpm:' \
    -e 's:/etc/php-fpm.conf:%{_sysconfdir}/php-fpm.conf:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i $RPM_BUILD_ROOT%{_root_initddir}/%{?scl_prefix}php-fpm
%endif

# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm

# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
sed -e 's:php-fpm.service:%{?scl_prefix}php-fpm.service:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm

# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# make the cli commands available in standard root for SCL build
%if 0%{?scl:1}
install -m 755 -d $RPM_BUILD_ROOT%{_root_bindir}
ln -s %{_bindir}/php       $RPM_BUILD_ROOT%{_root_bindir}/%{scl}
ln -s %{_bindir}/php-cgi   $RPM_BUILD_ROOT%{_root_bindir}/%{scl}-cgi
ln -s %{_bindir}/phar.phar $RPM_BUILD_ROOT%{_root_bindir}/%{scl_prefix}phar
%if %{with_lsws}
ln -s %{_bindir}/lsphp     $RPM_BUILD_ROOT%{_root_bindir}/ls%{scl}
%endif
%endif

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc \
%if %{with_imap}
    imap \
%endif
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    gmp \
    pdo pdo_pgsql pdo_odbc pdo_sqlite json \
%if %{with_sqlite3}
    sqlite3 \
%endif
%if %{with_oci8}
    oci8 pdo_oci \
%endif
%if %{with_interbase}
    interbase pdo_firebird \
%endif
%if %{with_enchant}
    enchant \
%endif
    phar fileinfo intl \
%if %{with_mcrypt}
    mcrypt \
%endif
%if %{with_tidy}
    tidy \
%endif
%if %{with_freetds}
    pdo_dblib mssql sybase_ct \
%endif
%if %{with_recode}
    recode \
%endif
%if %{with_zip}
    zip \
%endif
    pspell curl wddx \
    posix sysvshm sysvsem sysvmsg; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
%if %{with_freetds}
cat files.pdo_dblib >> files.mssql
cat files.sybase_ct >> files.mssql
%endif
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_oci8}
cat files.pdo_oci >> files.oci8
%endif
%if %{with_interbase}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if %{with_sqlite3}
cat files.sqlite3 >> files.pdo
%endif

# Package json, zip, curl, phar and fileinfo in -common.
cat files.json files.curl files.phar files.fileinfo files.gmp > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# Install the macros file:
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros.%{name}

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.*

%if ! %{with_httpd2410}
%pre fpm
# Add the "apache" user (to avoid pulling httpd in our dep)
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0
%endif

%post fpm
%if 0%{?systemd_post:1}
%systemd_post %{?scl:%{scl}-}php-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add %{?scl_prefix}php-fpm
%endif
fi
%endif

%preun fpm
%if 0%{?systemd_preun:1}
%systemd_preun %{?scl:%{scl}-}php-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable %{?scl_prefix}php-fpm.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{?scl_prefix}php-fpm.service >/dev/null 2>&1 || :
%else
    /sbin/service %{?scl_prefix}php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del %{?scl_prefix}php-fpm
%endif
fi
%endif

%postun fpm
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart %{?scl:%{scl}-}php-fpm.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{?scl_prefix}php-fpm.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ]; then
    /sbin/service %{?scl_prefix}php-fpm condrestart >/dev/null 2>&1 || :
fi
%endif
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- %{?scl_prefix}php-fpm
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/%{?scl_prefix}php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save %{?scl_prefix}php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del %{?scl_prefix}php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart %{?scl_prefix}php-fpm.service >/dev/null 2>&1 || :
fi
%endif

%posttrans common
cat << EOF
=====================================================================

 WARNING : PHP 5.4 have reached its "End of Life" in September 2015.
 Even, if this package includes some of the important security fix,
 backported from 5.5 or 5.6,
 The UPGRADE to a maintained version is very strongly RECOMMENDED.

%if %{?fedora}%{!?fedora:99} < 28
 WARNING : Fedora %{fedora} is now EOL :
 You should consider upgrading to a supported release
%endif
=====================================================================
EOF


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root)
%{_httpd_moddir}/libphp5.so
%if 0%{?scl:1}
%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_root_httpd_moddir}/lib%{name}5.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%config(noreplace) %{_httpd_confdir}/%{name}.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-%{name}.conf
%endif
%{_httpd_contentdir}/icons/%{name}.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%license LICENSE ZEND_LICENSE TSRM_LICENSE regex_COPYRIGHT
%license libmagic_LICENSE
%license phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_localstatedir}/lib/php
%dir %{_datadir}/php
%if 0%{?fedora} >= 24
%dir %{_localstatedir}/lib/php/peclxml
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%endif

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%doc sapi/cgi/README* sapi/cli/README
%if 0%{?scl:1}
%{_root_bindir}/%{scl}
%{_root_bindir}/%{scl}-cgi
%{_root_bindir}/%{scl_prefix}phar
%endif

%files fpm
%defattr(-,root,root)
%doc php-fpm.conf.default
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/%{name}.conf
%endif
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%if %{with_systemd}
%{_unitdir}/%{?scl_prefix}php-fpm.service
%dir %{_root_sysconfdir}/systemd/system/%{?scl_prefix}php-fpm.service.d
%else
%{_root_initddir}/%{?scl_prefix}php-fpm
%endif
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html


%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{embed_version}.so

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1*
%{macrosdir}/macros.%{name}

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%if %{with_imap}
%files imap -f files.imap
%endif
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%defattr(-,root,root,-)
%license libmbfl_LICENSE
%license oniguruma_COPYING
%license ucgendat_LICENSE
%files gd -f files.gd
%defattr(-,root,root,-)
%license libgd_README
%license libgd_COPYING
%files soap -f files.soap
%files bcmath -f files.bcmath
%defattr(-,root,root,-)
%license libbcmath_COPYING
%files dba -f files.dba
%files pdo -f files.pdo
%if %{with_mcrypt}
%files mcrypt -f files.mcrypt
%endif
%if %{with_tidy}
%files tidy -f files.tidy
%endif
%if %{with_freetds}
%files mssql -f files.mssql
%endif
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%if %{with_recode}
%files recode -f files.recode
%endif
%if %{with_interbase}
%files interbase -f files.interbase
%endif
%if %{with_enchant}
%files enchant -f files.enchant
%endif
%files mysqlnd -f files.mysqlnd
%if %{with_oci8}
%files oci8 -f files.oci8
%endif


%changelog
* Thu Jun 23 2022 Remi Collet <remi@remirepo.net> - 5.4.45-19
- myqlnd: fix #81719: mysqlnd/pdo password buffer overflow. CVE-2022-31626

* Tue Oct 22 2019 Remi Collet <remi@remirepo.net> - 5.4.45-18
- FPM:
  Fix CVE-2019-11043 env_path_info underflow in fpm_main.c

* Fri Jan 11 2019 Remi Collet <remi@remirepo.net> - 5.4.45-17
- Fix #77242 heap out of bounds read in xmlrpc_decode
- Fix #77380 Global out of bounds read in xmlrpc base64 code

* Mon Dec 10 2018 Remi Collet <remi@remirepo.net> - 5.4.45-16
- Fix #77231 Segfault when using convert.quoted-printable-encode filter
- Fix #77020 null pointer dereference in imap_mail
  CVE-2018-19935
- Fix #77153 imap_open allows to run arbitrary shell commands via
  mailbox parameter
  CVE-2018-19158

* Fri Sep 14 2018 Remi Collet <remi@remirepo.net> - 5.4.45-15
- fix #76582: XSS due to the header Transfer-Encoding: chunked
  CVE-2018-17082

* Thu Mar  1 2018 Remi Collet <remi@remirepo.net> - 5.4.45-14
- fix #73549: Use after free when stream is passed to imagepng
- fix #73868: Fix DOS vulnerability in gdImageCreateFromGd2Ctx()
  CVE-2016-10167
- fix #73869: Signed Integer Overflow gd_io.c
  CVE-2016-10168
- fix #74435: Buffer over-read into uninitialized memory
  CVE-2017-7890
- fix #75571: Potential infinite loop in gdImageCreateFromGifCtx
  CVE-2018-5711
- fix #75981: stack-buffer-overflow while parsing HTTP response

* Sat Feb 18 2017 Remi Collet <remi@remirepo.net> - 5.4.45-13
- fix #73737: FPE when parsing a tag format
  CVE-2016-10158
- fix #73764: int overflows in phar
  CVE-2016-10159
- fix #73768: Memory corruption when loading hostile phar
  CVE-2016-10160

* Mon Sep 19 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-12
- fix #72627: Memory Leakage In exif_process_IFD_in_TIFF
  CVE-2016-7128
- fix #72926: Uninitialized Thumbail Data Leads To Memory Leakage
  in exif_process_IFD_in_TIFF
- fix #73035: Out of bound when verify signature of tar phar
- fix #72928: Out of bound when verify signature of zip phar
  CVE-2016-7414
- fix #72735 regression in exif maker note parser

* Fri Jul 22 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-11
- Fix #70480: php_url_parse_ex() buffer overflow read
  CVE-2016-6288
- Fix #69975: PHP segfaults when accessing nvarchar(max) defined columns
- Fix #72479: Use After Free Vulnerability in SNMP with GC and unserialize()
  CVE-2016-6295
- Fix #72573: HTTP_PROXY is improperly trusted by some PHP libraries
  CVE-2016-5385
- Fix #72513: buffer overflow vulnerability in virtual_file_ex
  CVE-2016-6289
- Fix #72520: buffer overflow vulnerability in php_stream_zip_opener
  CVE-2016-6297
- Fix #72533: locale_accept_from_http out-of-bounds access
  CVE-2016-6294
- Fix #72562: Use After Free in unserialize() with Unexpected Session
  Deserialization CVE-2016-6290
- Fix #72603: Out of bound read in exif_process_IFD_in_MAKERNOTE
  CVE-2016-6291
- Fix #72606: heap-buffer-overflow (write) simplestring_addn simplestring.c
  CVE-2016-6296
- Partial fix #72613: do not treat negative returns from bz2 as size_t
- Fix #72618: NULL Pointer Dereference in exif_process_user_comment
  CVE-2016-6292
- Fix #72519: possible OOB using imagegif

* Thu Jun 30 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-10.1
- own tests/doc directories for pecl packages (f24)

* Tue Jun 21 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-10
- Fix #66387: Stack overflow with imagefilltoborder
- Fix #72340: Double Free Courruption in wddx_deserialize
  CVE-2016-5772
- Fix #72275: don't allow smart_str to overflow int
- Fix #72400: prevent signed int overflows for string lengths
- Fix #72403: prevent signed int overflows for string lengths
- Fix #72268: Integer Overflow in nl2br(). (Stas)
- Fix #72339: Integer Overflow in _gd2GetHeader() resulting in heap overflow
  CVE-2016-5766
- Fix #72298: pass2_no_dither out-of-bounds access
- Fix #72402: _php_mb_regex_ereg_replace_exec - double free
  CVE-2016-5768
- Fix #72433: SPL use After Free Vulnerability in PHP's GC
  CVE-2016-5771
- Fix #72434: ZipArchive class use After Free Vulnerability in PHP's GC
  CVE-2016-5773
- Fix #72455: Heap Overflow due to integer overflows
  CVE-2016-5769
- Fix #72446: Integer Overflow in gdImagePaletteToTrueColor()
  CVE-2016-5767

* Sun May 29 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-9
- Fix #71331: Uninitialized pointer in phar_make_dirstream
  CVE-2016-4343
- Fix #72114: int/size_t confusion in fread
  CVE-2016-5096
- Add check for string overflow to all string add operations
- Fix #72135: don't create strings with lengths outside int range
  CVE-2016-5094
- Fix #72241: get_icu_value_internal out-of-bounds read
  CVE-2016-5093

* Tue Apr 26 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-8
- Fix #64938: libxml_disable_entity_loader setting is shared between threads
  CVE-2015-8866
- Fix #71912: libgd signedness vulnerability
  CVE-2016-3074
- Fix #72061: Out-of-bounds reads in zif_grapheme_stripos with negative offset
  CVE-2016-4540 CVE-2016-4541
- Fix #72093: bcpowmod accepts negative scale and corrupts _one_ definition
  CVE-2016-4537 CVE-2016-4538
- Fix #72094: Out of bounds heap read access in exif header processing
  CVE-2016-4542 CVE-2016-4543 CVE-2016-4544
- Fix #72099: xml_parse_into_struct segmentation fault
  CVE-2016-4539

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-7
- Fix #71860: Require valid paths for phar filenames
  CVE-2016-4072
- Fix #71906: AddressSanitizer: negative-size-param in mbfl_strcut
  CVE-2016-4073
- Fix #71798: Integer Overflow in php_raw_url_encode
  CVE-2016-4070
- Fix #71704: php_snmp_error() Format String Vulnerability
  CVE-2016-4071
- Fix #71527: Buffer over-write in finfo_open with malformed magic file
  CVE-2015-8865

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-6
- adapt for F24: define %%pecl_xmldir and own it

* Wed Mar  2 2016 Remi Collet <remi@remirepo.net> 5.4.45-5
- Fix #71498: Out-of-Bound Read in phar_parse_zipfile()
- Fix #71587: Use-After-Free / Double-Free in WDDX Deserialize

* Tue Feb 16 2016 Remi Collet <remi@remirepo.net> 5.4.45-4
- Fix #71354: phar, remove UMR when size is 0
  CVE-2016-4342
- Fix #71335: type confusion in WDDX packet deserialization
- Fix #71391: NULL pointer dereference in phar_tar_setupmetadata()
- Fix #71323: output of stream_get_meta_data can be falsified by its input
- Fix #71459: integer overflow in iptcembed()
- Fix #71039: exec functions ignore length but look for NULL termination
- Fix #71720: heap bufferover flow in escapeshell functions
- Fix #71488: Stack overflow when decompressing tar archives
  CVE-2016-2554
- upgrade bundled PCRE to 8.38

* Wed Jan  6 2016 Remi Collet <remi@fedoraproject.org> 5.4.45-3
- Fix #70755: fpm_log.c memory leak and buffer overflow
- Fix #70728: Type Confusion Vulnerability in PHP_to_XMLRPC_worker
- Fix #70741: Session WDDX Packet Deserialization Type
- Fix #70661: Use After Free Vulnerability in WDDX Packet Deserialization
- curl: add CURL_SSLVERSION_TLSv1_x constants

* Wed Sep 30 2015 Remi Collet <remi@fedoraproject.org> 5.4.45-2
- Fix bug #70433 - Uninitialized pointer in phar_make_dirstream
  when zip entry filename is "/" CVE-2015-7804
- Fix bug #69720: Null pointer dereference in phar_get_fp_offset()
  CVE-2015-7803

* Wed Sep  2 2015 Remi Collet <remi@fedoraproject.org> 5.4.45-1
- Update to 5.4.45
  http://www.php.net/releases/5_4_45.php

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> 5.4.44-1
- Update to 5.4.44
  http://www.php.net/releases/5_4_44.php

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> 5.4.43-1
- Update to 5.4.43
  http://www.php.net/releases/5_4_43.php

* Wed Jun 10 2015 Remi Collet <remi@fedoraproject.org> 5.4.42-1
- Update to 5.4.42
  http://www.php.net/releases/5_4_42.php

* Thu May 14 2015 Remi Collet <remi@fedoraproject.org> 5.4.41-1
- Update to 5.4.41
  http://www.php.net/releases/5_4_41.php

* Wed Apr 15 2015 Remi Collet <remi@fedoraproject.org> 5.4.40-1
- Update to 5.4.40
  http://www.php.net/releases/5_4_40.php

* Thu Apr  9 2015 Remi Collet <remi@fedoraproject.org> 5.4.39-2
- add patch from 5.5.14 for https://bugs.php.net/50444

* Thu Mar 19 2015 Remi Collet <remi@fedoraproject.org> 5.4.39-1
- Update to 5.4.39
  http://www.php.net/releases/5_4_39.php

* Sat Feb 28 2015 Remi Collet <remi@fedoraproject.org> 5.4.38-2
- fix fedora 22 build with recent systemd
  add patch fix from https://bugs.php.net/67635

* Wed Feb 18 2015 Remi Collet <remi@fedoraproject.org> 5.4.38-1
- Update to 5.4.38
  http://www.php.net/releases/5_4_38.php

* Wed Jan 21 2015 Remi Collet <rcollet@redhat.com> 5.4.37-1
- Update to 5.4.37
  http://www.php.net/releases/5_4_37.php

* Tue Jan 20 2015 Remi Collet <rcollet@redhat.com> 5.4.36-1.2
- fix php-fpm.service.d location

* Mon Dec 22 2014 Remi Collet <remi@fedoraproject.org> 5.4.36-1.1
- allow multiple paths in ini_scan_dir, backported from 5.5
  and applied in RHSCL packages

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> 5.4.36-1
- Update to 5.4.36
  http://www.php.net/releases/5_4_36.php
- add embedded sub package
- filter all libraries to avoid provides
- add sybase_ct extension

* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> 5.4.35-1
- Update to 5.4.35
  http://www.php.net/releases/5_4_35.php

* Sun Nov  2 2014 Remi Collet <remi@fedoraproject.org> 5.4.34-2
- new version of systzdata patch, fix case sensitivity
- add php54-cgi command in base system
- gmp: fix memory management conflict with other libraries
  using libgmp, backport fix for https://bugs.php.net/63595

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> 5.4.34-1
- Update to 5.4.34
  http://www.php.net/releases/5_4_34.php
- build gmp as shared, so can be disabled by user

* Sat Sep 20 2014 Remi Collet <remi@fedoraproject.org> 5.4.33-2
- openssl: fix regression introduce in changes for upstream
  bug #65137 and #41631, revert to 5.4.32 behavior

* Wed Sep 17 2014 Remi Collet <remi@fedoraproject.org> 5.4.33-1
- Update to 5.4.33
  http://www.php.net/releases/5_4_33.php
- fpm: fix script_name with mod_proxy_fcgi / proxypass
  add upstream patch for https://bugs.php.net/65641

* Fri Sep  5 2014 Remi Collet <rcollet@redhat.com> - 5.4.33-0.1.RC1
- update to 5.4.33RC1
- add system libraries to default include_path

* Sun Aug 31 2014 Remi Collet <rcollet@redhat.com> - 5.4.32-1
- update to 5.4.32
- cleanup, merge with spec from remi repository
- enable most extensions

* Tue Feb  4 2014 Remi Collet <rcollet@redhat.com> - 5.4.16-16
- allow multiple paths in ini_scan_dir #1058162

* Fri Dec  6 2013 Remi Collet <rcollet@redhat.com> - 5.4.16-12
- add security fix for CVE-2013-6420

* Fri Sep 27 2013 Remi Collet <rcollet@redhat.com> 5.4.16-10
- disable mod_php for httpd24

* Tue Sep 17 2013 Remi Collet <rcollet@redhat.com> 5.4.16-8
- relocate RPM macro #1008483
- remove ZTS conditional stuf for ligibility
- add mod_php for httpd24 collection

* Mon Aug 19 2013 Remi Collet <rcollet@redhat.com> - 5.4.16-7
- fix enchant package summary and description
- add security fix for CVE-2013-4248

* Thu Jul 18 2013 Remi Collet <rcollet@redhat.com> 5.4.16-4
- improve mod_php, pgsql and ldap description
- add missing man pages (phar, php-cgi)
- add provides php(pdo-abi) for consistency with php(api) and php(zend-abi)
- use %%__isa_bits instead of %%__isa in ABI suffix #985350

* Fri Jul 12 2013 Remi Collet <rcollet@redhat.com> - 5.4.16-3
- add security fix for CVE-2013-4113
- add missing ASL 1.0 license

* Fri Jun  7 2013 Remi Collet <rcollet@redhat.com> 5.4.16-2
- run tests during build

* Fri Jun  7 2013 Remi Collet <rcollet@redhat.com> 5.4.16-1
- rebase to 5.4.16
- fix hang in FindTishriMolad(), #965144
- patch for upstream Bug #64915 error_log ignored when daemonize=0
- patch for upstream Bug #64949 Buffer overflow in _pdo_pgsql_error, #969103
- patch for upstream bug #64960 Segfault in gc_zval_possible_root

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 5.4.14-3
- remove wrappers in /usr/bin (#966407)

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.4.14-2
- rebuild for libjpeg (instead of libjpeg_turbo)
- fix unowned dir %%{_datadir}/fpm and %%{_libdir}/httpd (#956221)

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> 5.4.14-1
- update to 5.4.14
- clean old deprecated options

* Wed Mar 13 2013 Remi Collet <rcollet@redhat.com> 5.4.13-1
- update to 5.4.13
- security fixes for CVE-2013-1635 and CVE-2013-1643
- make php-mysql package optional (and disabled)
- make ZTS build optional (and disabled)
- always try to load mod_php (apache warning is usefull)
- Hardened build (links with -z now option)
- Remove %%config from /etc/rpm/macros.php

* Wed Jan 16 2013 Remi Collet <rcollet@redhat.com> 5.4.11-1
- update to 5.4.11
- fix php.conf to allow MultiViews managed by php scripts

* Wed Dec 19 2012 Remi Collet <rcollet@redhat.com> 5.4.10-1
- update to 5.4.10
- remove patches merged upstream
- drop "Configure Command" from phpinfo output
- prevent php_config.h changes across (otherwise identical)
  rebuilds


* Thu Nov 22 2012 Remi Collet <rcollet@redhat.com> 5.4.9-1
- update to 5.4.9

* Mon Nov 19 2012 Remi Collet <rcollet@redhat.com> 5.4.8-7
- fix php.conf

* Mon Nov 19 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- filter private shared in _httpd_modir
- improve system libzip patch to use pkg-config
- use _httpd_contentdir macro and fix php.gif path
- switch back to upstream generated scanner/parser
- use system pcre only when recent enough

* Fri Nov 16 2012 Remi Collet <rcollet@redhat.com> 5.4.8-5
- improves php.conf, no need to be relocated

* Fri Nov  9 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- clarify Licenses
- missing provides xmlreader and xmlwriter
- change php embedded library soname version to 5.4

* Mon Nov  5 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix mysql_sock macro definition

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix standard build (non scl)

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- fix installed headers

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 5.4.8-2
- use libldap_r for ldap extension

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- add missing scl_prefix in some provides/requires

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 5.4.8-2.1
- make php-enchant optionnal, not available on RHEL-5
- make php-recode optionnal, not available on RHEL-5
- disable t1lib on RHEL-5

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 5.4.8-2
- enable tidy on RHEL-6 only
- re-enable unit tests

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 5.4.8-1.2
- minor macro fixes for RHEL-5 build
- update autotools workaround for RHEL-5
- use readline when libedit not available (RHEL-5)

* Mon Oct 22 2012 Remi Collet <rcollet@redhat.com> 5.4.8-1
- update to 5.4.8
- define both session.save_handler and session.save_path
- fix possible segfault in libxml (#828526)
- use SKIP_ONLINE_TEST during make test
- php-devel requires pcre-devel and php-cli (instead of php)
- provides php-phar
- update systzdata patch to v10, timezone are case insensitive

* Mon Oct 15 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- php-fpm: create apache user if needed
- php-cli: provides cli command in standard root (scl)

* Fri Oct 12 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- add configtest option to init script
- test configuration before service reload
- fix php-fpm service relocation
- fix php-fpm config relocation
- drop embdded subpackage for scl

* Wed Oct  3 2012 Remi Collet <rcollet@redhat.com> 5.4.7-2
- missing requires on scl-runtime
- relocate /var/lib/session
- fix php-devel requires
- rename, but don't relocate macros.php

* Tue Oct  2 2012 Remi Collet <rcollet@redhat.com> 5.4.7-1
- initial spec rewrite for scl build

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-10
- fix typo in systemd macro

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-9
- php-fpm: enable PrivateTmp
- php-fpm: new systemd macros (#850268)
- php-fpm: add upstream patch for startup issue (#846858)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 5.4.7-8
- systemd integration, https://bugs.php.net/63085
- no odbc call during timeout, https://bugs.php.net/63171
- check sqlite3_column_table_name, https://bugs.php.net/63149

* Mon Sep 24 2012 Remi Collet <rcollet@redhat.com> 5.4.7-7
- most failed tests explained (i386, x86_64)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-6
- fix for http://bugs.php.net/63126 (#783967)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-5
- patch to ensure we use latest libdb (not libdb4)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- really fix rhel tests (use libzip and libdb)

* Tue Sep 18 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- fix test to enable zip extension on RHEL-7

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-2
- remove session.save_path from php.ini
  move it to apache and php-fpm configuration files

* Fri Sep 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-1
- update to 5.4.7
  http://www.php.net/releases/5_4_7.php
- php-fpm: don't daemonize

* Mon Aug 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-2
- enable php-fpm on secondary arch (#849490)

* Fri Aug 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-1
- update to 5.4.6
- update to v9 of systzdata patch
- backport fix for new libxml

* Fri Jul 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.5-1
- update to 5.4.5

* Mon Jul 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-4
- also provide php(language)%%{_isa}
- define %%{php_version}

* Mon Jul 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-3
- drop BR for libevent (#835671)
- provide php(language) to allow version check

* Thu Jun 21 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-2
- add missing provides (core, ereg, filter, standard)

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.4-1
- update to 5.4.4 (CVE-2012-2143, CVE-2012-2386)
- use /usr/lib/tmpfiles.d instead of /etc/tmpfiles.d
- use /run/php-fpm instead of /var/run/php-fpm

* Wed May 09 2012 Remi Collet <remi@fedoraproject.org> 5.4.3-1
- update to 5.4.3 (CVE-2012-2311, CVE-2012-2329)

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> 5.4.2-1
- update to 5.4.2 (CVE-2012-1823)

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-1
- update to 5.4.1

* Wed Apr 25 2012 Joe Orton <jorton@redhat.com> - 5.4.0-6
- rebuild for new icu
- switch (conditionally) to libdb-devel

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-5
- fix Loadmodule with MPM event (use ZTS if not MPM worker)
- split conf.d/php.conf + conf.modules.d/10-php.conf with httpd 2.4

* Thu Mar 29 2012 Joe Orton <jorton@redhat.com> - 5.4.0-4
- rebuild for missing automatic provides (#807889)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-3
- really use _httpd_mmn

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-2
- rebuild against httpd 2.4
- use _httpd_mmn, _httpd_apxs macros

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1
- update to PHP 5.4.0 finale

* Sat Feb 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.4.RC8
- update to PHP 5.4.0RC8

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.3.RC7
- update to PHP 5.4.0RC7
- provides env file for php-fpm (#784770)
- add patch to use system libzip (thanks to spot)
- don't provide INSTALL file

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.2.RC6
- all binaries in /usr/bin with zts prefix

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-0.1.RC6
- update to PHP 5.4.0RC6
  https://fedoraproject.org/wiki/Features/Php54

* Sun Jan 08 2012 Remi Collet <remi@fedoraproject.org> 5.3.8-4.4
- fix systemd unit

* Mon Dec 12 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-4.3
- switch to systemd

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 5.3.8-4.2
- Rebuild for new libpng

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.3.8-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 5.3.8-3.1
- rebuild with new gmp

* Wed Sep 28 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-3
- revert is_a() to php <= 5.3.6 behavior (from upstream)
  with new option (allow_string) for new behavior

* Tue Sep 13 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-2
- add mysqlnd sub-package
- drop patch4, use --libdir to use /usr/lib*/php/build
- add patch to redirect mysql.sock (in mysqlnd)

* Tue Aug 23 2011 Remi Collet <remi@fedoraproject.org> 5.3.8-1
- update to 5.3.8
  http://www.php.net/ChangeLog-5.php#5.3.8

* Thu Aug 18 2011 Remi Collet <remi@fedoraproject.org> 5.3.7-1
- update to 5.3.7
  http://www.php.net/ChangeLog-5.php#5.3.7
- merge php-zts into php (#698084)

* Tue Jul 12 2011 Joe Orton <jorton@redhat.com> - 5.3.6-4
- rebuild for net-snmp SONAME bump

* Mon Apr  4 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-3
- enable mhash extension (emulated by hash extension)

* Wed Mar 23 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-2
- rebuild for new MySQL client library

* Thu Mar 17 2011 Remi Collet <Fedora@famillecollet.com> 5.3.6-1
- update to 5.3.6
  http://www.php.net/ChangeLog-5.php#5.3.6
- fix php-pdo arch specific requires

* Tue Mar 15 2011 Joe Orton <jorton@redhat.com> - 5.3.5-6
- disable zip extension per "No Bundled Libraries" policy (#551513)

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> 5.3.5-5
- rebuild for icu 4.6

* Mon Feb 28 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-4
- fix systemd-units requires

* Thu Feb 24 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-3
- add tmpfiles.d configuration for php-fpm
- add Arch specific requires/provides

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Remi Collet <Fedora@famillecollet.com> 5.3.5-1
- update to 5.3.5
  http://www.php.net/ChangeLog-5.php#5.3.5
- clean duplicate configure options

* Tue Dec 28 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-2
- rebuild against MySQL 5.5.8
- remove all RPM_SOURCE_DIR

* Sun Dec 12 2010 Remi Collet <rpms@famillecollet.com> 5.3.4-1.1
- security patch from upstream for #660517

* Sat Dec 11 2010 Remi Collet <Fedora@famillecollet.com> 5.3.4-1
- update to 5.3.4
  http://www.php.net/ChangeLog-5.php#5.3.4
- move phpize to php-cli (see #657812)

* Wed Dec  1 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-5
- ghost /var/run/php-fpm (see #656660)
- add filter_setup to not provides extensions as .so

* Mon Nov  1 2010 Joe Orton <jorton@redhat.com> - 5.3.3-4
- use mysql_config in libdir directly to avoid biarch build failures

* Fri Oct 29 2010 Joe Orton <jorton@redhat.com> - 5.3.3-3
- rebuild for new net-snmp

* Sun Oct 10 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-2
- add php-fpm sub-package

* Thu Jul 22 2010 Remi Collet <Fedora@famillecollet.com> 5.3.3-1
- PHP 5.3.3 released

* Fri Apr 30 2010 Remi Collet <Fedora@famillecollet.com> 5.3.2-3
- garbage collector upstream  patches (#580236)

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> 5.3.2-2
- rebuild for icu 4.4

* Sat Mar 06 2010 Remi Collet <Fedora@famillecollet.com> 5.3.2-1
- PHP 5.3.2 Released!
- remove mime_magic option (now provided by fileinfo, by emu)
- add patch for http://bugs.php.net/50578
- remove patch for libedit (upstream)
- add runselftest option to allow build without test suite

* Fri Nov 27 2009 Joe Orton <jorton@redhat.com> - 5.3.1-3
- update to v7 of systzdata patch

* Wed Nov 25 2009 Joe Orton <jorton@redhat.com> - 5.3.1-2
- fix build with autoconf 2.6x

* Fri Nov 20 2009 Remi Collet <Fedora@famillecollet.com> 5.3.1-1
- update to 5.3.1
- remove openssl patch (merged upstream)
- add provides for php-pecl-json
- add prod/devel php.ini in doc

* Tue Nov 17 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 5.3.0-7
- use libedit instead of readline to resolve licensing issues

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 5.3.0-6
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Joe Orton <jorton@redhat.com> 5.3.0-4
- rediff systzdata patch

* Thu Jul 16 2009 Joe Orton <jorton@redhat.com> 5.3.0-3
- update to v6 of systzdata patch; various fixes

* Tue Jul 14 2009 Joe Orton <jorton@redhat.com> 5.3.0-2
- update to v5 of systzdata patch; parses zone.tab and extracts
  timezone->{country-code,long/lat,comment} mapping table

* Sun Jul 12 2009 Remi Collet <Fedora@famillecollet.com> 5.3.0-1
- update to 5.3.0
- remove ncurses, dbase, mhash extensions
- add enchant, sqlite3, intl, phar, fileinfo extensions
- raise sqlite version to 3.6.0 (for sqlite3, build with --enable-load-extension)
- sync with upstream "production" php.ini

* Sun Jun 21 2009 Remi Collet <Fedora@famillecollet.com> 5.2.10-1
- update to 5.2.10
- add interbase sub-package

* Sat Feb 28 2009 Remi Collet <Fedora@FamilleCollet.com> - 5.2.9-1
- update to 5.2.9

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  5 2009 Joe Orton <jorton@redhat.com> 5.2.8-9
- add recode support, -recode subpackage (#106755)
- add -zts subpackage with ZTS-enabled build of httpd SAPI
- adjust php.conf to use -zts SAPI build for worker MPM

* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 5.2.8-8
- fix patch fuzz, renumber patches

* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 5.2.8-7
- drop obsolete configure args
- drop -odbc patch (#483690)

* Mon Jan 26 2009 Joe Orton <jorton@redhat.com> 5.2.8-5
- split out sysvshm, sysvsem, sysvmsg, posix into php-process

* Sun Jan 25 2009 Joe Orton <jorton@redhat.com> 5.2.8-4
- move wddx to php-xml, build curl shared in -common
- remove BR for expat-devel, bogus configure option

* Fri Jan 23 2009 Joe Orton <jorton@redhat.com> 5.2.8-3
- rebuild for new MySQL

* Sat Dec 13 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.8-2
- libtool 2 workaround for phpize (#476004)
- add missing php_embed.h (#457777)

* Tue Dec 09 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.8-1
- update to 5.2.8

* Sat Dec 06 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.7-1.1
- libtool 2 workaround

* Fri Dec 05 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.7-1
- update to 5.2.7
- enable pdo_dblib driver in php-mssql

* Mon Nov 24 2008 Joe Orton <jorton@redhat.com> 5.2.6-7
- tweak Summary, thanks to Richard Hughes

* Tue Nov  4 2008 Joe Orton <jorton@redhat.com> 5.2.6-6
- move gd_README to php-gd
- update to r4 of systzdata patch; introduces a default timezone
  name of "System/Localtime", which uses /etc/localtime (#469532)

* Sat Sep 13 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.6-5
- enable XPM support in php-gd
- Fix BR for php-gd

* Sun Jul 20 2008 Remi Collet <Fedora@FamilleCollet.com> 5.2.6-4
- enable T1lib support in php-gd

* Mon Jul 14 2008 Joe Orton <jorton@redhat.com> 5.2.6-3
- update to 5.2.6
- sync default php.ini with upstream
- drop extension_dir from default php.ini, rely on hard-coded
  default, to make php-common multilib-safe (#455091)
- update to r3 of systzdata patch

* Thu Apr 24 2008 Joe Orton <jorton@redhat.com> 5.2.5-7
- split pspell extension out into php-spell (#443857)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.2.5-6
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Joe Orton <jorton@redhat.com> 5.2.5-5
- ext/date: use system timezone database

* Fri Dec 28 2007 Joe Orton <jorton@redhat.com> 5.2.5-4
- rebuild for libc-client bump

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 5.2.5-3
- Rebuild for openssl bump

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 5.2.5-2
- update to 5.2.5

* Mon Oct 15 2007 Joe Orton <jorton@redhat.com> 5.2.4-3
- correct pcre BR version (#333021)
- restore metaphone fix (#205714)
- add READMEs to php-cli

* Sun Sep 16 2007 Joe Orton <jorton@redhat.com> 5.2.4-2
- update to 5.2.4

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 5.2.3-9
- rebuild for fixed APR

* Tue Aug 28 2007 Joe Orton <jorton@redhat.com> 5.2.3-8
- add ldconfig post/postun for -embedded (Hans de Goede)

* Fri Aug 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.2.3-7
- add php-embedded sub-package

* Fri Aug 10 2007 Joe Orton <jorton@redhat.com> 5.2.3-6
- fix build with new glibc
- fix License

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 5.2.3-5
- define php_extdir in macros.php

* Mon Jul  2 2007 Joe Orton <jorton@redhat.com> 5.2.3-4
- obsolete php-dbase

* Tue Jun 19 2007 Joe Orton <jorton@redhat.com> 5.2.3-3
- add mcrypt, mhash, tidy, mssql subpackages (Dmitry Butskoy)
- enable dbase extension and package in -common

* Fri Jun  8 2007 Joe Orton <jorton@redhat.com> 5.2.3-2
- update to 5.2.3 (thanks to Jeff Sheltren)

* Wed May  9 2007 Joe Orton <jorton@redhat.com> 5.2.2-4
- fix php-pdo *_arg_force_ref global symbol abuse (#216125)

* Tue May  8 2007 Joe Orton <jorton@redhat.com> 5.2.2-3
- rebuild against uw-imap-devel

* Fri May  4 2007 Joe Orton <jorton@redhat.com> 5.2.2-2
- update to 5.2.2
- synch changes from upstream recommended php.ini

* Thu Mar 29 2007 Joe Orton <jorton@redhat.com> 5.2.1-5
- enable SASL support in LDAP extension (#205772)

* Wed Mar 21 2007 Joe Orton <jorton@redhat.com> 5.2.1-4
- drop mime_magic extension (deprecated by php-pecl-Fileinfo)

* Mon Feb 19 2007 Joe Orton <jorton@redhat.com> 5.2.1-3
- fix regression in str_{i,}replace (from upstream)

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 5.2.1-2
- update to 5.2.1
- add Requires(pre) for httpd
- trim %%changelog to versions >= 5.0.0

* Thu Feb  8 2007 Joe Orton <jorton@redhat.com> 5.2.0-10
- bump default memory_limit to 32M (#220821)
- mark config files noreplace again (#174251)
- drop trailing dots from Summary fields
- use standard BuildRoot
- drop libtool15 patch (#226294)

* Tue Jan 30 2007 Joe Orton <jorton@redhat.com> 5.2.0-9
- add php(api), php(zend-abi) provides (#221302)
- package /usr/share/php and append to default include_path (#225434)

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 5.2.0-8
- fix filter.h installation path
- fix php-zend-abi version (Remi Collet, #212804)

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-7
- rebuild again

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-6
- rebuild for net-snmp soname bump

* Mon Nov 27 2006 Joe Orton <jorton@redhat.com> 5.2.0-5
- build json and zip shared, in -common (Remi Collet, #215966)
- obsolete php-json and php-pecl-zip
- build readline extension into /usr/bin/php* (#210585)
- change module subpackages to require php-common not php (#177821)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-4
- provide php-zend-abi (#212804)
- add /etc/rpm/macros.php exporting interface versions
- synch with upstream recommended php.ini

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-3
- update to 5.2.0 (#213837)
- php-xml provides php-domxml (#215656)
- fix php-pdo-abi provide (#214281)

* Tue Oct 31 2006 Joseph Orton <jorton@redhat.com> 5.1.6-4
- rebuild for curl soname bump
- add build fix for curl 7.16 API

* Wed Oct  4 2006 Joe Orton <jorton@redhat.com> 5.1.6-3
- from upstream: add safety checks against integer overflow in _ecalloc

* Tue Aug 29 2006 Joe Orton <jorton@redhat.com> 5.1.6-2
- update to 5.1.6 (security fixes)
- bump default memory_limit to 16M (#196802)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.1.4-8.1
- rebuild

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-8
- Provide php-posix (#194583)
- only provide php-pcntl from -cli subpackage
- add missing defattr's (thanks to Matthias Saou)

* Fri Jun  9 2006 Joe Orton <jorton@redhat.com> 5.1.4-7
- move Obsoletes for php-openssl to -common (#194501)
- Provide: php-cgi from -cli subpackage

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 5.1.4-6
- split out php-cli, php-common subpackages (#177821)
- add php-pdo-abi version export (#193202)

* Wed May 24 2006 Radek Vokal <rvokal@redhat.com> 5.1.4-5.1
- rebuilt for new libnetsnmp

* Thu May 18 2006 Joe Orton <jorton@redhat.com> 5.1.4-5
- provide mod_php (#187891)
- provide php-cli (#192196)
- use correct LDAP fix (#181518)
- define _GNU_SOURCE in php_config.h and leave it defined
- drop (circular) dependency on php-pear

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 5.1.4-3
- update to 5.1.4

* Wed May  3 2006 Joe Orton <jorton@redhat.com> 5.1.3-3
- update to 5.1.3

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 5.1.2-5
- provide php-api (#183227)
- add provides for all builtin modules (Tim Jackson, #173804)
- own %%{_libdir}/php/pear for PEAR packages (per #176733)
- add obsoletes to allow upgrade from FE4 PDO packages (#181863)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.3
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.1.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 5.1.2-4
- rebuild for new libc-client soname

* Mon Jan 16 2006 Joe Orton <jorton@redhat.com> 5.1.2-3
- only build xmlreader and xmlwriter shared (#177810)

* Fri Jan 13 2006 Joe Orton <jorton@redhat.com> 5.1.2-2
- update to 5.1.2

* Thu Jan  5 2006 Joe Orton <jorton@redhat.com> 5.1.1-8
- rebuild again

* Mon Jan  2 2006 Joe Orton <jorton@redhat.com> 5.1.1-7
- rebuild for new net-snmp

* Mon Dec 12 2005 Joe Orton <jorton@redhat.com> 5.1.1-6
- enable short_open_tag in default php.ini again (#175381)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Joe Orton <jorton@redhat.com> 5.1.1-5
- require net-snmp for php-snmp (#174800)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 5.1.1-4
- add /usr/share/pear back to hard-coded include_path (#174885)

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 5.1.1-3
- rebuild for httpd 2.2

* Mon Nov 28 2005 Joe Orton <jorton@redhat.com> 5.1.1-2
- update to 5.1.1
- remove pear subpackage
- enable pdo extensions (php-pdo subpackage)
- remove non-standard conditional module builds
- enable xmlreader extension

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 5.0.5-6
- rebuilt against new openssl

* Mon Nov  7 2005 Joe Orton <jorton@redhat.com> 5.0.5-5
- pear: update to XML_RPC 1.4.4, XML_Parser 1.2.7, Mail 1.1.9 (#172528)

* Tue Nov  1 2005 Joe Orton <jorton@redhat.com> 5.0.5-4
- rebuild for new libnetsnmp

* Wed Sep 14 2005 Joe Orton <jorton@redhat.com> 5.0.5-3
- update to 5.0.5
- add fix for upstream #34435
- devel: require autoconf, automake (#159283)
- pear: update to HTTP-1.3.6, Mail-1.1.8, Net_SMTP-1.2.7, XML_RPC-1.4.1
- fix imagettftext et al (upstream, #161001)

* Thu Jun 16 2005 Joe Orton <jorton@redhat.com> 5.0.4-11
- ldap: restore ldap_start_tls() function

* Fri May  6 2005 Joe Orton <jorton@redhat.com> 5.0.4-10
- disable RPATHs in shared extensions (#156974)

* Tue May  3 2005 Joe Orton <jorton@redhat.com> 5.0.4-9
- build simplexml_import_dom even with shared dom (#156434)
- prevent truncation of copied files to ~2Mb (#155916)
- install /usr/bin/php from CLI build alongside CGI
- enable sysvmsg extension (#142988)

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 5.0.4-8
- prevent build of builtin dba as well as shared extension

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-7
- split out dba and bcmath extensions into subpackages
- BuildRequire gcc-c++ to avoid AC_PROG_CXX{,CPP} failure (#155221)
- pear: update to DB-1.7.6
- enable FastCGI support in /usr/bin/php-cgi (#149596)

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-6
- build /usr/bin/php with the CLI SAPI, and add /usr/bin/php-cgi,
  built with the CGI SAPI (thanks to Edward Rudd, #137704)
- add php(1) man page for CLI
- fix more test cases to use -n when invoking php

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 5.0.4-5
- rebuild for new libpq soname

* Tue Apr 12 2005 Joe Orton <jorton@redhat.com> 5.0.4-4
- bundle from PEAR: HTTP, Mail, XML_Parser, Net_Socket, Net_SMTP
- snmp: disable MSHUTDOWN function to prevent error_log noise (#153988)
- mysqli: add fix for crash on x86_64 (Georg Richter, upstream #32282)

* Mon Apr 11 2005 Joe Orton <jorton@redhat.com> 5.0.4-3
- build shared objects as PIC (#154195)

* Mon Apr  4 2005 Joe Orton <jorton@redhat.com> 5.0.4-2
- fix PEAR installation and bundle PEAR DB-1.7.5 package

* Fri Apr  1 2005 Joe Orton <jorton@redhat.com> 5.0.4-1
- update to 5.0.4 (#153068)
- add .phps AddType to php.conf (#152973)
- better gcc4 fix for libxmlrpc

* Wed Mar 30 2005 Joe Orton <jorton@redhat.com> 5.0.3-5
- BuildRequire mysql-devel >= 4.1
- don't mark php.ini as noreplace to make upgrades work (#152171)
- fix subpackage descriptions (#152628)
- fix memset(,,0) in Zend (thanks to Dave Jones)
- fix various compiler warnings in Zend

* Thu Mar 24 2005 Joe Orton <jorton@redhat.com> 5.0.3-4
- package mysqli extension in php-mysql
- really enable pcntl (#142903)
- don't build with --enable-safe-mode (#148969)
- use "Instant Client" libraries for oci8 module (Kai Bolay, #149873)

* Fri Feb 18 2005 Joe Orton <jorton@redhat.com> 5.0.3-3
- fix build with GCC 4

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 5.0.3-2
- install the ext/gd headers (#145891)
- enable pcntl extension in /usr/bin/php (#142903)
- add libmbfl array arithmetic fix (dcb314@hotmail.com, #143795)
- add BuildRequire for recent pcre-devel (#147448)

* Wed Jan 12 2005 Joe Orton <jorton@redhat.com> 5.0.3-1
- update to 5.0.3 (thanks to Robert Scheck et al, #143101)
- enable xsl extension (#142174)
- package both the xsl and dom extensions in php-xml
- enable soap extension, shared (php-soap package) (#142901)
- add patches from upstream 5.0 branch:
 * Zend_strtod.c compile fixes
 * correct php_sprintf return value usage

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 5.0.2-8
- update for db4-4.3 (Robert Scheck, #140167)
- build against mysql-devel
- run tests in %%check

* Wed Nov 10 2004 Joe Orton <jorton@redhat.com> 5.0.2-7
- truncate changelog at 4.3.1-1
- merge from 4.3.x package:
 - enable mime_magic extension and Require: file (#130276)

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-6
- fix dom/sqlite enable/without confusion

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-5
- fix phpize installation for lib64 platforms
- add fix for segfault in variable parsing introduced in 5.0.2

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 5.0.2-4
- update to 5.0.2 (#127980)
- build against mysqlclient10-devel
- use new RTLD_DEEPBIND to load extension modules
- drop explicit requirement for elfutils-devel
- use AddHandler in default conf.d/php.conf (#135664)
- "fix" round() fudging for recent gcc on x86
- disable sqlite pending audit of warnings and subpackage split

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-4
- don't build dom extension into 2.0 SAPI

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-3
- ExclusiveArch: x86 ppc x86_64 for the moment

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 5.0.1-2
- fix default extension_dir and conf.d/php.conf

* Thu Sep  9 2004 Joe Orton <jorton@redhat.com> 5.0.1-1
- update to 5.0.1
- only build shared modules once
- put dom extension in php-dom subpackage again
- move extension modules into %%{_libdir}/php/modules
- don't use --with-regex=system, it's ignored for the apache* SAPIs

* Wed Aug 11 2004 Tom Callaway <tcallawa@redhat.com>
- Merge in some spec file changes from Jeff Stern (jastern@uci.edu)

* Mon Aug 09 2004 Tom Callaway <tcallawa@redhat.com>
- bump to 5.0.0
- add patch to prevent clobbering struct re_registers from regex.h
- remove domxml references, replaced with dom now built-in
- fix php.ini to refer to php5 not php4
