Summary:	Create deltas between rpms
Summary(pl.UTF-8):	Generowanie różnic między pakietami rpm
Name:		deltarpm
Version:	3.4
Release:	1
License:	BSD
Group:		Base
Source0:	ftp://ftp.suse.com/pub/projects/deltarpm/%{name}-%{version}.tar.bz2
# Source0-md5:  cac779a18a1bc256fb6497526a83ac82
Patch0:		%{name}-3.4-multilib-workaround.patch
Patch1:		%{name}-3.4-multilib-include-colored.patch
Patch2:		%{name}-3.4-prelink-bugfix.patch
Patch3:		%{name}-3.4-no-skip-doc.patch
Patch4:		%{name}-3.4-pld.patch
URL:		http://www.novell.com/products/linuxpackages/professional/deltarpm.html
BuildRequires:	bzip2-devel
BuildRequires:	rpm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A deltarpm contains the difference between an old and a new version of
a rpm, which makes it possible to recreate the new rpm from the
deltarpm and the old one. You don't have to have a copy of the old
rpm, deltarpms can also work with installed rpms.

%description -l pl.UTF-8
Deltarpm zawiera różnice pomiędzy starą i nową wersją pakietu rpm,
pozwaljąc na stworzenie nowej wersji na podstawie delty i starej
wersji. Nie jest konieczne posiadanie pakietu rpm, deltarpm wspiera
takze już zainstalowane pakiety.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} \
	CFLAGS="$RPM_OPT_FLAGS" \
	bindir=%{_bindir} \
	mandir=%{_mandir} \
	prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.BSD README
%attr(755,root,roto) %{_bindir}/*
%{_mandir}/man8/*
