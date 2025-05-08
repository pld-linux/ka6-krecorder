#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		krecorder
Summary:	A convergent audio recording application for Plasma
Name:		ka6-%{kaname}
Version:	25.04.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	d7a420df5dd69bac815112985d66ab73
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A convergent audio recording application for Plasma.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DFREERDP_EXECUTABLE:PATH=/usr/bin/xfreerdp \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/krecorder
%{_desktopdir}/org.kde.krecorder.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.krecorder.svg
%{_datadir}/metainfo/org.kde.krecorder.appdata.xml
