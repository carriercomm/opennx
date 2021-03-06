%define version 0.16
%define svnrev 724

# Build-time configuration
# use wxWidgets debug libs
%define with_debug %{?_with_debug: 1} %{?!_with_debug: 0}
# use wxWidgets static libs
%define with_staticwx %{?_with_staticwx: 1} %{?!_with_staticwx: 0}
# Enable USBIP support
%define with_usbip %{?_with_usbip: 1} %{?!_with_usbip: 0}
# Enable single session support
%define with_singlesession %{?_with_singlesession: 1} %{?!_with_singlesession: 0}
# Make recommended RPM dependencies mandatory
%define with_forceopt %{?_with_forceopt: 1} %{?!_with_forceopt: 0}

# Caution:
# Using --with fetchnx triggers downloading the latest
# tarballs from NoMachine. This does *not* work in common
# jailed build-environments (like Suse BuildService)
%define with_fetchnx %{?_with_fetchnx: 1} %{?!_with_fetchnx: 0}

##
## OS detection
##
%define is_rh %(test -n "`echo %{?dist}|grep rh`" && echo 1 || echo 0)
%define is_el %(test -n "`echo %{?dist}|grep el`" && echo 1 || echo 0)
%define is_fc 0%{?fedora}%{?fedora_version}
%define is_suse 0%{?suse_version}
%define is_sles 0%{?sles_version}
%define is_mdv 0%{?mdkversion}
%if %{is_rh}%{is_el}
%define ostag %{?dist}
%endif
%if %{is_mdv}
%if %{mdkversion} > 200000
%define ostag .mdv%(echo %{mdkversion}|sed -e 's/\\(....\\).*/\\1/')
%else
%define ostag .mdv%{mdkversion}
%endif
# Mandriva's cool underlink protection unfortunately breaks nxesd
%define _disable_ld_no_undefined 1
%endif
%if %{is_fc}
%define ostag %{?dist}
%endif

%if %{is_sles}
%if %{sles_version} > 999
%define ostag .SLE%(echo %{sles_version}|sed -e 's/\\(..\\)\\(.\\)./\\1.\\2/')
%else
%define ostag .SLE%(echo %{sles_version}|sed -e 's/\\(.\\)\\(.\\)./\\1.\\2/')
%endif
%else
%if %{is_suse}
%if %{suse_version} > 999
%define ostag .SuSE%(echo %{suse_version}|sed -e 's/\\(..\\)\\(.\\)./\\1.\\2/')
%else
%define ostag .SuSE%(echo %{suse_version}|sed -e 's/\\(.\\)\\(.\\)./\\1.\\2/')
%endif
%endif
%endif

%global _prefix /opt/%{name}

%ifarch x86_64
%if %{is_mdv}
%define lpfx  lib64
%else
%define lpfx  lib
%endif
%define nxlib %{_prefix}/lib64
%else
%define nxlib %{_prefix}/lib
%define lpfx  lib
%endif

%define nxdlurl http://www.nomachine.com/sources.php
%define nxpkgs nxcomp nxproxy
%define nxpkgsall nxcomp nxproxy nxssh

%define rel %{svnrev}%{ostag}

Summary: An OpenSource NX client
Name: opennx
Version: %{version}
Release: %{rel}
License: LGPL/GPL
Group: Applications/Internet
URL: http://sourceforge.net/projects/opennx
Source0: opennx-%{version}.tar.gz
%if !%{with_fetchnx}
Source100: nxcomp-3.3.0-4.tar.gz
Source102: nxssh-3.3.0-1.tar.gz
Source103: nxproxy-3.3.0-2.tar.gz
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Obsoletes: nxclient
Provides: nxclient

BuildRequires: libtool
BuildRequires: automake >= 1.10
BuildRequires: audiofile-devel
BuildRequires: libusb-devel
BuildRequires: gcc-c++
BuildRequires: zip
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: libcurl-devel

%if %{is_suse}
# Workaround for https://bugzilla.novell.com/show_bug.cgi?id=436992
BuildRequires: -post-build-checks
%if %{suse_version} >= 1140
BuildRequires: wxWidgets-wxcontainer-devel
%define _use_internal_dependency_generator 0
%define __find_requires %wx_requires
%else
BuildRequires: wxGTK-devel >= 2.8.0
%endif
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libpulse-devel
BuildRequires: libcurl-devel
%endif

