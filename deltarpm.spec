Summary:	Create deltas between rpms
Name:		deltarpm
Version:	3.4
Release:	5
License:	BSD
Group:		Base
URL:		http://www.novell.com/products/linuxpackages/professional/deltarpm.html

Source0:	ftp://ftp.suse.com/pub/projects/deltarpm/%{name}-%{version}.tar.bz2
# Source0-md5:  cac779a18a1bc256fb6497526a83ac82

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:	bzip2-devel
BuildRequires:	rpm-devel

Patch0:		%{name}-3.4-multilib-workaround.patch
Patch1:		%{name}-3.4-multilib-include-colored.patch
Patch2:		%{name}-3.4-prelink-bugfix.patch
Patch3:		%{name}-3.4-no-skip-doc.patch
Patch4:		%{name}-3.4-pld.patch

%description
A deltarpm contains the difference between an old and a new version of
a rpm, which makes it possible to recreate the new rpm from the
deltarpm and the old one. You don't have to have a copy of the old
rpm, deltarpms can also work with installed rpms.

%prep
%setup -q
%patch0 -p0 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
	bindir=%{_bindir} mandir=%{_mandir} prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.BSD README
%{_mandir}/man8/*
%attr(755,root,root) %{_bindir}/applydeltaiso
%attr(755,root,root) %{_bindir}/applydeltarpm
%attr(755,root,root) %{_bindir}/combinedeltarpm
%attr(755,root,root) %{_bindir}/drpmsync
%attr(755,root,root) %{_bindir}/fragiso
%attr(755,root,root) %{_bindir}/makedeltaiso
%attr(755,root,root) %{_bindir}/makedeltarpm
%attr(755,root,root) %{_bindir}/rpmdumpheader
