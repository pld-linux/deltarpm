#
# Conditional build:
%bcond_with	python2	# CPython2 module
%bcond_without	python3	# CPython3 module
%bcond_with	rpm5	# build with rpm5
#
Summary:	Create deltas between rpms
Summary(pl.UTF-8):	Generowanie różnic między pakietami rpm
Name:		deltarpm
Version:	3.6.5
Release:	2
License:	BSD
Group:		Base
#Source0Download: https://github.com/rpm-software-management/deltarpm/tags
Source0:	https://github.com/rpm-software-management/deltarpm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d60921e36c8866cb5933e2002c1b3830
Patch0:		%{name}-3.4-no-skip-doc.patch
Patch1:		%{name}-3.4-pld.patch
Patch2:		%{name}-rpm5.patch
URL:		https://github.com/rpm-software-management/deltarpm
BuildRequires:	bzip2-devel
BuildRequires:	popt-devel
%{?with_python2:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.507
BuildRequires:	xz-devel
BuildRequires:	zlib-static
BuildRequires:	zstd-devel
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
Summary:	Python 2 bindings for deltarpm
Summary(pl.UTF-8):	Wiązania Pythona 2 do deltarpm
Group:		Libraries/Python
# does not require base package

%description -n python-deltarpm
This package contains Python 2 bindings for deltarpm.

%description -n python-deltarpm -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 2 do deltarpm.

%package -n python3-deltarpm
Summary:	Python 3 bindings for deltarpm
Summary(pl.UTF-8):	Wiązania Pythona 3 do deltarpm
Group:		Libraries/Python
# does not require base package

%description -n python3-deltarpm
This package contains Python 3 bindings for deltarpm.

%description -n python3-deltarpm -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 3 do deltarpm.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%{?with_rpm5:%patch2 -p1}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/rpm -D_GNU_SOURCE" \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	prefix=%{_prefix} \
	zlibbundled='' \
	zlibldflags='-lz' \
	zlibcppflags=''

%{__make} python \
	PYTHONS="%{?with_python2:python} %{?with_python3:python3}" \
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

%if %{with python2}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with python3}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

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

%if %{with python2}
%files -n python-deltarpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_deltarpmmodule.so
%{py_sitedir}/deltarpm.py[co]
%endif

%if %{with python3}
%files -n python3-deltarpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_deltarpmmodule.so
%{py3_sitedir}/deltarpm.py
%{py3_sitedir}/__pycache__/deltarpm.cpython-*.py[co]
%endif