%if %{is_mdv}
BuildRequires: %{lpfx}wxgtku2.8-devel >= 2.8.0
%if %{mdkversion} >= 201100
BuildRequires: %{lpfx}xmu-devel
%else
BuildRequires: %{lpfx}xmu6-devel
%endif
BuildRequires: x11-proto-devel
BuildRequires: x11-xtrans-devel
BuildRequires: libpulseaudio-devel
BuildRequires: libcurl-devel
%endif

%if %{is_fc}%{is_rh}%{is_el}
%if %{is_fc} > 10
BuildRequires: wxGTK-devel >= 2.8.0
BuildRequires: pulseaudio-libs-devel
%else
%if %{is_el}
BuildRequires: wxGTK-devel >= 2.8.0
BuildRequires: curl-devel
%else
BuildRequires: wxGTK2-devel >= 2.8.0
BuildRequires: pulseaudio-libs-devel
BuildRequires: libcurl-devel
%endif
%endif
BuildRequires: samba-common
BuildRequires: libXmu-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
%endif

%if %{with_fetchnx}
BuildRequires: wget
%endif

Requires(post): xdg-utils
Requires(preun): xdg-utils
%if %{with_forceopt}
# The following are actually *not*
# required but *recommended*
%if %{is_suse}
# SMB sharing
Requires: libsmbclient0
# Printer sharing
Requires: cups-libs
# Smartcard support
Requires: libopensc2
Requires: libusb-0_1-4
%else
# SMB sharing
Requires: samba-common
# Printer sharing
Requires: cups-libs
# Smartcard support
Requires: opensc
Requires: libusb
%endif
Requires: pulseaudio
%if %{with_usbip}
Requires: usbip2-nxclient
%endif
%endif

%description
opennx is an OSS replacement for Nomachine's NX client.

%prep
%if %{with_fetchnx}
%setup -q
perl getnxsrcpkg %{nxpkgsall}
for pkg in %{nxpkgsall} ; do
    tar xzf ${pkg}-*.tar.gz
done
ncver=`ls nxcomp-*.tar.gz|perl -ne 'printf("%02d%02d%02d%02d\n",$1,$2,$3,$4)if(/nxcomp-(\d+)\.(\d+)\.(\d+)-(\d+)\.tar.*/);'`
%else
%setup -q -a 100 -a 102 -a 103
ncver=`basename %{SOURCE100}|perl -ne 'printf("%02d%02d%02d%02d\n",$1,$2,$3,$4)if(/nxcomp-(\d+)\.(\d+)\.(\d+)-(\d+)\.tar.*/);'`
%endif

# Apply openssh askPIN patch (see https://bugzilla.mindrot.org/show_bug.cgi?id=608)
cd nxssh && patch -p1 < ../patches/openssh-scard-pin.patch
cd ../nxcomp
for p in ../patches/nxcomp-*.patch ; do
    bn=`basename $p`
    case $bn in
        nxcomp-gcc44.patch)
            test $ncver -lt 03040006 && patch -p1 < $p
            ;;
        nxcomp-visibility.patch)
            test $ncver -ge 03050000 && patch -p1 < $p
            ;;
        *)
            patch -p1 < $p
            ;;
    esac
done
rm -f configure.in
touch .run_autoreconf
cd ..
# Make nxssh load libopensc dynamically
patch -p0 < patches/nxssh-dynopensc.patch

%build
./configure --prefix=%{_prefix} \
%if %{with_staticwx}
    --enable-staticwx \
%else
    --disable-staticwx \
%endif
%if %{with_debug}
    --enable-debug \
%endif
%if %{with_singlesession}
    --enable-singlesession \
%endif
%if %{with_usbip}
    --enable-usbip
%endif
# keep this comment line!!

make
for pkg in %{nxpkgs} ; do
    cd $pkg
    test -f .run_autoreconf && autoreconf -f -i || :
	./configure --prefix=%{_prefix} && make
    test $pkg = nxcomp && make DESTDIR=`pwd` libdir=/ install
    cd ..
