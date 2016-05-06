Summary:	Create deltas between rpms
Summary(pl.UTF-8):	Generowanie różnic między pakietami rpm
Name:		deltarpm
Version:	3.6
Release:	4
License:	BSD
Group:		Base
Source0:	ftp://ftp.suse.com/pub/projects/deltarpm/%{name}-%{version}.tar.bz2
# Source0-md5:	2cc2690bd1088cfc3238c25e59aaaec1
Patch0:		%{name}-3.4-no-skip-doc.patch
Patch1:		%{name}-3.4-pld.patch
Patch2:		%{name}-rpm5.patch
Patch3:		python-install.patch
URL:		http://www.novell.com/products/linuxpackages/opensuse/deltarpm.html
BuildRequires:	bzip2-devel
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	rpm-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xz-devel
BuildRequires:	zlib-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A deltarpm contains the difference between an old and a new version of
a rpm, which makes it possible to recreate the new rpm from the
deltarpm and the old one. You don't have to have a copy of the old
rpm, deltarpms can also work with installed rpms.

%description -l pl.UTF-8
Deltarpm zawiera różnice pomiędzy starą i nową wersją pakietu RPM,
pozwalając na stworzenie nowej wersji na podstawie delty i starej
wersji. Nie jest konieczne posiadanie kopii starego pakietu RPM,
deltarpm obsługuje także już zainstalowane pakiety.

%package -n drpmsync
Summary:	Sync a file tree with deltarpms
Summary(pl.UTF-8):	Synchronizacja drzewa plików deltarpm
Group:		Base
Requires:	%{name} = %{version}-%{release}
Suggests:	deltaiso

%description -n drpmsync
This package contains a tool to sync a file tree with deltarpms.

%description -n drpmsync -l pl.UTF-8
Ten pakiet zawiera narzędzie do synchronizacji drzewa plików deltarpm.

%package -n deltaiso
Summary:	Create deltas between isos containing rpms
Summary(pl.UTF-8):	Tworzenie różnic między obrazami ISO zawierającymi pakiety RPM
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltaisos, a
difference between an old and a new iso containing rpms.

%description -n deltaiso -l pl.UTF-8
Ten pakiet zawiera narzędzia do tworzenia i wykorzystywania plików
deltaiso - różnic między starymi a nowymi obrazami ISO zawierającymi
pakiety RPM.

%package -n python-deltarpm
Summary:	Python bindings for deltarpm
Summary(pl.UTF-8):	Wiązania Pythona do deltarpm
Group:		Base
# does not require base package

%description -n python-deltarpm
This package contains Python bindings for deltarpm.

%description -n python-deltarpm -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona do deltarpm.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i -e 's/python3//' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/rpm" \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	prefix=%{_prefix} \
	zlibbundled='' \
	zlibldflags='-lz' \
	zlibcppflags=''

%{__make} python \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	prefix=%{_prefix} \
	zlibbundled='' \
	zlibldflags='-lz' \
	zlibcppflags=''

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.BSD README
%attr(755,root,root) %{_bindir}/applydeltarpm
%attr(755,root,root) %{_bindir}/combinedeltarpm
%attr(755,root,root) %{_bindir}/makedeltarpm
%attr(755,root,root) %{_bindir}/rpmdumpheader
%{_mandir}/man8/applydeltarpm.8*
%{_mandir}/man8/combinedeltarpm.8*
%{_mandir}/man8/makedeltarpm.8*

%files -n deltaiso
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/applydeltaiso
%attr(755,root,root) %{_bindir}/fragiso
%attr(755,root,root) %{_bindir}/makedeltaiso
%{_mandir}/man8/applydeltaiso.8*
%{_mandir}/man8/fragiso.8*
%{_mandir}/man8/makedeltaiso.8*

%files -n drpmsync
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/drpmsync
%{_mandir}/man8/drpmsync.8*

%files -n python-deltarpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_deltarpmmodule.so
%{py_sitedir}/deltarpm.py[co]
