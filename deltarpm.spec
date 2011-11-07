%define		subver	20110223
%define		rel		1
Summary:	Create deltas between rpms
Summary(pl.UTF-8):	Generowanie różnic między pakietami rpm
Name:		deltarpm
Version:	3.6
Release:	0.%{subver}git.%{rel}
License:	BSD
Group:		Base
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/deltarpm/%{name}-git-%{subver}.tar.bz2/70f8884be63614ca7c3fc888cf20ebc8/deltarpm-git-%{subver}.tar.bz2
# Source0-md5:	70f8884be63614ca7c3fc888cf20ebc8
Patch0:		%{name}-3.4-no-skip-doc.patch
Patch1:		%{name}-3.4-pld.patch
Patch2:		%{name}-rpmdumpheader.patch
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
Deltarpm zawiera różnice pomiędzy starą i nową wersją pakietu rpm,
pozwalając na stworzenie nowej wersji na podstawie delty i starej
wersji. Nie jest konieczne posiadanie kopii starego pakietu rpm,
deltarpm obsługuje także już zainstalowane pakiety.

%package -n drpmsync
Summary:	Sync a file tree with deltarpms
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with deltarpms.

%package -n deltaiso
Summary:	Create deltas between isos containing rpms
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos, a
difference between an old and a new iso containing rpms.

%package -n python-deltarpm
Summary:	Python bindings for deltarpm
Group:		Base
# does not require base package

%description -n python-deltarpm
This package contains python bindings for deltarpm.

%prep
%setup -q -n %{name}-git-%{subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's/python3//' Makefile

%build
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -I/usr/include/rpm" \
	bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
	zlibbundled='' zlibldflags='-lz' zlibcppflags=''

%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags}" \
	bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
	zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
	python

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
%{_mandir}/man8/applydeltaiso*
%{_mandir}/man8/makedeltaiso*

%files -n drpmsync
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/drpmsync
%{_mandir}/man8/drpmsync*

%files -n python-deltarpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_deltarpmmodule.so
%{py_sitedir}/deltarpm.py[co]