done
export PATH=`pwd`/opensc:$PATH
cd nxssh
%if %{is_el}
LIBS=-lresolv ./configure --prefix=%{_prefix} --with-opensc --enable-opensc-dynamic && make
%else
./configure --prefix=%{_prefix} --with-opensc --enable-opensc-dynamic && make
%endif
cd ..

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} prefix=/usr install-man
%{__install} -d -m 755 %{buildroot}%{nxlib}
%{__install} -m 755 nxcomp/libXcomp.so.*.*.* %{buildroot}%{nxlib}
%{__install} -m 755 nxssh/nxssh %{buildroot}%{_prefix}/bin
%{__install} -m 755 nxproxy/nxproxy %{buildroot}%{_prefix}/bin
/sbin/ldconfig -n %{buildroot}%{nxlib}
%{__install} -d -m 755 %{buildroot}/usr/bin
ln -s %{_prefix}/bin/opennx %{buildroot}/usr/bin/nxclient
%if %{with_usbip}
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/udev/rules.d
%{__install} -m 644 etc/*.rules %{buildroot}%{_sysconfdir}/udev/rules.d
%endif

%clean
%{__rm} -rf %{buildroot}

%triggerin -- opensc, libsmbclient, samba-common, libusb, libusb-0_1-4, cups-libs, pulseaudio-libs
# Create symlinks with plain .so extension under %{_prefix}/lib[64]
for lname in usb-0 opensc smbclient cups pulse ; do
    LPATH=`/sbin/ldconfig -p|awk '/lib'$lname'[\.-]/ {print $4}'|head -1`
    if test -n "$LPATH" ; then
        blname=`echo $lname|sed -e 's/[-0-9]//g'`
        ln -snf $LPATH %{nxlib}/lib$blname.so
    fi
done

%if %{with_usbip}
%pre
if [ $1 = 1 ] ; then
    /usr/sbin/groupadd -r opennx || :
fi
%endif

%postun
if [ $1 = 0 ] ; then
%if %{with_usbip}
    /usr/sbin/groupdel opennx || :
%endif
    rm -f /usr/NX || :
fi

%post
# Create symlink to /usr/NX for compatibility to original
rm -rf /usr/NX
ln -snf %{_prefix} /usr/NX
# Create symlinks with plain .so extension under %{_prefix}/lib[64]
for lname in usb-0 opensc smbclient cups pulse ; do
    LPATH=`/sbin/ldconfig -p|awk '/lib'$lname'[\.-]/ {print $4}'|head -1`
    if test -n "$LPATH" ; then
        blname=`echo $lname|sed -e 's/[-0-9]//g'`
        ln -snf $LPATH %{nxlib}/lib$blname.so
    fi
done

# Install icons
cd %{_prefix}/share/icons
SIZES="16 32 48 128 256"
ICINSTALL="xdg-icon-resource install --noupdate --novendor --mode system"
for sz in $SIZES ; do
    case $sz in
        scalable)
            subdir=$sz
            ext=svg
            ;;
        [0-9]*)
            subdir=${sz}x${sz}
            ext=png
            ;;
    esac
    for ctx in apps mimetypes ; do
        (
            cd $subdir/$ctx
            for f in *.$ext ; do
                $ICINSTALL --context $ctx --size $sz $f
            done
        )
    done
done
xdg-icon-resource forceupdate
# Install menu entries
cd %{_prefix}/share/applnk/xdg
xdg-desktop-menu install --mode system *.directory *.desktop

%preun
if [ $1 -gt 0 ] ; then
    exit 0
fi

rm -f %{nxlib}/libusb.so
rm -f %{nxlib}/libopensc.so
rm -f %{nxlib}/libsmbclient.so
rm -f %{nxlib}/libcups.so

# Uninstall menu entries
cd %{_prefix}/share/applnk/xdg
xdg-desktop-menu uninstall --mode system *.directory *.desktop
# Install icons
cd %{_prefix}/share/icons
SIZES="16 32 48 128 256"
ICREMOVE="xdg-icon-resource uninstall --noupdate --novendor --mode system"
for sz in $SIZES ; do
    case $sz in
        scalable)
            subdir=$sz
            ext=svg
            ;;
        [0-9]*)
            subdir=${sz}x${sz}
            ext=png
            ;;
    esac
    for ctx in apps mimetypes ; do
        (
            cd $subdir/$ctx
            for f in *.$ext ; do
                $ICREMOVE --context $ctx --size $sz `basename $f .$ext`
            done
        )
    done
done
xdg-icon-resource forceupdate

%files
%defattr(-, root, root, 0755)
%doc COPYING INSTALL ChangeLog
%_prefix
/usr/bin/nxclient
/usr/share/man/man1/*
%if %{with_usbip}
%{_sysconfdir}/udev
%endif

%changelog
* Sun Apr 19 2009 Fritz Elfert <fritz@fritz-elfert.de>
- Set prefix to /opt/lsb/%{name} for FHS compliance
* Wed Apr 15 2009 Michael Kromer <michael.kromer@millenux.com>
- Fixes for SuSE Plattform (openSuSE/SLES)
* Sun Jan  7 2007 Fritz Elfert <fritz@fritz-elfert.de>
- Initial package
